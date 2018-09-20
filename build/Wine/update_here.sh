#!/bin/bash

# Do not use "verbose" in order to spot errors easily

mkdir -p resources/locale/ru/LC_MESSAGES/

# Copy shared resources
cp -u /usr/local/bin/shared/resources/{error,info,question,warning}.gif ./resources/

# Copy Yatube resources
cp -u /usr/local/bin/Yatube/resources/nopic.png ./resources
cp -u /usr/local/bin/Yatube/resources/locale/ru/LC_MESSAGES/yatube.mo ./resources/locale/ru/LC_MESSAGES/yatube.mo

# Copy Yatube Python files
cp -u /usr/local/bin/Yatube/src/{db,gui,logic,tests,yatube}\.py .

# Copy shared Python files
cp -u /usr/local/bin/shared/src/{gettext_windows,shared,sharedGUI}.py .

# (all platforms) Copy Yatube icon
cp -u /usr/local/bin/Yatube/resources/icon_64x64_yatube.gif ./resources/
# (Wine-only) Copy Yatube icon
cp -u /usr/local/bin/Yatube/resources/icon_64x64_yatube.ico ./resources/

# (Wine-only) Copy build scripts
cp -u /usr/local/bin/Yatube/build/Wine/{build.sh,clean_up.sh,setup.py,update_yatube.sh,Yatube.cmd} .

ls --color=always .
