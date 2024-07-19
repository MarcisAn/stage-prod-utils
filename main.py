from stupidArtnet import StupidArtnetServer
import time
import asyncio
import websockets

        
def crossfade(value1, value2, factor):
    """
    Crossfade between two numeric values.

    :param value1: The start value.
    :param value2: The end value.
    :param factor: The interpolation factor between 0 and 1.
                   0 returns value1, 1 returns value2, and 0.5 returns the midpoint.
    :return: The interpolated value.
    """
    if not 0 <= factor <= 1:
        raise ValueError("Factor must be between 0 and 1")

    return (1 - factor) * value1 + factor * value2

server = StupidArtnetServer()
 
universes_to_listen = [0,1,2,3]
light_count = 200

universes = [] 

for uninumber in universes_to_listen:
    universes.append(server.register_listener(uninumber))

async def hello():
    while True:
        uri = "ws://172.20.10.2:8765"
        async with websockets.connect(uri) as websocket:
            packet = []
            for lightindex in range(0, light_count*3):
                channel_index_with_overflow = lightindex
                if channel_index_with_overflow >= 511:
                    channel_index_with_overflow += 2
                universe = channel_index_with_overflow // 512
                address = channel_index_with_overflow % 512
                #print(universe, address)
                buffers = [server.get_buffer(universes[0]),server.get_buffer(universes[1]),server.get_buffer(universes[2]),server.get_buffer(universes[3])]
                if len(buffers[0]) + len(buffers[1]) +  len(buffers[2]) + len(buffers[3]) == 512  * 4:
                    val1 = buffers[universe][address]
                    val2 = buffers[universe+2][address]
                    #print(buffers[1][91])
                    final_value = crossfade(val1, val2, buffers[1][91] * (1/255))
                    packet.append(final_value)
            #print(str(packet))

            await websocket.send(str(packet))
                #print(len(buffer))


        #8765


if __name__ == "__main__":

    asyncio.run(hello())