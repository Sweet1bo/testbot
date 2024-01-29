from aiogram import Dispatcher
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str('TOKEN')
dp = Dispatcher()
