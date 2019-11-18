#!/usr/bin/env bash

function usage {
    echo "Creates certificates for CAs and for services. By default it creates web and kafka certs for consentmanager hgwfrontend hgwbackend. If you need other services specify them"
    echo "usage: ${0} [-s] [-h] [list of additional services]"
    echo " -o       specify output dir. If not present it will use the current dir"
    echo " -h       print this message"
}

if [ $# -ge 1 ]; then
    case "$1" in
        -h)
            usage
            exit 1
            ;;
        -o)
            if [ "$#" = 1 ]; then
                echo ERROR: Missing param for -o option
                exit 1
            fi
            OUTPUT_DIR=$2
            ;;
        -c|--clean)
            echo "Removing certs/ca"
            rm -rf certs/ca
            echo "certs/kafka"
            rm -rf certs/kafka
            echo "certs/root"
            rm -rf certs/root
            echo "certs/web"
            rm -rf certs/web
            echo "...done!"
    esac
fi

if [ ! -d "djangosaml2" ]; then
  git clone -b develop https://github.com/crs4/djangosaml2.git
fi

cd djangosaml2 && python3 setup.py install
cd ../certs

./generate_development.sh

mkdir -p ca/kafka/certs
sudo cp -r kafka/certs/* ca/kafka/certs
