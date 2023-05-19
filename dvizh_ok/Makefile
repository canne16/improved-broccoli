BIN_DIR := build
FLAGS := -shared -fPIC

all: dvizh_ok.so dvizh_ok_exec

dvizh_ok.so: dvizh_ok.c
	gcc $(FLAGS) dvizh_ok.c -o dvizh_ok.so

dvizh_ok_exec: dvizh_ok.c main.c
	gcc main.c -o dvizh_ok_exec -lm

clean:
	rm dvizh_ok.so
	rm dvizh_ok_exec
