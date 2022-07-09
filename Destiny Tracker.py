## Destiny Tracker

import pydest
import asyncio

async def Main():
    destiny = pydest.Pydest("APIKEY")
    json = await destiny.api.search_destiny_player(1, 'Acer, Topper of Laps')
    print(json)
    await destiny.close()

if __name__ == "__main__":
    Main()