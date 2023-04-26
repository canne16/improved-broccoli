BIN_DIR := build
FLAGS := -shared -fPIC

all: dvizh_ok.so

dvizh_ok.so: dvizh_ok.c
	gcc $(FLAGS) dvizh_ok.c -o dvizh_ok.so

clean:
	rm dvizh_ok.so
