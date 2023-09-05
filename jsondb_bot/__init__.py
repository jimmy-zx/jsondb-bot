import logging
import json

import discord

__all__ = ['App']

class App:
    PREFIX = '$'

    def __init__(self, intents, regs = None) -> None:
        self.client = discord.Client(intents=intents)
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.logger = logging.getLogger('discord')
        self.regs: dict[str, list[str]] = regs or {}

        self.cmd: str = None
        self.userid: str = None
        self.message = None
        self.channel = None

    async def on_ready(self) -> None:
        self.logger.info(f'logged in as {self.client.user}')

    async def on_message(self, message) -> None:
        if message.author == self.client.user:
            return
        if not message.content.startswith(App.PREFIX):
            return
        self.cmd = message.content.split('$')[1]
        self.userid = str(message.author.id)
        self.message = message
        self.channel = message.channel
        func = getattr(self, f'cmd_{self.cmd}', None)
        if func:
            await func()
        else:
            await message.channel.send('Unknown message')
        self.cmd = None
        self.userid = None
        self.message = None
        self.channel = None


    async def cmd_ping(self):
        await self.channel.send('pong')

    async def cmd_reg(self):
        cmd = self.message.content.removeprefix(App.PREFIX)
        if not cmd.startswith('reg$'):
            await self.channel.send('Usage: reg$[data]')
            return
        try:
            data = json.loads(cmd.removeprefix('reg$'))
            if self.userid not in self.regs:
                self.regs[self.userid] = []
            self.regs[self.userid].append(data)
            await self.channel.send('registered')
        except ValueError:
            await self.channel.send('data is not valid json')

    async def cmd_dmping(self):
        await self.message.author.send('pong')

    async def cmd_check(self):
        await self.channel.send(json.dumps(self.regs.get(self.userid, None)))

    async def cmd_dereg(self):
        del self.regs[self.userid]
        await self.channel.send('de-registered')
