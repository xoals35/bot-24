import discord
from discord import message
from discord.enums import _is_descriptor
from discord.ext import commands
import asyncio
import datetime
import random
import time
import sys
import json
import os
import discord as d
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import aiohttp
from captcha.image import ImageCaptcha
from discord.ext.commands import has_permissions, MissingPermissions
from youtube_search import YoutubeSearch
import youtube_dl
from random import choice
import math
import aiosqlite
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests



intents = discord.Intents.all()
bot = commands.Bot(command_prefix="ㅇ!", intents=intents)
bot.multiplier = 1


async def initialize():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("expData.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")



ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'downloads': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.id = data.get('id')
        self.uploader = data.get('uploader')
        self.uploaderid = data.get('uploader_id')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.event
async def on_ready(): #봇이 준비되었을때 뭐라고하기
    user = len(bot.users)
    server = len(bot.guilds)
    message = ["ㅇ!게임 ㅇ!유저, ㅇ!관리자 3개중 하나만 쳐봐요!",  str(user) + "유저와 함께해요!", str(server) + "개의 서버에 알파프리베이트가 같이운영해요!"]
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(message[0]))
        message.append(message.pop(0))
        await asyncio.sleep(4)




@bot.command() 
async def 안녕(ctx):
	await ctx.send("그래 안녕!")



@bot.command(aliases=['청소'])
@commands.has_permissions(administrator=True)
async def clear(ctx, l: int = 50):
   c = await ctx.channel.purge(limit=l)
   await ctx.send(f"`{len(c)}` 개의 메세지를 삭제했습니다.", delete_after=3)
   





@bot.command()
async def 밴(ctx, user: discord.User):
	guild = ctx.guild
	mbed = discord.Embed(
		title = '처리 완료',
		description = f"{user}님이 밴을 당하셨어요!"
	)
	if ctx.author.guild_permissions.ban_members:
		await ctx.send(embed=mbed)
		await guild.ban(user=user)

@bot.command()
async def 언밴(ctx, user: discord.User):
	guild = ctx.guild
	mbed = discord.Embed(
		title = '처리완료',
		description = f"{user}님을 언밴 했어요!"
	)
	if ctx.author.guild_permissions.ban_members:
		await ctx.send(embed=mbed)
		await guild.unban(user=user)

@bot.command()
@commands.has_permissions(kick_members=True)
async def 킥(ctx, member:discord.Member):
    await member.kick()
    await ctx.send(f"{member.name}님을 킥했습니다.")

@bot.command(name="뮤트")
@commands.has_permissions(manage_messages=True)
async def mute(ctx , member: discord.Member, *, reason=None):
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")

	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")

		for channel in guild.channels:
			await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

	await member.add_roles(mutedRole, reason=reason)
	await ctx.send(f"뮤트 {member.mention} 사유: {reason}으로 뮤트를 먹으셨습니다.")
	await member.send(f"뮤트 {member.mention} 사유: {reason}으로 뮤트를 먹으셨습니다.")


@bot.command(name="언뮤트")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	
			

	await member.remove_roles(mutedRole)
	await ctx.send(f"언뮤트 {member.mention}님이 언뮤트를 당하셨습니다.")
	await member.send(f"언뮤트 {member.mention}님이  언뮤트를 당하셨습니다.")






 
@bot.command(aliases = ['세이','메세지'])
async def say(ctx,*,message):
    emb=discord.Embed(title="say", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    
   

                 
@bot.command()
@commands.has_role("💎AC ▪ MASTER💎")
async def 경품(ctx, mins : int, * , prize: str):
	embed = discord.Embed(title = "상품!", description = f"{prize}", color = ctx.author.color)

	end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)

	embed.add_field(name = "종료 시간:", value = f"{end} UTC")
	embed.set_footer(text = f"지금부터 {mins}분 후 Emds")

	my_msg = await ctx.send(embed = embed)

	await my_msg.add_reaction("🎉")

