import time
import asyncio

FINISHED = False

class Proto(asyncio.DatagramProtocol):
    def __init__(self):
        pass
    

    def connection_made(self, transport):
        self.transport = transport
        transport.sendto(f"NEW".encode())

    

async def step(transport, proto):
    transport.sendto(f"DATA".encode())
    
    return 1

async def main():
    loop = asyncio.get_running_loop()
    transport, proto = await loop.create_datagram_endpoint(Proto, remote_addr=('127.0.0.1', '8787'))

    while not FINISHED:
        if await step(transport, proto) == 0:
            break
        await asyncio.sleep(1)
    transport.close()

asyncio.run(main())