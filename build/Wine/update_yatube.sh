#!/bin/bash

ver='3.4'

./update_here.sh
./build.sh
mkdir -p ./Yatube/app
mv ./build/exe.win32-$ver/* ./Yatube/app/
rmdir -p build/exe.win32-$ver
cp -r $HOME/bin/shared_bin_win/* ./Yatube/app/
cp $HOME/.wine/drive_c/Python34/Lib/site-packages/httplib2/socks.py ./Yatube/app/
cp -r ./resources ./Yatube/
cp ./Yatube.cmd ./Yatube/

cd Yatube/app && wine yatube.exe
read -p "Update the archive? (y/n) " choice
if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
	rm -f $HOME/binaries/Yatube/win32.zip
	cd ../.. && zip -rv $HOME/binaries/Yatube/win32.zip Yatube/ && rm -r Yatube
	./clean_up.sh
fi
