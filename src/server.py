#coding:utf-8

import sys
import os
import getopt


def usage():
    print """usage: server.py -s service -i sid
    service - [ mas | mexs | mgws ]
    sid - [mgws_server | mexs_server ]
    """

if __name__ == '__main__':
    service_name = ''
    sid = ''
    options, args = getopt.getopt(sys.argv[1:], 'hs:i:', ['help', 'service=', 'config=','id='])  # : 带参数
    for name, value in options:
        if name in ['-h', "--help"]:
            usage()
            sys.exit()
        if name in ('-s', '--service'):
            service_name = value
        if name in ('-i','--id'):
            sid = value

    if not service_name or not sid:
        usage()
        sys.exit()

    service_name = service_name.lower()
    server = None
    if service_name == 'mgws':
        import mgws.server
        server = mgws.server

    if service_name =='mexs':
        import mexs.server
        server = mexs.server
    if service_name == 'mas':
        import mas.server
        server = mas.server

    if server:
        server.run(sid)


