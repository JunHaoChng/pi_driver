#!/bin/bash

# Linux
CURL='/usr/bin/curl'

working_directory=$PWD/..
echo $working_directory

url="http://www.airspayce.com/mikem/bcm2835/bcm2835-1.68.tar.gz"
filename="bcm2835_zip"
filename_extract='bcm2835'
$CURL $url -o $filename
mkdir $filename_extract 
tar -C $filename_extract -zxf $filename

rm -r $filename

#cd into directory
cd $filename_extract/bcm2835*

# need sudo permission
./configure
make
sudo make check
sudo make install

echo $PWD
cd ..
mv bcm2835* ../
cd ..
rm -r $working_directory/$filename_extract
