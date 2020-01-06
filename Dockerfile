# docker file for discord GEEKS Bot

FROM archlinux/base

RUN pacman -Syyuu --noconfirm # update everything
RUN pacman -Sy python  # install python, no need for venv
RUN mkdir /program

ENV WORKDIR /program
WORKDIR $WORKDIR
ADD . /program

RUN pip install -r requirements

# maybe this will work?
RUN python sheets_interface.py > sheets_url

# ENTRYPIONT sh discord_bot.sh
