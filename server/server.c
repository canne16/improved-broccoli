#include <stdlib.h>
#include <stdio.h>
#include <uv.h>
#include <string.h>
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>
#include "server.h"


#define STR_BUFFER 256
#define TICK 200
#define DELAY 1000



uv_loop_t *loop;        //  цикл для обработки событий
uv_udp_t recv_socket;   //  
uv_udp_t send_socket;
uv_timer_t game_tick;   //  тикрейт получения и отправки сообщений сервера (=engine_tick??)

FILE* fp_in; // reading pipe
FILE* fp_out; // writing pipe
int NPlayers = 0;

lua_State* Lua;

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
			break;
		}
	}
	client = malloc(sizeof(client_t));									//	Добавляем пользователя в список, выделяем 
	client->addr = *(const struct sockaddr_in*)addr;					//	память, присваиваем адрес и индивидуальный буфер
	char* s = malloc(17);
	printf("Client address: %s\n", get_ip_str(&client->addr, s, 17));	//
	client->buf = uv_buf_init(malloc(1024), 1024);	
	client->index = NPlayers;											//	Номер клиента = номер управляемого объекта
	NPlayers += 1;			
	client->next = game.clients;										//
	game.clients = client;		
	printf("Adding client with index %d\n", client->index);		//										//
}


/// @brief обработчик получения пакета
/// @param req UDP request handle. Need not be initialized
/// @param nread число полученных байт
/// @param buf пакет полученных данных
/// @param addr адрес игрока, от которого пришел пакет
/// @param flags какие-то флаги

void on_read(uv_udp_t* req, ssize_t nread, const uv_buf_t* buf,	const struct sockaddr* addr, unsigned flags) {
	if ( nread > 0 ) {	//	если при получении не было ошибок и пакет не пустой
		int index = 0;
		printf("data got: %s\n", buf->base);	//	buf->base == содержимое пакета без адреса и прочего
		if (strncmp(buf->base, "initial", 7) == 0) {	//	команда NEW == запрос на подключение к игре
			printf("Adding new client\n");
			add_client(addr);
		} else {
			client_t* client; 
			for( client = game.clients; client; client = client->next)
				if ( !memcmp(addr, &client->addr, sizeof(struct sockaddr_in)) )
					break;
			index = client->index;
			char* comm = calloc(2, sizeof(char));
			strncpy(comm, buf->base, 2);
			interpret(index, comm);
		}
		
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
	fprintf(fp_out, "end\n");
	fprintf(fp_out, "begin\n");
	fflush(fp_out);
	get_pos();
	send_pos(POS);
}


void get_pos(){
	fgets(POS, 4096, fp_in);
}

void interpret(int index, char* comm){
	lua_getglobal(Lua, "translate");
	lua_pushnumber(Lua, index);
	lua_pushstring(Lua, comm);
	lua_call(Lua, 2, 1);
	//printf("%s\n", lua_tostring(Lua, -1));
	fprintf(fp_out, "%s\n", lua_tostring(Lua, -1));
	lua_pop(Lua, 1);
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
		//printf("Sending pos to client %s:%d\n", addr, client->addr.sin_port);
		uv_udp_send_t* send_req = malloc(sizeof(uv_udp_send_t));
		
		client->buf.len = sprintf(client->buf.base, "%s", POS);
		//printf("Buf: %s\n", client->buf.base);
		int err = uv_udp_send(send_req, &recv_socket, &client->buf, 1, (const struct sockaddr*)&client->addr, on_send);
		if ( err ) 
			printf("Send %p returned: %d %s\n", &recv_socket, err, uv_err_name(err));
	}
    
    return 0;
}

void start_engine(){
		char *data = "init\nbegin";
        fprintf(fp_out, "%s\n", data);
        fflush(fp_out);
}


int main(){
    loop = uv_default_loop();		//	создание цикла
    struct sockaddr_in recv_addr;	//	инициализация ардеса получения пакетов

	fp_out = fopen("fp_ser_eng", "w");
	fp_in = fopen("fp_eng_ser", "r");

	POS = malloc(4096);
	
	Lua = luaL_newstate();
	luaL_openlibs(Lua);
	luaL_dofile(Lua, "./server/interpretator.lua");

	NPlayers = 0;
	start_engine();

	uv_udp_init(loop, &recv_socket);	//	привязка сокета к циклу
    uv_timer_init(loop, &game_tick);	//	привязка таймера к циклу
    uv_ip4_addr("127.0.0.1", 8787, &recv_addr);	//	задание адреса
    uv_udp_bind(&recv_socket, (const struct sockaddr*)&recv_addr, UV_UDP_REUSEADDR);	//	настройка UDP
    uv_timer_start(&game_tick, on_timer, DELAY, TICK);
	uv_udp_recv_start(&recv_socket, alloc_buffer, on_read);

	printf("Server started\n");	
	return uv_run(loop, UV_RUN_DEFAULT);

	fprintf(fp_out, "end\nexit\n");
	fclose(fp_in);
	fclose(fp_out);
	lua_close(Lua);
}