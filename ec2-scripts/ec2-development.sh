#!/usr/bin/bash

# install packages
yum -y update
yum install -y emacs-nox nano tree python3
yum install -y git
amazon-linux-extras install -y nginx1
yum install -y gcc
yum install -y python3-devel
yum install -y postgresql-devel

# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/ghgoodreau/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
cd ~/python-image-gallery
su ec2-user -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

# start/enable cervices
systemctl start nginx
systemctl enable nginx
systemctl stop postfix
systemctl disable postfix
