#!/bin/bash 

function pyAll {
    find . -type f -name "*.py" | grep -v "11-organizing-files/selectivelyCopying/" | awk 'BEGIN {FS="/"} {print $NF}' | sort
    return
}

function py11 {
    find 11-organizing-files/selectivelyCopying/ -type f -name "*.py" | awk 'BEGIN {FS="/"} {print $NF}' | sort
    return
}

cd ..
rm -rf 11-organizing-files/selectivelyCopying/

cd 11-organizing-files/
python3 selectivelyCopying.py
cd ..

diff <(pyAll) <(py11)