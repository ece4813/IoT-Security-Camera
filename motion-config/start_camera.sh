#!/bin/bash

echo starting motion detection

if [ ! -f /etc/motion/motion.conf ]; then
    echo "File not found!"
    sudo apt-get install motion
    sudo cp /home/fiifi/Desktop/4813/PROJECT/IoTCamera/setup/motion-config /etc/motion
    sudo motion 
else
    sudo motion
fi


