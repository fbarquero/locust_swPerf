#!/usr/bin/env bash
echo "INSTALLING OS DEPENDENCIES"
yum install libxslt-devel libxml2-devel -y
sudo yum install make automake gcc gcc-c++ kernel-devel git-core -y
sudo yum install libpng-devel freetype-devel -y

echo "INSTALLING FIRST SET OF PYTHON MODULES..."
pip install -r requirements_linux_01.txt

echo "INSTALLING MATPLOTLIB.."
pip install --no-cache-dir matplotlib