@bot.command()
async def 리로드(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded extension: {extension}.")

@bot.command()
async def 언로드(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded extension: {extension}.")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command(aliases = ['ㅊㄴㅈㄱ'])
async def 채널제거(ctx, channel: d.TextChannel):
	mbed = d.Embed(
		title = '완료!',
		description = f'{channel}이라는 채널을 삭제했습니다.',
	)
	if ctx.author.guild_permissions.manage_channels:
		await ctx.send(embed=mbed)
		await channel.delete()


@bot.command(aliases = ['ㅊㄴㅅㅅ'])
async def 채널생성(ctx, channelName):
	guild = ctx.guild

	mbed = d.Embed(
		title = '완료!',
		description = "{}이라는 채널을 성공적으로 생성되었습니다.".format(channelName)
	)
	if ctx.author.guild_permissions.manage_channels:
		await guild.create_text_channel(name='{}'.format(channelName))
		await ctx.send(embed=mbed)
		
		
@bot.command(aliases = ['ㄸㄹㅎ'])
async def 따라해(ctx, *, text):
    await ctx.send(text)



@bot.command(pass_context=True)
async def 역할부여(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{user.name}님한테 **{role.name}**역할을 추가했어요!")

@bot.command(pass_context=True)
async def 역할제거(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{user.name}님한테 **{role.name}**역할을 제거했어요!")

@bot.command()
async def 유튜브(ctx):
    embed = discord.Embed(colour=0x95efcc, title=f"알파캡틴유튜브")
    await ctx.send(embed=embed)
    await ctx.send('https://www.youtube.com/user/cho090501')
    
@bot.command()
async def 레일건사기템존(ctx):
    embed=discord.Embed(title='이거 눌러보셈 ㅋㅋㅋㅋㅋㅋㅋ', description = "레일건 사기템존님은?\n잼민티 내고 이상하고 병신임 이거 이욕해도됌 제목눌러보셈", color = 0xff0000, url = "https://www.youtube.com/watch?v=K51gdMm3wWM")
    embed.set_footer(text = "와 니애미 욕은 해도됌 이사람한테는 (?)")
#출처: https://tercomgame.tistory.com/138 [단순한.]
    await ctx.send(embed=embed)






@bot.command(name="관리자")
async def help2(ctx):
        embed = discord.Embed(title="관리자 명령어", color=0x20ff05)
        embed.add_field(name="ㅇ!밴", value="ㅇ!밴 (밴하고싶은사람 맨션) 사유", inline=False) 
        embed.add_field(name="ㅇ!언밴", value="ㅇ!언밴 (차단된 사람 아이디)", inline=False)
        embed.add_field(name="ㅇ!뮤트", value="ㅇ!뮤트 (뮤트하고싶은사람 맨션) 사유", inline=False) 
        embed.add_field(name="ㅇ!언뮤트", value="ㅇ!언뮤트 (언뮤트하고싶은사람 맨션)", inline=False) 
        embed.add_field(name="ㅇ!채널생성", value="ㅇ!채널생성 (생성할 채널이름)", inline=False) 
        embed.add_field(name="ㅇ!채널제거", value="ㅇ!채널제거 (제거할 채널이름)", inline=False) 
        embed.add_field(name="ㅇ!역할부여", value="ㅇ!역할부여 (역할부여할 사용자 맨션) (부여할 역할 맨션)", inline=False) 
        embed.add_field(name="ㅇ!역할제거", value="ㅇ!역할제거 (역할제거할 사용자 맨션) (제거할 역할 맨션)", inline=False) 
        embed.add_field(name="ㅇ!킥", value="ㅇ!킥 (킥하고싶은사람 맨션)", inline=False) 
        await ctx.send(embed=embed)

@bot.command(name="유저")
async def help1(ctx):
        embed = discord.Embed(title="유저 명령어", color=0x20ff05)
        embed.add_field(name="ㅇ!레벨", value="ㅇ!레벨 자신의 레벨확인이 가능함", inline=False) 
        embed.add_field(name="ㅇ!핑", value="핑을 보여줍니다.", inline=False)
        embed.add_field(name="ㅇ!청소", value="ㅇ!청소 (메세지를 삭제할 수)", inline=False) 
        embed.add_field(name="ㅇ!유튜브", value="배그 AC클랜 서버장 유튜브 채널", inline=False) 
        embed.add_field(name="ㅇ!레일건사기템존", value="이상한 거임", inline=False) 
        await ctx.send(embed=embed)
   






@bot.event
async def on_member_join(member):
    await member.guild.system_channel.send(f'{member.mention}님이 들어오셨습니다')

@bot.event
async def on_member_remove(member):
    await member.guild.system_channel.send(f'{member.mention}님이 나가셨습니다')




@bot.command()
async def 입장(msg,*,channel:discord.VoiceChannel = None):
    if channel == None:
        channel = msg.author.voice.channel
    if msg.voice_client is not None:
        await msg.voice_client.move_to(channel)
    else:
        await channel.connect()

@bot.command()
async def 퇴장(msg):
    await msg.voice_client.disconnect()

@bot.command() #재생
async def 재생(ctx, *, url):
    async with ctx.typing():
        player = await YTDLSource.from_url(url)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    e = discord.Embed(title="재생 중!",description=player.title)
    e.set_image(url=f'https://i.ytimg.com/vi/{player.id}/hqdefault.jpg')
    await ctx.send(embed = e)
            
@bot.command(name="게임")
async def 게임(ctx):
    embed = discord.Embed(title="게임 도움말")
    embed.add_field(name="ㅇ!주사위", value="ㅇ!주사위 (숫자)", inline=False) 
    embed.add_field(name="ㅇ!새총", value="새총으로 게임을 해요!", inline=False) 
    await ctx.send(embed=embed)
   
@bot.command()
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' dm전송이 완료되었습니다.: " + target.name)

        except:
            await ctx.channel.send("지정된 사용자한테 dm을(를)할 수 없습니다.")
        

    else:
        await ctx.channel.send("사용자 ID 및 / 또는 메시지를 제공하지 않았습니다.")
 
@bot.event
async def on_message(message):
    if not message.author.bot:
        cursor = await bot.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1)) 

        if cursor.rowcount == 0:
            await bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            cur = await bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / bot.multiplier
        
            if lvl.is_integer():
                await message.channel.send(f"{message.author.mention} 축하합니다. 레벨업 하셨어요! \n`s!rank`로 자신에 정보를 확인해보세요!\n현재레벨: {int(lvl)}.")

        await bot.db.commit()

    await bot.process_commands(message)

@bot.command(aliases = ['ㄹㅋ', '랭킹'])
async def rank(ctx, member: discord.Member=None):
    if member is None: member = ctx.author

    # get user exp
    async with bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)) as cursor:
        data = await cursor.fetchone()
        exp = data[0]

        # calculate rank
    async with bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
        rank = 1
        async for value in cursor:
            if exp < value[0]:
                rank += 1

    lvl = int(math.sqrt(exp)//bot.multiplier)

    current_lvl_exp = (bot.multiplier*(lvl))**2
    next_lvl_exp = (bot.multiplier*((lvl+1)))**2

    lvl_percentage = ((exp-current_lvl_exp) / (next_lvl_exp-current_lvl_exp)) * 100

    embed = discord.Embed(title=f"통계 {member.name}", colour=discord.Colour.gold())
    embed.add_field(name="레벨", value=str(lvl))
    embed.add_field(name="경험치", value=f"현재경험치:{exp}/다음레벨까지 남은 경험치:{next_lvl_exp}")
    embed.add_field(name="랭크", value=f"{rank}위/{ctx.guild.member_count}")
    embed.add_field(name="다음 레벨까지", value=f"{round(lvl_percentage, 2)}% 남았습니다.")
    

    await ctx.send(embed=embed)

@bot.command(aliases = ['ㄹㄷㅂㄷ'])
async def 리더보드(ctx): 
    buttons = {}
    for i in range(1, 6):
        buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i # only show first 5 pages

    previous_page = 0
    current = 1
    index = 1
    entries_per_page = 10

    embed = discord.Embed(title=f"리더보드 페이지 {current}", description="", colour=discord.Colour.gold())
    msg = await ctx.send(embed=embed)

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        if current != previous_page:
            embed.title = f"리더보드 페이지{current}"
            embed.description = ""

            async with bot.db.execute(f"SELECT user_id, exp FROM guildData WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ", (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                index = entries_per_page*(current-1)

                async for entry in cursor:
                    index += 1
                    member_id, exp = entry
                    member = ctx.guild.get_member(member_id)
                    embed.description += f"{index}) {member.mention} : {exp}\n"

                await msg.edit(embed=embed)

        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            return await msg.clear_reactions()

        else:
            previous_page = current
            await msg.remove_reaction(reaction.emoji, ctx.author)
            current = buttons[reaction.emoji]



@bot.event 
async def on_member_join(member): # 방에 멤버가 들어왔을때
    date = datetime.datetime.utcfromtimestamp(((int(member.id) >> 22) + 1420070400000) / 1000)
    now = datetime.datetime.now()
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="닉네임", value=member.name, inline=True)
    embed.add_field(name="디스코드 가입일", value=str(date.year) + "년도" + str(date.month) + "월" + str(date.day) + "일",inline=True)
    embed.add_field(name="서버 가입일",value=str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second), inline=False)
    embed.add_field(name="입장인사",value=f"{member.name}님 저의 {member.guild}에 오신걸 환영합니다.", inline=False)
    embed.set_thumbnail(url=member.avatar_url)

    channel = bot.get_channel(id=806857560056922132) # id= 후에 채널 아이디을 넣으면 거기로 가짐
    await channel.send(embed=embed) # 임베트 출력

@bot.event 
async def on_member_remove(member): # 방에 멤버가 들어왔을때
    date = datetime.datetime.utcfromtimestamp(((int(member.id) >> 22) + 1420070400000) / 1000)
    now = datetime.datetime.now()
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="닉네임", value=member.name, inline=True)
    embed.add_field(name="디스코드 가입일", value=str(date.year) + "년도" + str(date.month) + "월" + str(date.day) + "일",inline=True)
    embed.add_field(name="서버 가입일",value=str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second), inline=False)
    embed.add_field(name="퇴장인사",value=f"{member.name}님이 저의 {member.guild}에서 퇴장 하셨어요 ㅠㅠㅠㅠ", inline=False)
    embed.set_thumbnail(url=member.avatar_url)

    channel = bot.get_channel(id=806857560056922132) # id= 후에 채널 아이디을 넣으면 거기로 가짐
    await channel.send(embed=embed) # 임베트 출력

@bot.command()
async def 시간(ctx):
    await ctx.send(embed=discord.Embed(title="현재시간", timestamp=datetime.datetime.utcnow()))

@bot.command(aliases=["주사위"])
async def roll(ctx, number:int):
    await ctx.sned(f"주사위 굴려서 {random.randint(1,int(number))}이(가) 나왔습니다. \n이 숫자는 (1~{number})중에 나온숫자 입니다.")
@roll.error
async def roll_error(ctx, error):
    await ctx.send("오류 발생 명령어를 잘못 치셨어요! \n원래명령어는 ㅇ!주사위 (숫자) 이에요")
    


@bot.command()
async def 핑(ctx):
    embed = discord.Embed(title="핑 측정중.......", color=0x00ff00)
    await ctx.send(embed=embed)
    time.sleep(3)
    embed = discord.Embed(title="핑 측정완료", description=f"{round(bot.latency * 1000)}ms 으로 측정되었습니다.", color=0x00ff00)
    await ctx.send(embed=embed)






bot.loop.create_task(initialize())
asyncio.run(bot.db.close())
access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
