BIN_DIR := build
FLAGS := -fPIC

all: server_exec dvizh_ok_exec fp_eng_ser fp_ser_eng

server_exec: ./server/server.c	
	gcc -I/usr/include/lua5.4 ./server/server.c -o server_exec -luv -llua || gcc -I/usr/include/lua5.4 ./server/server.c -o server_exec -luv -llua5.4

dvizh_ok_exec: ./dvizh_ok/dvizh_ok.c ./dvizh_ok/main.c
	gcc ./dvizh_ok/main.c -o dvizh_ok_exec -lm

clean:
	rm dvizh_ok_exec
	rm server_exec
	rm fp_eng_ser fp_ser_eng

fp_eng_ser:
	mkfifo fp_eng_ser 

fp_ser_eng:
	mkfifo fp_ser_eng