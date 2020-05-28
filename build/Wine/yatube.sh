#!/bin/bash

product="Yatube"
productlow='yatube'
python="$HOME/.wine/drive_c/Python"
pyinstaller="$python/Scripts/pyinstaller.exe"
binariesdir="$HOME/binaries"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
cmd="$HOME/bin/$product/build/Wine/$product.cmd"
pildir="$python/Lib/site-packages/PIL"
apidir="$python/Lib/site-packages/google_api_python_client-1.8.4.dist-info"
tmpdir="$HOME/.wine/drive_c/$product" # Will be deleted!
builddir="$tmpdir/$product"           # Will be deleted!

if [ ! -e "$pyinstaller" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -e "$cmd" ]; then
    echo "File $cmd does not exist!"; exit
fi

if [ ! -d "$pildir" ]; then
    echo "Folder $pildir does not exist!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$srcdir" ]; then
    echo "Folder $srcdir does not exist!"; exit
fi

if [ ! -d "$resdir" ]; then
    echo "Folder $resdir does not exist!"; exit
fi

if [ ! -d "$apidir" ]; then
    echo "Folder $apidir does not exist!"; exit
fi

# Build with pyinstaller
rm -rf "$tmpdir"
mkdir -p "$builddir/app"
cp -r "$srcdir"/* "$tmpdir"
cp -r "$resdir" "$builddir"
cp "$cmd" "$builddir"
cd "$tmpdir"
# Icon path should be windows-compliant
wine "$pyinstaller" -w -i ./$product/resources/icon_64x64_$productlow.ico "$productlow.py"
mv "$tmpdir/dist/$productlow"/* "$builddir/app"
cp -r "$pildir" "$apidir" "$builddir/app"
# Tesh launch
cd "$builddir/app"
wine ./$productlow.exe&
# Update the archive
read -p "Update the archive? (y/n) " choice
if [ "$choice" = "n" ] || [ "$choice" = "N" ]; then
    exit;
fi
rm -f "$binariesdir/$product/$productlow-win32.7z"
7z a "$binariesdir/$product/$productlow-win32.7z" "$builddir"
rm -rf "$tmpdir"
