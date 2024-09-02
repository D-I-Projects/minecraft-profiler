#!/bin/bash

install_quilt() {
    mkdir installer
    cd installer
    curl -L -o quilt-installer.jar https://quiltmc.org/api/v1/download-latest-installer/java-universal

    INSTALL_DIR=".."

    java -jar quilt-installer.jar install client 1.21 0.26.3 --install-dir="$INSTALL_DIR" --no-profile

    echo "Quilt installation is complete in $INSTALL_DIR!"
}

install_loader() {
    if [ "$1" == "quilt" ]; then
        install_quilt
    fi
}

# Aufruf der Funktion mit Parameter "quilt"
install_loader $1
