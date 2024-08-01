from twitchAPI.twitch import Twitch
from twitchAPI.object.eventsub import ChannelFollowEvent, ChannelSubscribeEvent, ChannelCheerEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.helper import first

import asyncio
import requests

from decouple import config

APP_ID = config('APP_ID')
APP_SECRET = config('APP_SECRET')
TARGET_SCOPES = [AuthScope.MODERATOR_READ_FOLLOWERS, AuthScope.CHANNEL_READ_SUBSCRIPTIONS, AuthScope.BITS_READ]
TARGET_CHANNEL = config('TARGET_CHANNEL')
TARGET_USER = config('TARGET_USER')

backend_URL = config('BACKEND_HOST')

async def on_follow(data: ChannelFollowEvent):
    # our event happend, lets do things with the data we got!
    requests.post(f'http://{backend_URL}:8000/api/timer/test/')
    print(f'\n{data.event.user_name} now follows {data.event.broadcaster_user_name}!')
    print('-'*100)


async def on_subscription(data: ChannelSubscribeEvent):
    # our event happend, lets do things with the data we got!
    print(f'\n{data.event.user_name} now subscribes to {data.event.broadcaster_user_name}!')
    print(data.event)

    match data.event.tier:
        case '1000':
            print('Tier 1')
        case '2000':
            print('Tier 2')
        case '3000':
            print('Tier 3')
        case _:
            print('Prime')

    print('-'*100)

async def on_cheer(data: ChannelCheerEvent):
    # our event happend, lets do things with the data we got!
    print(f'\n{data.event.user_name} cheered {data.event.bits} bits to {data.event.broadcaster_user_name}!')
    print(data.event)
    print('-'*100)

async def run():
    # create the api instance and get user auth either from storage or website
    twitch = await Twitch(APP_ID, APP_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
    await helper.bind()


    # get the currently logged in user
    userB = await first(twitch.get_users(logins=[TARGET_CHANNEL]))
    userM = await first (twitch.get_users(logins=[TARGET_USER]))

    # create eventsub websocket instance and start the client.
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    # subscribing to the desired eventsub hook for our user
    # the given function (in this example on_follow) will be called every time this event is triggered
    # the broadcaster is a moderator in their own channel by default so specifying both as the same works in this example
    # We have to subscribe to the first topic within 10 seconds of eventsub.start() to not be disconnected.
    await eventsub.listen_channel_follow_v2(userB.id, userM.id, on_follow)
    await eventsub.listen_channel_subscribe(userB.id, on_subscription)
    await eventsub.listen_channel_subscription_gift(userB.id, on_subscription)
    await eventsub.listen_channel_cheer(userB.id, on_cheer)

    # eventsub will run in its own process
    # so lets just wait for user input before shutting it all down again
    try:
        input('press Enter to shut down...')
    except KeyboardInterrupt:
        pass
    finally:
        # stopping both eventsub as well as gracefully closing the connection to the API
        await eventsub.stop()
        await twitch.close()


asyncio.run(run())