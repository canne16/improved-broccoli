import time
import asyncio

FINISHED = False
pipe = open("fp_ser_eng", "r")

class Proto(asyncio.DatagramProtocol):
    def __init__(self):
        pass
    

    def connection_made(self, transport):
        self.transport = transport
        transport.sendto(f"initial".encode())

    def datagram_received(self, data, addr):
        result = data.decode()
        cmd = result.split()
        if cmd[0] == 'hello':
            print("HELLO recieved!")
        


async def step(transport, proto):
    ch = input()
    if ch == "start":
        transport.sendto(f"start".encode())
    if ch == "+w":
        transport.sendto(f"+w".encode())
    if ch == "-a":
        transport.sendto(f"-a".encode())
    if ch == "+s":
        transport.sendto(f"+s".encode())
    if ch == "+d":
        transport.sendto(f"+d".encode())
    s = pipe.readline()
    if s != "":
        print(s, end="")

async def main():

    global pipe
    
    loop = asyncio.get_running_loop()
    transport, proto = await loop.create_datagram_endpoint(Proto, remote_addr=('127.0.0.1', '8787'))

    while not FINISHED:
        if await step(transport, proto) == 0:
            break
        await asyncio.sleep(2)
    transport.close()

asyncio.run(main())

pipe.close()