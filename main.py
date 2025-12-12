import asyncio
import httpx
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import json
import httpx



TELEGRAM_TOKEN = ""
RAGFLOW_API_KEY = ""

CHAT_ID = ""
RAGFLOW_BASE_URL = "https://api.swipies.app"

bot = Bot(token=TELEGRAM_TOKEN)
router = Router()
dp = Dispatcher()
dp.include_router(router)


async def swipies_request(text: str) -> str:
    url = f"https://api.swipies.app/api/v1/chats_openai/88584bb6d5fa11f0968c96bf0244a63a/chat/completions"

    headers = {
        "Authorization": "Bearer ragflow-Snlz91W1HWulWDc7K-Do0_JW0tqVL8lAFuz_LTnOfkU",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": text}],
    }

    async with httpx.AsyncClient(timeout=50.0) as client:
        r = await client.post(url, headers=headers, json=payload)
        raw_text = r.text

    result = ""
    for line in raw_text.splitlines():
        if line.startswith("data:"):
            chunk = line[len("data:"):].strip()
            if chunk == "[DONE]" or chunk == "":
                continue
            try:
                data = json.loads(chunk)
                delta = data["choices"][0]["delta"]
                content = delta.get("content")
                if content:
                    result += content
            except Exception:
                continue

    return result or "Swipies ai answered you"


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Send some message!")


@router.message()
async def message_handler(message: Message):
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await swipies_request(message.text)
    await message.answer(answer)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())