from fastapi import FastAPI, Depends
from app.schema import Query
from app.api_key_auth import get_api_key
from app.gpt import GPT
from config import get_settings
import discord
from discord.ext import commands
import asyncio
import logging

settings = get_settings()

intents = discord.Intents.default()
intents.message_content = True


app = FastAPI()
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = settings.discord_bot_token


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!pyhand'):
        result = GPT.get_answer(message.content[:])
        await message.reply(result)

async def run_discord_bot():
    await bot.start(TOKEN)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_discord_bot())

@app.post("/query")
async def get_the_answer(query: Query, api_key: str = Depends(get_api_key)):
    return {"response": GPT.get_answer(query.query, query.thread_id)}
