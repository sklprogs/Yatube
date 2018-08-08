#!/bin/sh

# Do not use "verbose" in order to spot errors easily

./update_here.sh
./build.sh
mkdir -p Yatube/app
cp -r resources user ./Yatube
mv build/exe.linux-i686-3.4/* ./Yatube/app
rmdir -p build/exe.linux-i686-3.4
rm -r ./Yatube/app/{libicudata.so.54,libicui18n.so.54,libicuuc.so.54,libQt*,platforms,imageformats}
rm -r ./Yatube/app/lib/python3.4/{pymorphy*,pyasn*,PyQt5}
cp /usr/lib/python3.4/site-packages/httplib2/socks.py ./Yatube/app/lib/python3.4/httplib2/
ls --color=always .
