#include <stdlib.h>
#include <stdio.h>
#include <uv.h>
#include <string.h>
#include "server.h"

#define STR_BUFFER 256

int send_pos();


uv_loop_t *loop;        //  цикл для обработки событий
uv_udp_t recv_socket;   //  
uv_udp_t send_socket;
uv_timer_t game_tick;   //  тикрейт получения и отправки сообщений сервера (=engine_tick??)

FILE* fp_in; // reading pipe
FILE* fp_out; // writing pipe
int NPlayers;
double x, y;
double vx, vy;

char* POS;


typedef struct _client_list {	//	односвязный список
    struct sockaddr_in addr;	//	адрес, откуда приходят пакеты
    uv_buf_t buf;				//	буфер содержит адрес получателя, отправителя, число бит и данные
    int index;
	struct _client_list* next;
} client_t;

typedef struct _game {		//	объект игры ( + uv_udp_t engine )
	uv_udp_t server;
	client_t* clients;
} game_t;

game_t game;	//	создание игры


/// @brief обработчик подключения нового играка
/// @param addr	адрес игрока, от которого пришел пакет

void add_client(const struct sockaddr* addr) {
	client_t* client; 
	for( client = game.clients; client; client = client->next) {			//	проверка, что игрок с этим адресом еще не добавлен
		if ( !memcmp(addr, &client->addr, sizeof(struct sockaddr_in)) ) {	//
			printf("Client found\n");										//
			return;
		}
	}
	client = malloc(sizeof(client_t));									//	Добавляем пользователя в список, выделяем 
	client->addr = *(const struct sockaddr_in*)addr;					//	память, присваиваем адрес и индивидуальный буфер
	printf("Adding client with port %d\n", client->addr.sin_port);		//
	char* s = malloc(17);
	printf("Client address: %s\n", get_ip_str(&client->addr, s, 17));	//
	client->buf = uv_buf_init(malloc(1024), 1024);	
	client->index = NPlayers;											//	Номер клиента = номер управляемого объекта
	NPlayers += 1;			
	client->next = game.clients;										//
	game.clients = client;												//
}


/// @brief обработчик получения пакета
/// @param req UDP request handle. Need not be initialized
/// @param nread число полученных байт
/// @param buf пакет полученных данных
/// @param addr адрес игрока, от которого пришел пакет
/// @param flags какие-то флаги

void on_read(uv_udp_t* req, ssize_t nread, const uv_buf_t* buf,	const struct sockaddr* addr, unsigned flags) {
	//	char temp[1024];	//	временный буфер

	if ( nread > 0 ) {	//	если при получении не было ошибок и пакет не пустой
		printf("data got: %s\n", buf->base);	//	buf->base == содержимое пакета без адреса и прочего
		if (strncmp(buf->base, "initial", 7) == 0) {	//	команда NEW == запрос на подключение к игре
			printf("Adding new client\n");
			add_client(addr);
		
		//	Обработка других команд или данных пользователя
		} else if ( strncmp(buf->base, "+w", 2) == 0) {
			//fprintf(fp_out, "SET VY %f\n", 1.0);
			vy = 2;
		} else if ( strncmp(buf->base, "-w", 2) == 0) {
			//fprintf(fp_out, "SET VY %f\n", 0.0);
			vy = 0;
		} else if ( strncmp(buf->base, "+a", 2) == 0) {
			//fprintf(fp_out, "SET VX %f\n", -1.0);
			vx = -2;
		} else if ( strncmp(buf->base, "-a", 2) == 0) {
			//fprintf(fp_out, "SET VX %f\n", 0.0);
			vx = 0;
		} else if ( strncmp(buf->base, "+s", 2) == 0) {
			//fprintf(fp_out, "SET VY %f\n", -1.0);
			vy = -2;
		} else if ( strncmp(buf->base, "-s", 2) == 0) {
			//fprintf(fp_out, "SET VY %f\n", 0.0);
			vy = 0;
		} else if ( strncmp(buf->base, "+d", 2) == 0) {
			//fprintf(fp_out, "SET VX %f\n", 1.0);
			vx = 2;
		} else if ( strncmp(buf->base, "-d", 2) == 0) {
			//fprintf(fp_out, "SET VX %f\n", 0.0);
			vx = 0;
		} else if ( strncmp(buf->base, "start", 5) == 0) {
			//start_engine();
		} else if ( nread == 0 ) {	//	получили пустой пакет
		//	printf("Empty data got\n");
		} else {
			//printf("Error %s\n", uv_err_name(nread));
		}
		//fflush(fp_out);
		
		//send_pos();
		free(buf->base);	//	необходимо самостоятельно очищать буфер
	}
}


