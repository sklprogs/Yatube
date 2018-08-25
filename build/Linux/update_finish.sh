#!/bin/sh

# Do this after testing the program

rm -f $HOME/binaries/Yatube/linux.tar.bz2
tar -cvjSf $HOME/binaries/Yatube/linux.tar.bz2 ./Yatube
rm -r ./Yatube
./clean_up.sh
