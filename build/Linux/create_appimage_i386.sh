#!/bin/bash

product="Yatube"
productlow='yatube'
arch="i686"
os="Linux" # Linux or Wine
oslow="linux"
# oldstable debian has glibc 2.19, whereas current stable debian has glibc 2.24
glibc="2.19"
binariesdir="$HOME/binaries"
appimagedir="$binariesdir/appimage"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
tmpdir="/tmp/$product"   # Will be deleted!
builddir="$tmpdir/build" # Will be deleted!
pildir="/usr/lib/python3/dist-packages/PIL"

export "ARCH=$arch"

if [ "`which pyinstaller`" = "" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -d "$pildir" ]; then
    echo "Folder $pildir does not exist!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$appimagedir" ]; then
    echo "Folder $appimagedir does not exist!"; exit
fi

if [ ! -d "$srcdir" ]; then
    echo "Folder $srcdir does not exist!"; exit
fi

if [ ! -d "$resdir" ]; then
    echo "Folder $resdir does not exist!"; exit
fi

if [ ! -e "$appimagedir/AppRun-$arch" ]; then
    echo "File $appimagedir/AppRun-$arch does not exist!"; exit
fi

if [ ! -e "$appimagedir/appimagetool-$arch.AppImage" ]; then
    echo "File $appimagedir/appimagetool-$arch.AppImage does not exist!"; exit
fi

if [ ! -e "$HOME/bin/$product/build/$os/$productlow.desktop" ]; then
    echo "File $HOME/bin/$product/build/$os/$productlow.desktop does not exist!"; exit
fi

if [ ! -e "$HOME/bin/$product/build/$os/$productlow.png" ]; then
    echo "File $HOME/bin/$product/build/$os/$productlow.png does not exist!"; exit
fi

# Build with pyinstaller
rm -rf "$tmpdir"
mkdir -p "$builddir" "$tmpdir/app/usr/bin" "$tmpdir/app/resources"
cp -r "$srcdir"/* "$builddir"
cp -r "$resdir" "$tmpdir/app/usr"
cp -r "$resdir/locale" "$tmpdir/app/resources/"
cp -r "$pildir" "$tmpdir/app/usr/bin"
cd "$builddir"
pyinstaller "$productlow.py"
# Create AppImage
mv "$builddir/dist/$productlow"/* "$tmpdir/app/usr/bin"
cd "$tmpdir/app"
cp "$appimagedir/AppRun-$arch" "$tmpdir/app/AppRun"
cp "$appimagedir/appimagetool-$arch.AppImage" "$tmpdir"
cp "$HOME/bin/$product/build/$os/$productlow.desktop" "$tmpdir/app"
cp "$HOME/bin/$product/build/$os/$productlow.png" "$tmpdir/app"
cd "$tmpdir"
./appimagetool-$arch.AppImage app
read -p "Update the AppImage? (Y/n) " choice
if [ "$choice" = "n" ] || [ "$choice" = "N" ]; then
    exit;
fi
# The tool is i686, but creates i386
mv -fv "$tmpdir/$product-i386.AppImage" "$HOME/binaries/$product/$productlow-$oslow-i386-glibc$glibc.AppImage"
rm -rf "$tmpdir"
