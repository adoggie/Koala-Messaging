#!/bin/sh

#以下命令只能生成第一个idl的代码，后面的无法生成 ( bug ) .todo
# 路径不能带有 '.'
python $TCE/tce2js_requirejs.py -i ../../../../common/idl/koala.idl,../../../../common/idl/gws.idl,../../../../common/idl/mexs.idl -o ./scripts


rm -f parser.out parsetab.py
