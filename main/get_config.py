# from pyspark.sql import SparkSession
# from pyspark import SparkConf


# config = SparkConf().setAll([('spark.executor.memory', '8g'), ('spark.executor.cores', '3'), ('spark.cores.max', '3'), ('spark.driver.memory','8g')])
# # sc.stop()
# # sc = pyspark.SparkContext(conf=config)
# spark_session = SparkSession.builder.config(conf=config).getOrCreate()

# config_list = spark_session.sparkContext.getConf().getAll()
# for key, value in config_list:
#     with open("config_spark.txt", "a") as file:
#         file.writelines(f'{key}: {value}\n')

# from face_recog import Face_Recog
import numpy as np
import pickle
# spark_session = SparkSession.builder.getOrCreate()
# fc = Face_Recog()
# print(fc)

array = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])

ser = pickle.dumps(array)
de_ser = pickle.loads(ser)
# Print the array
print(ser)
print(de_ser)