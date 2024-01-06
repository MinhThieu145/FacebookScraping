import discord
from discord.ext import commands, tasks

async def info(ctx):
    title = "Fridge"
    price = "200"
    location = "Hanoi"
    time = "23 hours ago"
    photo_link = "https://scontent.ftpf1-2.fna.fbcdn.net/v/t45.5328-4/331825286_5796994537017075_1953585859080300839_n.jpg?stp=c0.156.403.403a_dst-jpg_p403x403&_nc_cat=106&ccb=1-7&_nc_sid=c48759&_nc_ohc=dY7YYLymuvMAX-jj6HI&_nc_ht=scontent.ftpf1-2.fna&oh=00_AfBu-2Mtctl6ZWYtdn1C75gB4k9wLZPrCZIG6ccx_cSP5g&oe=64118452"
    
    return title, price, location, time, photo_link
