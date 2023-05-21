FLAGS := -shared -fPIC

all: dvizh_ok.so dvizh_ok_new.so

dvizh_ok.so: dvizh_ok.c
	gcc $(FLAGS) ./dvizh_ok.c -o dvizh_ok.so

dvizh_ok_new.so: dvizh_ok_new.c
	gcc $(FLAGS) ./dvizh_ok_new.c -o dvizh_ok_new.so
