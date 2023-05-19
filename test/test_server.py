#!venv/bin/python3
import asyncio
from random import randint
from time import sleep

n = 0

class Circle:
    def __init__(self, x, y, r, vx, vy):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy

circles = []

class Client:
    def __init__(self, transport, address):
        self.transport = transport
        self.address = address

class PingPongProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, address):
        global circles
        global n
        msg = data.decode()
        print(f"recieved: {msg}")
        words = msg.split()
        if words[0] == "initial":
            self.transport.sendto(("{watching_keys: ['rmb'], figure_number: " + str(len(circles)) + "}").encode(), address)
            circles.append(Circle(500 + randint(-200, 200), 250 + randint(-100, 100), 50 + randint(-10, 10), randint(-2, 2), randint(-2, 2)))

        elif msg == "get_pos":
            answer = "{circles: ["
            for circle in circles:
                if (circle != circles[0]):
                    answer += ", "
                answer += "{" + f"x: {circle.x}, y: {circle.y}, r: {circle.r}, vx: {circle.vx}, vy: {circle.vy}" + ", requests: " + str(n)
                n += 1
            answer += "], polygons: []}"
            print(answer)

            self.transport.sendto(answer.encode(), address)

        elif msg == "update_pos":
            answer = "{circles: ["
            for circle in circles:
                if (circle != circles[0]):
                    answer += ", "
                answer += "{" + f"x: {circle.x}, y: {circle.y}, r: {circle.r}, vx: {circle.vx}, vy: {circle.vy}" + "}"
            answer += "], polygons: []}"
            print(answer)

            self.transport.sendto(answer.encode(), address)
        else:
            self.transport.sendto("Bad request".encode(), address)



async def main():
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(lambda: PingPongProtocol(),
            local_addr=('127.0.0.1', 9898))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()

    #async with server:
    #    await server.serve_forever()

asyncio.run(main())