import asyncio
import os

import aiomysql
import discord
from discord.ext import commands
from dotenv import load_dotenv

from ..database import TimeDB, UserDB

load_dotenv()


class TestBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="a!",
            intents=discord.Intents.all(),
            help_command=None,
        )

    async def setup_hook(self) -> None:
        self.database_pool = await aiomysql.create_pool(
            host="sql6.freemysqlhosting.net",
            user="sql6505678",
            db="sql6505678",
            password="nh3Bk4hZzV",
            port=int("3306"),
            loop=asyncio.get_event_loop(),
            autocommit=False,
        )
        self.db = UserDB()
        self.time_db = TimeDB()
        await self.db.setup(self)
        await self.time_db.setup(self)
        [
            await self.load_extension(f"test_bot.extensions.{file[:-3]}")
            for file in os.listdir("test_bot/extensions")
            if file.endswith(".py") and not file.startswith("_")
        ]

    def run(self) -> None:
        super().run("OTY0NTQ0MTg3OTAxMDI2MzI0.YlmLxg.mQwZC9_UYJ3FiY2IumDFwW3AyUE")
