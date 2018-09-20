#!/bin/bash

# Do not use "verbose" in order to spot errors easily

ver='3.5'

./update_here.sh
./build.sh
mkdir -p Yatube/app
cp -r resources ./Yatube
mv build/exe.linux-i686-$ver/* ./Yatube/app
rmdir -p build/exe.linux-i686-$ver
rm -rf ./Yatube/app/{libicudata.so.54,libicui18n.so.54,libicuuc.so.54,libQt*,platforms,imageformats}
rm -rf ./Yatube/app/lib/python$ver/{pymorphy*,pyasn*,PyQt5}
# Only for Centos6
#cp /usr/lib/python$ver/site-packages/httplib2/socks.py ./Yatube/app/lib/python$ver/httplib2/
ls --color=always .
