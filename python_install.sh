#!/bin/sh
RELEASE=3.6.3

# install dependencies
sudo apt-get install libxml2-dev libxslt1-dev sqlite3
sudo apt-get install python3-dev libffi-dev libssl-dev openssl
sudo apt-get install libbz2-dev liblzma-dev libsqlite3-dev libncurses5-dev libgdbm-dev zlib1g-dev libreadline-dev libssl-dev tk-dev

# download and build Python
mkdir ~/python3
cd ~/python3
wget https://www.python.org/ftp/python/$RELEASE/Python-$RELEASE.tar.xz
tar xvf Python-$RELEASE.tar.xz
cd Python-$RELEASE
./configure
make
sudo make install
sudo rm -rf ~/python3/Python-$RELEASE
cd ~