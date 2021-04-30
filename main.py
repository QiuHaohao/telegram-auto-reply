#!/usr/bin/env python3
import time
import re
import json
import random
import os
from pprint import pprint
from string import Template

from telethon import TelegramClient, events, utils
from dotenv import load_dotenv

load_dotenv()

session = os.environ.get('TG_SESSION', 'printer')
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

client = TelegramClient(session, api_id, api_hash).start()

tmpl = None

with open("template.txt") as f:
  tmpl = Template("".join(f.readlines()))

idList = []

@client.on(events.NewMessage)
async def handle_new_message(event):
    dialogs = await client.get_dialogs()
    me = await client.get_me()
    from_user = await client.get_entity(event.from_id) 
    to_user = await client.get_entity(event.message.to_id)

    if event.is_private and not (from_user.is_self or from_user.bot):
      print(time.asctime(), '-', event.message)
      time.sleep(1)

      idList.append(to_user.id)

      if idList.count(to_user.id) <= 1:
        await event.reply(tmpl.substitute(from_handle=f"@{from_user.username}"))

client.start()
client.run_until_disconnected()
