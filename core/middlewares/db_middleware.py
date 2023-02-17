from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot_market_learn.core.others.db_request import Request


class DbSession(BaseMiddleware):
    def __init__(self, session_pool):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool.connection() as session:
            data['request'] = Request(session)
            return await handler(event, data)
