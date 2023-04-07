#include <stdlib.h>
#include <stdio.h>
#include <uv.h>
#include <string.h>

uv_loop_t *loop;        //  цикл для обработки событий
uv_udp_t recv_socket;   //  
uv_timer_t game_tick;   //  тикрейт получения и отправки сообщений сервера (=engine_tick??)


typedef struct _client_list {
    struct sockaddr_in addr;
    uv_buf_t buf;
    struct _client_list* next;
} client_t;


typedef struct _game {
	uv_udp_t server;
	client_t* clients;
} game_t;


game_t game;


void add_client(const struct sockaddr* addr) {
	client_t* client;
	for( client = game.clients; client; client = client->next) {
		if ( !memcmp(addr, &client->addr, sizeof(struct sockaddr_in)) ) {
			printf("Client found\n");
			return;
		}
	}
	client = malloc(sizeof(client_t));
	client->addr = *(const struct sockaddr_in*)addr;
	printf("Adding client with port %d\n", client->addr.sin_port);
	client->buf = uv_buf_init(malloc(1024), 1024);
	client->next = game.clients;
	game.clients = client;
}


void on_read(uv_udp_t* req, ssize_t nread, const uv_buf_t* buf,
		const struct sockaddr* addr, unsigned flags) {
	char temp[1024];
	int a, b, c;
	if ( nread > 0 ) {
		printf("data got: %s\n", buf->base);
		if (strncmp(buf->base, "DIM", 3) == 0) {
			printf("adding new client\n");
			add_client(addr);
		/*} else if ( strncmp(buf->base, "INC", 3) == 0) {
			move_rocket(1);
		} else if ( strncmp(buf->base, "DEC", 3) == 0) {
			move_rocket(-1);
		} else if ( !strncmp(buf->base, "EXIT", 4) ) {
			remove_client(addr);*/
		}
	} else if ( nread == 0 ) {
		printf("Empty data got\n");
	} else {
		printf("Error %s\n", uv_err_name(nread));
	}
	free(buf->base);
}


void on_send(uv_udp_send_t* req, int status) {
	printf("Send done %p with status %d %s\n", req->handle, status, uv_err_name(status));
	free(req);	
}


void on_timer(uv_timer_t* timer){
    //printf("Timer....\n");
    

}


int main(){
    struct sockaddr_in recv_addr;

    loop = uv_default_loop();
    uv_udp_init(loop, &recv_socket);
    uv_timer_init(loop, &game_tick);
    uv_ip4_addr("127.0.0.1", 8787, &recv_addr);
    uv_udp_bind(&recv_socket, (const struct sockaddr*)&recv_addr, UV_UDP_REUSEADDR);
    uv_timer_start(&game_tick, on_timer, 100, 70);

    printf("Server started\n");
    uv_run(loop, UV_RUN_DEFAULT);

}