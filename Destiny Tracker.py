import pydest
import asyncio


platforms = {'XBOX': 1, 'PLAYSTATION': 2, 'PC': 3}

async def main():
    destiny = pydest.Pydest('bc7717e228cd49e58ec26949bba34f51')

    platform = None
    while not platform:
        user_input = input('Enter your platform (xbox, playstation, or pc): ')
        if user_input.upper() in platforms.keys():
            platform = platforms.get(user_input.upper())
        else:
            print('Invalid platform.')

    username = input('Enter the username to locate: ')
    res = await destiny.api.search_destiny_player(platform, username)

    print(res)

    if res['ErrorCode'] == 1 and len(res['Response']) > 0:
        print("---")
        print("Player found!")
        print("Display Name: {}".format(res['Response'][0]['displayName']))
        print("Membership ID: {}".format(res['Response'][0]['membershipId']))
    else:
        print("Could not locate player.")

    await destiny.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
