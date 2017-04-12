#Dockerfile for python-opencv

# Pull base image.
FROM ubuntu:16.04

MAINTAINER  <v.bontoux@free.fr>

# Install packages.
RUN apt-get update
RUN apt-get install -y python2.7-dev python3.5-dev
RUN apt-get install -y build-essential cmake pkg-config
RUN apt-get install -y libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev
RUN apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
RUN apt-get install -y libatlas-base-dev gfortran
# Compile opencv
RUN apt-get install -y wget
RUN apt-get install -y unzip
WORKDIR /tmp/
RUN wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
RUN unzip opencv.zip
RUN wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
RUN unzip opencv_contrib.zip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN ln -s /usr/bin/python2.7 /usr/bin/python
RUN python get-pip.py
RUN pip install virtualenv
RUN pip install numpy
WORKDIR /tmp/opencv-3.1.0/
RUN mkdir build
WORKDIR /tmp/opencv-3.1.0/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib-3.1.0/modules \
    -D PYTHON_EXECUTABLE=/usr/bin/python \
    -D BUILD_EXAMPLES=ON ..
RUN make -j4
RUN make install
RUN ldconfig
RUN pip install matplotlib
RUN apt-get install -y python-tk
# Define working directory.
WORKDIR /app

# Define default command.
CMD ["bash"]
