#!/bin/bash

# Do not use "verbose" in order to spot errors easily

mkdir -p resources/locale/ru/LC_MESSAGES/

# Copy shared resources
cp -u $HOME/bin/shared/resources/{error,info,question,warning}.gif ./resources/

# Copy Yatube resources
cp -u $HOME/bin/Yatube/resources/nopic.png ./resources
cp -u $HOME/bin/Yatube/resources/locale/ru/LC_MESSAGES/yatube.mo ./resources/locale/ru/LC_MESSAGES/yatube.mo

# Copy Yatube Python files
cp -u $HOME/bin/Yatube/src/{db,gui,logic,tests,yatube}\.py .

# Copy shared Python files
cp -u $HOME/bin/shared/src/{gettext_windows,shared,sharedGUI}.py .

# Copy Yatube icon
cp -u $HOME/bin/Yatube/resources/icon_64x64_yatube.gif ./resources/

# (Linux-only) Copy build scripts
cp -u $HOME/bin/Yatube/build/Linux/{build.sh,clean_up.sh,setup.py,update_finish.sh,update_yatube.sh} .

ls --color=always .
