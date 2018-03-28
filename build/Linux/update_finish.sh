#!/bin/sh

# Do this after testing the program

rm -f /home/pete/tmp/ars/binaries/Yatube/linux.tar.bz2
tar -cvjSf /home/pete/tmp/ars/binaries/Yatube/linux.tar.bz2 ./Yatube
rm -r ./Yatube
./clean_up.sh
