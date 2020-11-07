# docker file for discord GEEKS Bot

FROM python:3

MAINTAINER alkersh.omar@protonmail.com

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPIONT sh discord_bot.sh
CMD sh discord_bot.sh
