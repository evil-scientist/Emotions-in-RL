FROM ubuntu:16.04
MAINTAINER Chenna Varri

RUN apt-get update
RUN apt-get install -y build-essential apt-utils

RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev \
  libavformat-dev libswscale-dev
RUN  apt-get update && apt-get install -y python-dev python-numpy \
  python3 python3-pip python3-dev libtbb2 libtbb-dev \
  libjpeg-dev libjasper-dev libdc1394-22-dev \
  python-opencv libopencv-dev libav-tools python-pycurl \
  libatlas-base-dev gfortran webp qt5-default libvtk6-dev zlib1g-dev

RUN pip3 install numpy

RUN apt-get install -y python-pip
RUN pip install --upgrade pip

RUN cd ~/ &&\
    git clone https://github.com/Itseez/opencv.git &&\
    git clone https://github.com/Itseez/opencv_contrib.git &&\
    cd opencv && mkdir build && cd build && cmake  -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON .. && \
    make -j4 && make install && ldconfig && rm -rf ~/opencv*  # Remove the opencv folders to reduce image size

# Set the appropriate link
RUN ln /dev/null /dev/raw1394

RUN pip3 install numpy scipy scikit-learn pillow tensorflow pandas h5py keras statistics pyyaml pyparsing cycler matplotlib Flask

RUN apt-get -y install libv4l-dev

ADD . /

ENV PYTHONPATH=$PYTHONPATH:src
ENV FACE_CLASSIFIER_PORT=8084
EXPOSE $FACE_CLASSIFIER_PORT

ENV QT_QPA_PLATFORM offscreen

ENTRYPOINT ["python3"]
CMD ["src/video_emotion_color_demo.py"]
