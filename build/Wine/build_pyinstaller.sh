#!/bin/bash

cp $HOME/bin/Yatube/build/Wine/update_structure.sh .
./update_structure.sh
mkdir Yatube
cd src
wine pyinstaller yatube.py
mv dist/yatube ../Yatube/app
cd ..
cp $HOME/bin/Yatube/build/Wine/Yatube.cmd ./Yatube
mv resources ./Yatube/
cd Yatube/app && wine yatube.exe
read -p "Update the archive? (y/n) " choice
if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
	rm -f $HOME/binaries/Yatube/win32.zip
	cd ../.. && zip -rv $HOME/binaries/Yatube/win32.zip Yatube/ && rm -r Yatube src
fi
