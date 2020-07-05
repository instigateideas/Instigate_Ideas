# Pull and containerize the Python 3.6 Image from Docker Hub
FROM python:3.6.5

# Install System Dependencies to the root of the image
RUN apt-get -y update \
	&& apt-get -y install unzip \
	&& apt-get -y upgrade python3 \
	&& apt -y install python3-pip \
	&& apt install -y xvfb \
	&& apt-get install -y x11-utils \
	&& apt install -y libgirepository1.0-dev \
	&& apt-get install -y libcairo2-dev \
	&& apt-get install bash

# Install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
	&& dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Create necessary folders
RUN mkdir /home/seluser

# PIP install packages
RUN pip3 install pycairo
RUN pip3 install pyvirtualdisplay

# Copy the folder needed along with requirements.txt
COPY ./app.zip /home/seluser
RUN unzip /home/seluser/app.zip -d /home/seluser/
RUN echo unziping sucessfully done
RUN rm -rf /home/seluser/app.zip

# Bind map the volume to the local app folder
VOLUME /home/seluser/app

# Upgrade pip version and install all the requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r /home/seluser/app/requirements.txt

EXPOSE 5555
WORKDIR /home/seluser/app/

CMD ["python3","app.py"]