/// @brief обработчик отправки пакета
/// @param req UDP send request type.
/// @param status ??

void on_send(uv_udp_send_t* req, int status) {
	//printf("Send done %p with status %d %s\n", req->handle, status, uv_err_name(status));
	free(req);	
}


/// @brief обработчик событий таймера
/// @param timer - указатель на таймер, события которого обрабатываются

void on_timer(uv_timer_t* timer){
	printf("KJAHKGFD\n");
	fflush(stdout);
	fprintf(fp_out, "end\n");
	fprintf(fp_out, "begin\n");
	//POS = get_pos();
		fflush(fp_out);

	get_pos();
	send_pos(POS);
	fprintf(fp_out, "add 0 x -1\n");
	fflush(fp_out);
}


void get_pos(){
		//char c;
		//printf("AAAAAAbobus\n");
		//fflush(stdout);
		//fscanf(fp_in, "%c", &c);
		//printf("%c\n", c);
		//printf("AAAAAAbobus\n");
		//fflush(stdout);
	//fscanf(fp_in, "%[^\n]", input_string); 
	fgets(POS, 16000, fp_in);
	//fscanf(fp_in,"%s\n", POS);
	printf("%s\n", POS);
	//char c;
	//fscanf(fp_in, "%c", &c);
	//while (c != '\n')
	//{
	//	printf("%c", c);
	//}
	//printf("\n");
}


/// @brief аллокация памяти при необходимости (ответ на запрос при получении пакета)

void alloc_buffer(uv_handle_t* handle, size_t suggested_size, uv_buf_t* buf){
  	buf->base = malloc(suggested_size);
  	buf->len = suggested_size;
}


int send_pos(){
	client_t * client; 
	for (client=game.clients; client; client=client->next) {
		char addr[17] = {0};
		uv_ip4_name(&client->addr, addr, 16);
		printf("Sending pos to client %s:%d\n", addr, client->addr.sin_port);
		uv_udp_send_t* send_req = malloc(sizeof(uv_udp_send_t));
		
		client->buf.len = sprintf(client->buf.base, "%s", POS);
		printf("Buf: %s\n", client->buf.base);
		int err = uv_udp_send(send_req, &recv_socket, &client->buf, 1, (const struct sockaddr*)&client->addr, on_send);
		if ( err ) 
			printf("Send %p returned: %d %s\n", &recv_socket, err, uv_err_name(err));
	}
    
    return 0;
}

int start_engine(){
		char *data = "init\nbegin";
        fprintf(fp_out, "%s\n", data);
        fflush(fp_out);
}


int main(){
    loop = uv_default_loop();		//	создание цикла
    struct sockaddr_in recv_addr;	//	инициализация ардеса получения пакетов

	fp_out = fopen("fp_ser_eng", "w");
	fp_in = fopen("fp_eng_ser", "r");

	POS = malloc(16000);
	NPlayers = 0;
	start_engine();

	uv_udp_init(loop, &recv_socket);	//	привязка сокета к циклу
    uv_timer_init(loop, &game_tick);	//	привязка таймера к циклу
    uv_ip4_addr("127.0.0.1", 8787, &recv_addr);	//	задание адреса
    uv_udp_bind(&recv_socket, (const struct sockaddr*)&recv_addr, UV_UDP_REUSEADDR);	//	настройка UDP
    uv_timer_start(&game_tick, on_timer, 100, 50);
	uv_udp_recv_start(&recv_socket, alloc_buffer, on_read);

	printf("Server started\n");	
	return uv_run(loop, UV_RUN_DEFAULT);


}