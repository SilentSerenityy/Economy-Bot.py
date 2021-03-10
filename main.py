import discord
from discord.ext import commands
import random
import json
import os

client = commands.Bot(command_prefix = "e!")

@client.event
async def on_ready():
  print("Ready")

@client.command()
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  wallet_amt = users[str(user.id)]["wallet"]
  bank_amt = users[str(user.id)]["bank"]

  em = discord.Embed(title = f"{ctx.author.name}'s balance")
  em.add_field(name = "Wallet balance",value = wallet_amt)
  em.add_field(name = "Bank balance",value = bank_amt)
  await ctx.send(embed = em)


@client.command()
async def beg(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author

  earnings = random.randrange(101)

  await ctx.send(f"Someone gave you {earnings} coins!!")

  users[str(user.id)]["wallet"] += earnings

  with open("mainbank.json", "w") as f:
    json.dump(users, f)

async def open_account(user):

  users = await get_bank_data()

  if str(user.id) in users:
    return False
  with open("mainbank.json","r") as f:
    users = json.load(f)
  
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0
  
  with open("mainbank.json", "w") as f:
    json.dump(users,f)
  return true

async def get_bank_data():
  with open("mainbank.json", "r") as f:
    users = json.load(f)
  return users
