import asyncio
import serial_asyncio


class SerialEchoServer(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print("Micro:bit virtuelle connectée !")
        self.send_fake_data()

    def data_received(self, data):
        print(f"Reçu du PC: {data.decode().strip()}")

    def send_fake_data(self):
        async def send():
            while True:
                self.transport.write(b"Temperature: 25C\n")
                await asyncio.sleep(2)  # Envoie des données toutes les 2 secondes

        asyncio.create_task(send())

async def main():
    loop = asyncio.get_event_loop()
    server = await serial_asyncio.create_serial_connection(loop, SerialEchoServer, 'COM25', baudrate=115200)
    await asyncio.sleep(100)

asyncio.run(main())
