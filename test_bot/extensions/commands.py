from datetime import datetime, timedelta
from typing import Optional

import discord
from discord.ext import commands, tasks

from ..main import TestBot


class Rem(commands.Cog):
    def __init__(self, bot: TestBot) -> None:
        self.bot = bot
        self.background_loop_new.start()

    @commands.command(name="reminder")
    async def reminder(self, ctx: commands.Context) -> Optional[discord.Message]:
        c = await self.bot.db.create(ctx.author.id)
        if c is False:
            await self.bot.db.delete(ctx.author.id)
            embed1 = discord.Embed(
                title="Drop Reminder",
                description="**Reminder for Drop:** OFF",
                color=0xED4337,
            )
            return await ctx.send(embed=embed1)
        embed2 = discord.Embed(
            title="Drop Reminder",
            description="**Reminder for Drop:** ON",
            color=0x3AA346,
        )
        await ctx.send(embed=embed2)

    @commands.Cog.listener("on_message")
    async def remo_on_message(self, message: discord.Message) -> None:
        if (
            message.author.id == 853629533855809596
            and "is dropping the cards" in message.content
        ):
            userId = int("".join([char for char in message.content if char.isdigit()]))
            c = await self.bot.db.read(userId)
            if c:
                await self.bot.time_db.create(
                    userId, datetime.now() + timedelta(minutes=8), message.channel.id
                )
                await message.add_reaction("👍")

    @tasks.loop(seconds=20)
    async def background_loop_new(self) -> None:
        await self.bot.wait_until_ready()

        all_records = await self.bot.time_db.all_records()
        for record in all_records:
            channel = self.bot.get_channel(
                record.channel_id
            ) or await self.bot.fetch_channel(record.channel_id)
            deltime = record.time + timedelta(seconds=21)
            if deltime >= datetime.now() >= record.time:
                await channel.send(f"<@{record.user_id}>, your drop cooldown is over.")
            elif datetime.now() >= deltime:
                await self.bot.time_db.delete(record.user_id)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandNotFound):
            return
        else:
            raise error


async def setup(bot: TestBot) -> None:
    await bot.add_cog(Rem(bot))
