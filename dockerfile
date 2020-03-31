FROM archlinux/base

MAINTAINER omar_alkersh

ENV DISC_REPO="https://github.com/O-Zone-Guy/Discord-GEEKS-Bot.git"
ENV WRK_DIR=/discord

RUN echo "Updating and installing python and git..."
RUN pacman --noconfirm -Syyuu && pacman --noconfirm -Sy python python-pip git

RUN mkdir $WRK_DIR
WORKDIR $WRK_DIR

RUN git clone $DISC_REPO .

RUN pip install -r requirements.txt
