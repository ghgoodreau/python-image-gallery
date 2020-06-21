#!/usr/bin/bash

export IMAGE_GALLERY_SCRIPT_VERSION="1.1"

# install packages
yum -y update
yum install -y python3 python3-devel git postgresql postgresql-devel gcc
amazon-linux-extras install -y nginx1

# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/ghgoodreau/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
cd ~/python-image-gallery
su ec2-user -l -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

aws s3 cp s3://ghg.rocks.image-gallery/nginx/nginx.conf /etc/nginx
aws s3 cp s3://ghg.rock.image-gallery/nginx/default.d/image_gallery.conf /etc/nginx/default.d

# start/enable services
systemctl stop postfix
systemctl disable postfix
systemctl start nginx
systemctl enable nginx

su ec2-user -l -c "cd ~/python-image-gallery && ./start">/var/log/image_gallery.log 2>&1 &
