#include <stdlib.h>
#include <stdio.h>
#include <uv.h>
#include <string.h>

uv_loop_t *loop;        //  цикл для обработки событий
uv_udp_t recv_socket;   //  
uv_timer_t game_tick;   //  тикрейт получения и отправки сообщений сервера (=engine_tick??)


typedef struct _client_list {	//	односвязный список
    struct sockaddr_in addr;	//	адрес, откуда приходят пакеты
    uv_buf_t buf;				//	буфер содержит адрес получателя, отправителя, число бит и данные
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
	client->buf = uv_buf_init(malloc(1024), 1024);						//
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
		if (strncmp(buf->base, "NEW", 3) == 0) {	//	команда NEW == запрос на подключение к игре
			printf("adding new client\n");
			add_client(addr);
		}
		/*
			Обработка других команд или данных пользователя
		
		} else if ( strncmp(buf->base, "INC", 3) == 0) {
			move_rocket(1);
		} else if ( strncmp(buf->base, "DEC", 3) == 0) {
			move_rocket(-1);
		} else if ( !strncmp(buf->base, "EXIT", 4) ) {
			remove_client(addr);
		*/
	} else if ( nread == 0 ) {	//	получили пустой пакет
		//	printf("Empty data got\n");
	} else {
		printf("Error %s\n", uv_err_name(nread));
	}
	free(buf->base);	//	необходимо самостоятельно очищать буфер
}


/// @brief обработчик отправки пакета
/// @param req UDP send request type.
/// @param status ??

void on_send(uv_udp_send_t* req, int status) {
	printf("Send done %p with status %d %s\n", req->handle, status, uv_err_name(status));
	free(req);	
}


/// @brief обработчик событий таймера
/// @param timer - указатель на таймер, события которого обрабатываются

void on_timer(uv_timer_t* timer){
    //printf("Tick....\n"); 
}


/// @brief аллокация памяти при необходимости (ответ на запрос при получении пакета)

void alloc_buffer(uv_handle_t* handle, size_t suggested_size, uv_buf_t* buf){
  	buf->base = malloc(suggested_size);
  	buf->len = suggested_size;
}


int main(){
    loop = uv_default_loop();			//	создание цикла
    struct sockaddr_in recv_addr;	//	инициализация ардеса получения пакетов

	uv_udp_init(loop, &recv_socket);	//	привязка сокета к циклу
    uv_timer_init(loop, &game_tick);	//	привязка таймера к циклу
    uv_ip4_addr("127.0.0.1", 8787, &recv_addr);	//	задание адреса
    uv_udp_bind(&recv_socket, (const struct sockaddr*)&recv_addr, UV_UDP_REUSEADDR);	//	настройка UDP
    uv_timer_start(&game_tick, on_timer, 100, 1000);
	uv_udp_recv_start(&recv_socket, alloc_buffer, on_read);

    printf("Server started\n");
    uv_run(loop, UV_RUN_DEFAULT);

}