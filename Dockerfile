# ghg0004, docker hub link:

# ubuntu is familiar
FROM ubuntu:latest

# Environment variables
ENV PG_HOST = 0.0.0.0
ENV PG_PORT = 5432
ENV IG_DATABASE = image_gallery
ENV IG_USER = ig_user
ENV IG_PASSWRD = simple
ENV IG_PASSWD_FILE = /ig_password
ENV S3_IMAGE_BUCKET = m6-image-gallery-ghg
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Time Zone request fix
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Build commands
RUN apt-get update -y
RUN apt-get install git python3 python3-pip python3-psycopg2 postgresql -y
RUN mkdir /app
RUN git clone https://github.com/ghgoodreau/python-image-gallery.git /app
RUN useradd -m image_gallery
RUN chown -R image_gallery:image_gallery /app
RUN pip3 install -r /app/requirements.txt

# specifies user
USER image_gallery

# specifies working directory
WORKDIR /app

# EXPOSE
EXPOSE 5555
EXPOSE 8888

# boot commands
CMD ["uwsgi", "--http", ":5555", "--module", "gallery.ui.app:app", "--master", "--processes", "4", "--threads", "2"]
