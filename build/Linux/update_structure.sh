#!/bin/bash

# Do not use "verbose" in order to spot errors easily

mkdir -p resources/locale/ru/LC_MESSAGES/ src

# Copy shared resources
cp -u $HOME/bin/shared/resources/{error,info,question,warning}.gif ./resources/

# Copy Yatube resources
cp -u $HOME/bin/Yatube/resources/nopic.png ./resources
cp -u $HOME/bin/Yatube/resources/locale/ru/LC_MESSAGES/yatube.mo ./resources/locale/ru/LC_MESSAGES/yatube.mo

# Copy Yatube Python files
cp -u $HOME/bin/Yatube/src/{db,gui,logic,tests,yatube}\.py ./src/

# Copy shared Python files
cp -u $HOME/bin/shared/src/{gettext_windows,shared,sharedGUI}.py ./src/

# Copy Yatube icon
cp -u $HOME/bin/Yatube/resources/icon_64x64_yatube.gif ./resources/

rm ./update_structure.sh

ls --color=always .
