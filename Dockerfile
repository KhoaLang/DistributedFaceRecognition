# Runtime Image
FROM apache/spark:3.5.0-scala2.12-java11-python3-r-ubuntu

USER root
# Install Dependencies
RUN apt-get -y update && apt-get install -y --fix-missing \
    build-essential \
    cmake gcc\ 
    gfortran \
    git \
    tar \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3.8-venv \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip ffmpeg\
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

# Virtual Environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    SPARK_LOG_DIR=/opt/spark/logs \
    SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
    SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
    SPARK_MASTER_PORT=7077 \
    SPARK_MASTER_WEBUI_PORT=8080 \
    SPARK_WORKER_WEBUI_PORT=8080 \
    SPARK_WORKER_PORT=7000\
    SPARK_MASTER_URL=spark://spark-master:7077

RUN mkdir -p $SPARK_LOG_DIR && \
    touch $SPARK_MASTER_LOG && \
    touch $SPARK_WORKER_LOG && \
    ln -sf /dev/stdout $SPARK_MASTER_LOG && \
    ln -sf /dev/stdout $SPARK_WORKER_LOG

# Install Dlib
ENV CFLAGS=-static
RUN pip3 install --upgrade pip && \
    git clone https://github.com/davisking/dlib.git && \
    cd dlib &&\
    mkdir build; cd build; cmake ..; cmake --build . &&\
    cd .. && python3 setup.py install

COPY ./requirements.txt ./
COPY ./setup_spark/start_spark.sh ./
RUN pip3 install -r requirements.txt

CMD ["/bin/bash", "start_spark.sh"]