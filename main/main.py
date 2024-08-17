import cv2
from pyspark.sql import SparkSession
import numpy as np
from collections import namedtuple
import time
from datetime import date
from multiprocessing.pool import ThreadPool
import subprocess
import itertools

class RTMPStream:
    def __init__(self, width, height, fps, stream_key):
        self.rtmp_url = f"rtmp://rtmp-stream-server:1935/live/stream-{stream_key}"
        self.p = None 
        self.width = width
        self.height = height
        self.fps = fps

    def init_rtmp_streaming(self):
        command = [
            'ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', "{}x{}".format(self.width, self.height),
            '-r', str(self.fps),
            '-i', '-',
            '-c:v', 'libx264',
            '-bufsize', '64M',
            '-maxrate','4M',
            "-flvflags", "no_duration_filesize",
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-f', 'flv',
            self.rtmp_url
        ]
        self.p = subprocess.Popen(command, stdin=subprocess.PIPE)
    
    def get_subprocess(self):
        return self.p
    
    def publish_rtmp_streaming(self, frame):
        self.p.stdin.write(frame.tobytes())

class ProcessFrame:
    @staticmethod
    def encode_frame_bytes(frame_or_str, decode = False):
        if not decode:
            # input: frame np.array
            # output: bytes 
            return bytearray(cv2.imencode('.jpg', frame_or_str)[1].tobytes())
        else:
            # input: bytes
            # ouput: np.array
            nparr = np.frombuffer(bytes(frame_or_str), np.uint8)
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    @staticmethod
    def utilize_spark(sc, frame_batch, face_recog, rtmp, stream_key):
        try:
            rdd = sc.parallelize(frame_batch)
            processed = rdd.map(lambda row: ProcessFrame.process_frame_udf(row, face_recog, stream_key))
            dataCol = processed.collect()
            total_fps = 0

            date_now = date.today().strftime('%Y%B%d')
            f = open(f"./log/{date_now}_fps_{stream_key}.txt", "a")
            fps_list = []
            for i in range (0, len(dataCol)):
                row = dataCol[i]
                row_frame = ProcessFrame.encode_frame_bytes(row[0], decode=True)
                rtmp.publish_rtmp_streaming(row_frame)

                if float(row[1]) < 500: f.write(f"{float(row[1])}\n")
            f.close()

        except Exception as err:
            print("Err:", err)

    @staticmethod
    def process_frame_udf(frame_bytes, face_recog, stream_key):
        frame = ProcessFrame.encode_frame_bytes(frame_bytes[0], decode=True)

        start_time = time.time()
        frame = face_recog.publish_video(frame, stream_key)
        end_time = time.time()

        Record = namedtuple("Record", ['frames', 'fps'])
        return Record(ProcessFrame.encode_frame_bytes(frame), 1/(end_time-start_time))

def main_loop(spark, sc, face_recog, video, stream_key):
    cap = cv2.VideoCapture(video)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    global length
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    rtmp = RTMPStream(width, height, fps, stream_key)
    rtmp.init_rtmp_streaming()
    Record = namedtuple("Record", ['frames'])

    frame_batch=[]
    global BATCH_SIZE
    BATCH_SIZE = 60
    frame_counter = 0

    print("Reading !!")
    while True:
        ret, frame = cap.read()
        frame_counter += 1
        if not ret:
            break

        if len(frame_batch) >= BATCH_SIZE:
            ProcessFrame.utilize_spark(sc,frame_batch, face_recog, rtmp, stream_key)
            frame_batch = [] 
        frame_batch.append( Record(ProcessFrame.encode_frame_bytes(frame) ))

        if frame_counter == length:
            if len(frame_batch) <= BATCH_SIZE:
                ProcessFrame.utilize_spark(sc,frame_batch, face_recog, rtmp, stream_key)
                frame_batch = [] 
            frame_counter = 0 #Or whatever as long as it is the same as next line
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_counter)
    print("Done Reading !!")

if __name__ == "__main__":

    spark = SparkSession.builder.appName("VideoProcessing")\
        .master("spark://spark-master:7077").getOrCreate()
    sc = spark.sparkContext
    sc.addFile("./classes/face_recog_class.py")
    sc.addFile("./classes/ref_embed.pkl")
    sc.addFile("./classes/ref_name.pkl")
    from face_recog_class import Face_Recog

    face_recog = Face_Recog("./classes/ref_name.pkl","./classes/ref_embed.pkl")

    # ****Modify the video paths that you want to stream****
    videos = ["./videos_sample/v2.mp4", "./videos_sample/v1.mp4", "./videos_sample/v2.mp4"] * 2
    # ******************************************************
    
    keys = [f'{i}' for i in range(1, len(videos)+1)]
    pool = ThreadPool( len(videos)*2 )
    opt = pool.starmap(main_loop, zip(itertools.repeat(spark), itertools.repeat(sc), itertools.repeat(face_recog), videos, keys))
