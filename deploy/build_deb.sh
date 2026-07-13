#!/bin/bash

set -e

APP_NAME="cipher"
VERSION="2.0.0"

rm -rf build

mkdir -p build/${APP_NAME}/DEBIAN
mkdir -p build/${APP_NAME}/opt/${APP_NAME}
mkdir -p build/${APP_NAME}/usr/share/applications

cp -r . build/${APP_NAME}/opt/${APP_NAME}

cp deploy/cipher.desktop \
build/${APP_NAME}/usr/share/applications/

cat > build/${APP_NAME}/DEBIAN/control <<EOF
Package: cipher
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: all
Maintainer: Vasanth K
Description: Cipher Offline AI Assistant
EOF

dpkg-deb --build build/${APP_NAME}

echo "Build Complete"