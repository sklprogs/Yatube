#!/bin/sh

# Do not use "verbose" in order to spot errors easily

./update_here.sh
./build.sh
mkdir -p Yatube/app
cp -r resources user ./Yatube
mv build/exe.linux-i686-3.4/* ./Yatube/app
rmdir -p build/exe.linux-i686-3.4
rm -r ./Yatube/app/{libicudata.so.54,libicui18n.so.54,libicuuc.so.54,libQt5Core.so.5,libQt5Gui.so.5,PyQt5.QtCore.so,PyQt5.QtGui.so,platforms,imageformats}
ls .
