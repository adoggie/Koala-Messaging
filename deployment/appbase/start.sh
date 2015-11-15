mkdir /home/koala
DEAMON=-d
docker run --name koala $DEAMON -it -v /home/koala:/opt -p 15432:5432 -p 37017:37017 -p 16379:6379 -p 15672:5672 -p 16001:16001 -p 80:80 -p 14001:14001 -p 14002:14002 koala:0.0.3 /run/start_koala.sh
