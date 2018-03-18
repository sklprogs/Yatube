#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove shared resources
rm ./resources/{error,info,question,warning}.gif

# Remove Yatube resources
rm ./resources/nopic.png
rm ./resources/locale/ru/LC_MESSAGES/yatube.mo
rm ./user/{block.txt,subscribe.txt}

# Remove optional Yatube resources
rm ./user/{subscribe2.txt,yatube.db}

# Remove Yatube Python files
rm ./{db,gui,logic,tests,yatube}.py

# Remove shared Python files
rm ./{gettext_windows,shared,sharedGUI}.py

# Remove Yatube icon
rm ./resources/icon_64x64_yatube.gif

# (Linux-only) Remove build scripts
rm {build.sh,clean_up.sh,setup.py}

# Do not use dots in case of '-p' key
rmdir -p resources/locale/ru/LC_MESSAGES/ user/Youtube

ls .
