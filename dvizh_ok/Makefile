BIN_DIR := build
FLAGS := -shared -fPIC

all: dvizh_ok.so dvizh_ok_exec fp_eng_ser fp_ser_eng

dvizh_ok.so: dvizh_ok.c
	gcc $(FLAGS) dvizh_ok.c -o dvizh_ok.so

dvizh_ok_exec: dvizh_ok.c main.c
	gcc main.c -o dvizh_ok_exec -lm

clean:
	rm dvizh_ok.so
	rm dvizh_ok_exec
	rm fp_eng_ser fp_ser_eng

fp_eng_ser:
	mkfifo fp_eng_ser 

fp_ser_eng:
	mkfifo fp_ser_eng