#!/bin/bash

basename=$(cd  `dirname $0` ; pwd)

alias cp="cp -f"

python $TCE/tce2py.py -i koala.idl,gws.idl,mexs.idl -o ../koala/


cp ../koala/koala.py ../../src/sdk/python/libpushmessage_client/koala_imp.py

mv ../koala/koala.py ../koala/koala_impl.py


mkdir -p ../../src/sdk/java/lib/com/sw2us
python $TCE/tce2java.py -i koala.idl,gws.idl,mexs.idl -o ../../src/sdk/java/lib/com/sw2us -p com.sw2us

rm -f parser.out parsetab.py

#python $TCE/tce2js.py -i lemon.idl,tgs.idl,mexs.idl -o ../libs
#rm -f parser.out parsetab.py
