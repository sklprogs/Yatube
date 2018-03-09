#!/bin/sh

# Do not use "verbose" in order to spot errors easily

mkdir -p resources/locale/ru/LC_MESSAGES/

# Copy shared resources
cp -u /usr/local/bin/shared/resources/{error.gif,info.gif,question.gif,warning.gif} ./resources/

# Copy Yatube resources
cp -u /usr/local/bin/Yatube/resources/{nopic.png,block.txt,subscribe.txt} ./resources

# Copy optional Yatube resources
cp -u /usr/local/bin/Yatube/resources/{subscribe2.txt,yatube.db} ./resources

# Copy other Yatube resources
cp -u /usr/local/bin/Yatube/resources/locale/ru/LC_MESSAGES/yatube.mo ./resources/locale/ru/LC_MESSAGES/yatube.mo

# Copy Yatube Python files
cp -u /usr/local/bin/Yatube/{db,gui,logic,tests,yatube}\.py .

# Copy shared Python files
cp -u /usr/local/bin/shared/{gettext_windows.py,shared.py,sharedGUI.py} .

# (Wine-only) Copy Yatube icon
cp -u /usr/local/bin/Yatube/resources/icon_64x64_yatube\.{ico,gif} ./resources/

# (Wine-only) Copy build scripts
cp -u /usr/local/bin/Yatube/build/Wine/{build.sh,clean_up.sh,setup.py} .

ls .
