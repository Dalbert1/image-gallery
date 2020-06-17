#!/usr/bin/bash
export IMAGE_GALLERY_BOOTSTRAP_VERSION="1.0"

# Install Packages
sudo yum update -y
sudo yum install -y python3 git

# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/Dalbert1/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
cd python-image-gallery/
pip3 install -r requirements.txt --user 

# Start/enable services
systemctl stop postfix
systemctl disable postfix

su ec2-user -l -c "cd ~/python-image-gallery && ./start">/var/log/image_gallery.log 2>&1 &
