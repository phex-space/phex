#!/bin/bash

export SCRIPT_HOME="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd ${SCRIPT_HOME}/public/assets/logo

svg=symbol.svg

size=(16 24 32 48 72 96 144 152 192 196 256 512)

echo Making bitmaps from your svg...

for i in ${size[@]}; do
  inkscape -o symbol-$i.png -w $i -h $i $svg
done

echo Compressing...

## Replace with your favorite (e.g. pngquant)
# optipng -o7 "$out/*.png"
pngquant -f --ext .png *.png --posterize 4 --speed 1

echo Converting to favicon.ico...

convert "*.png" ../../favicon.ico

echo Done