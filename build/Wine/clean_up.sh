#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove shared resources
rm -f ./resources/{error.gif,info.gif,question.gif,warning.gif}

# Remove Yatube resources
rm -f ./resources/{nopic.png,block.txt,subscribe.txt}

# Remove optional Yatube resources
rm -f ./resources/{subscribe2.txt,yatube.db}

# Remove other Yatube resources
rm -f ./resources/locale/ru/LC_MESSAGES/yatube.mo

# Remove Yatube Python files
rm -f ./{db,gui,logic,tests,yatube}\.py

# Remove shared Python files
rm -f ./{gettext_windows.py,shared.py,sharedGUI.py}

# (Wine-only) Remove Yatube icon
rm -f ./resources/icon_64x64_yatube\.{ico,gif}

# (Wine-only) Remove build scripts
rm -f {build.sh,clean_up.sh,setup.py}

# Do not use dots in case of '-p' key
rmdir -p resources/locale/ru/LC_MESSAGES/

ls .
