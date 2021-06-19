FROM jenkins/jenkins:2.289.1-lts-jdk11

LABEL maintainer="Arunachalam <m10arunachalam@gmail.com>"

USER root

# install python dependency for ansible
RUN apt -y update
RUN apt -y install python3-pip

# Install Ansible
RUN pip3 install ansible --upgrade

RUN chown -R jenkins:jenkins /var/jenkins_home

USER jenkins

# Exposing the files in volumes
VOLUME ["/var/jenkins_home"]
