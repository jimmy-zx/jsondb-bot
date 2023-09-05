import os
import logging
import json

import dotenv
import discord


class App:
    PREFIX = '$'

    def __init__(self, intents, regs = None) -> None:
        self.client = discord.Client(intents=intents)
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.logger = logging.getLogger('discord')
        self.regs: dict[int, list[str]] = regs or {}

    async def on_ready(self) -> None:
        self.logger.info(f'logged in as {self.client.user}')

    async def on_message(self, message) -> None:
        if message.author == self.client.user:
            return
        if not message.content.startswith(App.PREFIX):
            return
        self.logger.debug(f'message: {message.content}')
        cmd = message.content.split('$')[1]
        func = getattr(self, f'cmd_{cmd}', None)
        if func:
            await func(message)
            return
        await message.channel.send('Unknown message')


    async def cmd_ping(self, message):
        await message.channel.send('pong')

    async def cmd_reg(self, message):
        cmd = message.content.removeprefix(App.PREFIX)
        if not cmd.startswith('reg$'):
            await message.channel.send('Usage: reg$[data]')
            return
        try:
            data = cmd.removeprefix('reg$')
            json.loads(data)  # validate for valid json
            if message.author.id not in self.regs:
                self.regs[message.author.id] = []
            self.regs[message.author.id].append(data)
            await message.channel.send('registered')
        except ValueError:
            await message.channel.send('data is not valid json')

    async def cmd_dmping(self, message):
        await message.author.send('pong')

    async def cmd_check(self, message):
        await message.channel.send(json.dumps(self.regs.get(message.author.id, None)))

    async def cmd_dereg(self, message):
        del self.regs[message.author.id]
        await message.channel.send('de-registered')


if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    dbfile = os.getenv('DBFILE', 'data/regs.json')

    try:
        with open(dbfile, 'r') as f:
            regs = json.load(f)
    except FileNotFoundError:
        regs = {}

    intents = discord.Intents.default()
    intents.message_content = True
    app = App(intents, regs=regs)

    app.client.run(token)

    with open(dbfile, 'w') as f:
        json.dump(app.regs, f)
