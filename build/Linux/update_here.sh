#!/bin/sh

# Do not use "verbose" in order to spot errors easily

mkdir -p resources/locale/ru/LC_MESSAGES/
mkdir -p user/Youtube

# Copy shared resources
cp -u /usr/local/bin/shared/resources/{error,info,question,warning}.gif ./resources/

# Copy Yatube resources
cp -u /usr/local/bin/Yatube/resources/nopic.png ./resources
cp -u /usr/local/bin/Yatube/resources/locale/ru/LC_MESSAGES/yatube.mo ./resources/locale/ru/LC_MESSAGES/yatube.mo
cp -u /usr/local/bin/Yatube/user/{block.txt,subscribe.txt} ./user

# Copy optional Yatube resources
#cp -u /usr/local/bin/Yatube/user/{subscribe2.txt,yatube.db} ./user

# Copy Yatube Python files
cp -u /usr/local/bin/Yatube/src/{db,gui,logic,tests,yatube}\.py .

# Copy shared Python files
cp -u /usr/local/bin/shared/src/{gettext_windows,shared,sharedGUI}.py .

# Copy Yatube icon
cp -u /usr/local/bin/Yatube/resources/icon_64x64_yatube.gif ./resources/

# (Linux-only) Copy build scripts
cp -u /usr/local/bin/Yatube/build/Linux/{build.sh,clean_up.sh,setup.py} .

ls .
