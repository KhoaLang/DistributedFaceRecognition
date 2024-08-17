<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/6295/6295417.png" width="100" />
</p>
<p align="center">
    <h1 align="center">FACE RECOGNITION ON DISTRIBUTED SYSTEM USING APACHE SPARK</h1>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/KhoaLang/DistributedFaceRecognition?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/KhoaLang/DistributedFaceRecognition?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/KhoaLang/DistributedFaceRecognition?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/KhoaLang/DistributedFaceRecognition?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/apachespark-E25A1C.svg?style=flat&logo=apachespark&logoColor=white" alt="Spark">
	<img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
</p>
<hr>

## Quick Links

> - [Overview](#Overview)
> - [Features](#-features)
> - [Features](#-description)
> - [Repository Structure](#-repository-structure)
> - [Modules](#-modules)
> - [Getting Started](#-getting-started)
>   - [Installation](#-installation)
>   - [Run the project](#-run-the-project)
> - [Project Roadmap](#-project-roadmap)
> - [License](#-license)
> - [References](#References)

---

## Overview

- This project demonstrates a distributed face recognition system built using Apache Spark. By leveraging the parallel processing capabilities of Spark, this system can efficiently handle large-scale face recognition tasks, making it suitable for scenarios that require processing vast amounts of video or image data in real-time. The system is containerized using Docker and supports streaming via RTMP, allowing for scalable and flexible deployment across multiple nodes.

- The primary goal of this project was to deploy on an edge device cluster (like Jetson Nano, Raspberry Pi,etc) enhancing both performance and scalability. But the cost of the real devices are not affordable therefore I will just use docker and try to use Kubernetes as Cluster Manager to mimic the behaviour of a physical cluster.

## Features

- Distributed Processing with Apache Spark: Utilizes Apache Spark to distribute the face recognition workload across multiple nodes, enabling efficient processing of large datasets.

- Real-Time Video Streaming: Integrates with an RTMP server for real-time streaming, allowing the system to process and recognize faces in live video feeds.

- Containerized Deployment: Uses Docker to containerize the application, ensuring a consistent environment and simplifying deployment across different platforms.

- Scalable Architecture: Designed to scale horizontally by adding more worker nodes to the Spark cluster, making it capable of handling growing data volumes.

- Customizable Training: Allows users to train the face recognition model with their datasets, offering flexibility in recognizing different sets of faces.

## Description

**NOTE**: In this project scope, the term **train/training** is stand for **embeding**.

The use of the Face Recognition library in this project is for embed the image of a person with their name. So the recognition phase is using the same library to embed the captured video/image and then compared it with the stored embeded images, which contained registered faces in the training phase.

(Comparing vector)

## Repository Structure

```sh
└── Face_Recognition_On_Distributed_System_Using_Apache_Spark/
    ├── Dockerfile
    ├── Dockerfile.rtmpserver
    ├── README.md
    ├── docker-compose.yml
    ├── main
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── face_recog.cpython-38.pyc
    │   │   ├── face_recog_class.cpython-38.pyc
    │   │   └── logging.cpython-38.pyc
    │   ├── classes
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-38.pyc
    │   │   │   └── face_recog_class.cpython-38.pyc
    │   │   ├── face_recog_class.py
    │   │   ├── ref_embed.pkl
    │   │   ├── ref_name.pkl
    │   ├── get_config.py
    │   ├── log
    │   │   ├── config_spark.txt
    │   │   └── frames_shape.txt
    │   ├── main.py
    │   ├── process_in_single.py
    │   └── videos_sample
    │       ├── quin.mp4
    │       ├── v1.mp4
    │       └── v2.mp4
    ├── requirements.txt
    ├── setup_spark
    │   ├── spark-submit.sh
    │   ├── start-master.sh
    │   ├── start-worker.sh
    │   └── start_spark.sh
    ├── train_dataset
    │   ├── TestDataset_kltn
    │   ├── khoa-19521692
    │   └── trainning_dataset_Feb29
    └── utils
        └── nginx_config.txt
```

---

## Modules

<details closed><summary>.</summary>

| File                                                                                                                                             | Summary                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| [Dockerfile.rtmpserver](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/Dockerfile.rtmpserver) | Setting up a RTMP server container for streaming task                   |
| [docker-compose.yml](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/docker-compose.yml)       | Start and mange all the related services                                |
| [Dockerfile](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/Dockerfile)                       | Setting up the main environment with Spark and Face Recognition library |
| [requirements.txt](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/requirements.txt)           | Listed out all the libraries required to run this project               |

</details>

<details closed><summary>setup_spark</summary>

| File                                                                                                                                             | Summary                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------- |
| [spark-submit.sh](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/setup_spark/spark-submit.sh) | Configuring the spark-submit      |
| [start-master.sh](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/setup_spark/start-master.sh) | Configuring the Spark master node |
| [start-worker.sh](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/setup_spark/start-worker.sh) | Configuring the Spark worker node |
| [start_spark.sh](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/setup_spark/start_spark.sh)   | Start spark in overall            |

</details>

<details closed><summary>main</summary>

| File                                                                                                                                  | Summary                                                |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [main.py](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/main/main.py)             | Start the streaming process as well as the recognition |
| [get_config.py](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/main/get_config.py) | Get the spark config                                   |

</details>

<details closed><summary>main.classes</summary>

| File                                                                                                                                                      | Summary                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [face_recog_class.py](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/main/classes/face_recog_class.py) | Define the face recognition behaviour in this project scope |

</details>

<details closed><summary>main.log</summary>

| File                                                                                                                                            | Summary                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| [config_spark.txt](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/main/log/config_spark.txt) | output of the get_config.py |
| [frames_shape.txt](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/main/log/frames_shape.txt) | Shape of a frame/image      |

</details>

<details closed><summary>utils</summary>

| File                                                                                                                                         | Summary                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| [nginx_config.txt](https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark/blob/master/utils/nginx_config.txt) | nginx configuration for the RMPT Server |

</details>

---

## Getting Started

**_Requirements_**

Ensure you have the following dependencies installed on your system:

- **Docker**: `Any stable version`
- **VLC**: `Any version`

**Note: Work best on Ubuntu v22**

### Setting up

1. Clone the Face_Recognition_On_Distributed_System_Using_Apache_Spark repository:

```sh
git clone https://github.com/KhoaLang/Face_Recognition_On_Distributed_System_Using_Apache_Spark
```

2. Change to the project directory:

```sh
cd Face_Recognition_On_Distributed_System_Using_Apache_Spark
```

3. Launch docker containers with docker compose:

```sh
docker compose up
```

or

```sh
docker-compose up
```

4. Wait till the third step succeed then get the **spark master** container id with:

```sh
docker ps
```

Note: **The spark master container will have a postfix "master" in container name**

5. Copy the **spark master** container id then access to container bash:

```sh
docker exec -it {container_id} /bin/bash
```

### Run the project

#### Train (Embeding):

```sh
cd ../spark_script/Face_Recognition_On_Distributed_System_Using_Apache_Spark/main
```

1. Modify the train/embeding dataset as you need in **main/train.py**

```
train_entry = TrainingEntry({your_path})
```

2. Use the following command for trainning:

```sh
python train.py
```

#### Run:

Modify the path to the video/stream which you want to run in **main.py**:

```
# ****Modify the video paths that you want to stream****
videos = ["./videos_sample/v2.mp4", "./videos_sample/v1.mp4", "./videos_sample/v2.mp4"] * 2
# ******************************************************
```

**IMPORTANT**:
The output stream will be indexed with **key** from 1 to **n**.
With **n** is the number of videos that you put in the above row.

Use the following command to run:

```sh
python main.py
```

#### Watch the stream:

Use another machine in same network to observe the stream.

- Open VLC
- Hit **Media** -> **Open Network Stream**
- Paste **rtmp://{streaming_source_ip}/live/stream-{key}** to network URL.

With:

- **streaming_source_ip**: ip of the machine run this project

Open as many VLC windows as the number of videos that you put into the main function.

## Project Roadmap

- [x] `► Build foundation: implementing spark and rtmp protocol to stream`
- [ ] `► Implementing Kubernetes as Cluster Manager`
- [ ] `► ...`

## License

This project is protected under the NONE License. I just specify this section for fun.

## References

This project was built based on the library:

- [Face Recognition](https://github.com/ageitgey/face_recognition/) of Adam Geitgey
