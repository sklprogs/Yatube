#!/bin/sh

# Do this after testing the program

rm -f $HOME/binaries/Yatube/lin32.tar.bz2
tar -cvjSf $HOME/binaries/Yatube/lin32.tar.bz2 ./Yatube
rm -r ./Yatube
./clean_up.sh
