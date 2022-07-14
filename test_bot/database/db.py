from __future__ import annotations

from datetime import datetime

import aiomysql
from discord.ext import commands

from ..utils import TimeRecord
from .mysql_db import DatabaseModel

__all__ = (
    "UserDB",
    "TimeDB",
)


class UserDB(DatabaseModel):
    database_pool: aiomysql.Pool

    async def setup(self, bot: commands.Bot) -> None:

        self.database_pool = bot.database_pool
        await self.exec_write_query(
            "CREATE TABLE IF NOT EXISTS users(id BIGINT PRIMARY KEY)"
        )

    async def read(self, user_id: int) -> bool:
        c = await self.exec_fetchone("SELECT * FROM users WHERE id = %s", (user_id,))
        return True if c else False

    async def create(self, user_id: int) -> bool:
        _check = await self.read(user_id)
        if _check:
            return False
        await self.exec_write_query("INSERT INTO users(id) VALUES(%s)", (user_id,))

        return True

    async def delete(self, user_id: int) -> bool:
        _check = await self.read(user_id)
        if not _check:
            return False
        await self.exec_write_query("DELETE FROM users WHERE id = %s", (user_id,))
        return True


class TimeDB(DatabaseModel):
    async def setup(self, bot: commands.Bot) -> None:
        self.database_pool = bot.database_pool
        await self.exec_write_query(
            "CREATE TABLE IF NOT EXISTS userss(id BIGINT PRIMARY KEY, time TIMESTAMP, channel BIGINT)"
        )

    async def read(self, user_id: int) -> TimeRecord | None:

        rec = await self.exec_fetchone("SELECT * FROM userss WHERE id = %s", (user_id,))

        return TimeRecord(rec[0], rec[1], rec[2]) if rec is not None else None

    async def create(
        self, user_id: int, dt: datetime, channel: int
    ) -> TimeRecord | bool:
        _c = await self.read(user_id)
        if _c is not None:
            return False
        await self.exec_write_query(
            "INSERT INTO userss(id, time, channel) VALUES(%s, %s, %s)",
            (
                user_id,
                dt,
                channel,
            ),
        )
        return TimeRecord(user_id, dt, channel)

    async def delete(self, user_id: int) -> TimeRecord | bool:
        _c = await self.read(user_id)
        if _c is None:
            return False
        await self.exec_write_query("DELETE FROM userss WHERE id = %s", (user_id,))
        return TimeRecord(_c.user_id, _c.time, _c.channel_id)

    async def update(self, user_id: int, dt: datetime) -> TimeRecord | bool:
        _c = await self.read(user_id)
        if _c is None:
            return False
        await self.exec_write_query(
            "UPDATE SET time = %s WHERE id = %s",
            (
                dt,
                user_id,
            ),
        )
        return TimeRecord(_c.user_id, dt, _c.channel_id)

    async def all_records(self) -> list | None:
        s = await self.exec_fetchall("SELECT * FROM userss")
        if s is None:
            return None
        return [TimeRecord(record[0], record[1], record[2]) for record in s]
