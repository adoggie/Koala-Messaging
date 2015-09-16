#!/bin/bash

basename=$(cd  `dirname $0` ; pwd)

python $TCE/tce2py.py -i koala.idl,gws.idl,mexs.idl -o ../

#mv ../service/desert.py ../service/desert_impl.py

rm -f parser.out parsetab.py

#python $TCE/tce2js.py -i lemon.idl,tgs.idl,mexs.idl -o ../libs
#rm -f parser.out parsetab.py
