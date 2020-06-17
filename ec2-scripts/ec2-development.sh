#!/usr/bin/bash #ec2-development

# Install Packages
sudo yum update -y
sudo yum install -y git
sudo yum install -y python3 tree
amazon-linux-extras install -y java-openjdk11
yum install -y java-11-openjdk-devel

# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/Dalbert1/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
cd python-image-gallery/
sudo pip3 install -r requirements.txt

#su ec2-user -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user" 
# LINE ABOVE DID NOT WORK PROMPTED FOR PASSWORD


# Start/enable services
systemctl stop postfix
systemctl disable postfix
