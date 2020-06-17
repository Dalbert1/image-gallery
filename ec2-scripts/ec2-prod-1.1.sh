#!/usr/bin/bash
export IMAGE_GALLERY_BOOTSTRAP_VERSION="1.1"
CONFIG_BUCKET="edu.au.cc.python-image-gallery-config"

# Install Packages
sudo yum update -y
sudo yum install -y python3 git postgres postgresql-devel gcc python3-devel
amazon-linux-extras install -y nginx1

# Configure/install custom software
cd /home/ec2-user/
git clone https://github.com/Dalbert1/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
cd python-image-gallery/
sudo pip3 install -r requirements.txt --user

aws s3 cp s3://${CONFIG_BUCKET}/nginx/nginx.conf /etc/nginx
aws s3 cp s3://${CONFIG_BUCKET}/nginx/default.d/image_gallery.conf /etc/nginx/default.d


# Start/enable services
systemctl stop postfix
systemctl disable postfix
systemctl start nginx
systemctl enable nginx

su ec2-user -l -c "cd ~/python-image-gallery && ./start">/var/log/image_gallery.log 2>&1 &
