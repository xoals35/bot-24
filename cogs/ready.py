import discord, datetime, time
from discord.ext import commands
import asyncio
from urllib import request
import time
import random
import pickle
import warnings
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup


start_time = time.time()

class Test(commands.Cog, name="관리자"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"ready.py 에서 봇을 켰습니다.")
        

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command(pass_context=True)
    async def 업타임(self, ctx):
            current_time = time.time()
            difference = int(round(current_time - start_time))
            text = str(datetime.timedelta(seconds=difference))
            embed = discord.Embed(colour=0xc8dc6c)
            embed.add_field(name="업타임", value=text)
            embed.set_footer(text="<알파프리베이트>")
            try:
                await ctx.send(embed=embed)
            except discord.HTTPException:
                await ctx.send("현재 봇작동시간: " + text)

    @commands.command()
    async def 새총(self, ctx):
        await ctx.trigger_typing()

        randomNum = random.randrange(1, 4)
        if randomNum == 1:
            embed = discord.Embed(title="새총으로 새를 잡았어요!", description="정말 잘했어요!")
            await ctx.send(embed=embed)
        if randomNum == 2:
            embed = discord.Embed(title="으악!!", description="새총을 쏘았는데 늑대가 왔어요 얼른 도망쳐요!")
            await ctx.send(embed=embed)
        if randomNum == 3:
            embed = discord.Embed(title="새총을 쏘았어요!", description="새총을 쏘았더니 경찰이었어요 도망쳐요!")
            await ctx.send(embed=embed)

    @commands.command()
    async def covid(self, ctx):
            # 보건복지부 코로나 바이러스 정보사이트"
            covidSite = "http://ncov.mohw.go.kr/index.jsp"
            covidNotice = "http://ncov.mohw.go.kr"
            html = urlopen(covidSite)
            bs = BeautifulSoup(html, 'html.parser')
            latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[0][1:].split('.')
            statisticalNumbers = bs.findAll('span', {'class': 'num'})
            beforedayNumbers = bs.findAll('span', {'class': 'before'})

            #주요 브리핑 및 뉴스링크
            briefTasks = []
            mainbrief = bs.findAll('a',{'href' : re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
            for brf in mainbrief:
                container = []
                container.append(brf.text)
                container.append(covidNotice + brf['href'])
                briefTasks.append(container)
        # 통계수치
            statNum = []
        # 전일대비 수치
            beforeNum = []
            for num in range(7):
                statNum.append(statisticalNumbers[num].text)
            for num in range(4):
                beforeNum.append(beforedayNumbers[num].text.split('(')[-1].split(')')[0])

            totalPeopletoInt = statNum[0].split(')')[-1].split(',')
            tpInt = ''.join(totalPeopletoInt)
            embed = discord.Embed(title="Covid-19 바이러스 코리아 현황", description="",color=0x5CD1E5)
            embed.add_field(name="자료 출처 : 보건 복지부", value="http://ncov.mohw.go.kr/index.jsp", inline=False)
            embed.add_field(name="최신 데이터 재생 시간",value="해당 자료는 " + latestupdateTime[0] + "월 " + latestupdateTime[1] + "일 "+latestupdateTime[2] +" 자료입니다.", inline=False)
            embed.add_field(name="확진환자(누적)", value=statNum[0].split(')')[-1]+"("+beforeNum[0]+")",inline=True)
            embed.add_field(name="완치환자(격리해제)", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
            embed.add_field(name="치료중(격리 중)", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
            embed.add_field(name="사망", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
            embed.add_field(name="누적확진률", value=statNum[6], inline=True)
            embed.add_field(name="- 최신 브리핑 1 : " + briefTasks[0][0],value="Link : " + briefTasks[0][1],inline=False)
            embed.add_field(name="- 최신 브리핑 2 : " + briefTasks[1][0], value="Link : " + briefTasks[1][1], inline=False)
            embed.add_field(name="Covid-19 확진 현황봇", value= "개발자 | hacking-Defender#4202 | 공식 커뮤니티 서버초대 초드 | http://asq.kr/djCAi4inQNMaUc")
            embed.set_thumbnail(url="https://wikis.krsocsci.org/images/7/79/%EB%8C%80%ED%95%9C%EC%99%95%EA%B5%AD_%ED%83%9C%EA%B7%B9%EA%B8%B0.jpg")
            await ctx.send(embed=embed)

    

   

   
def setup(bot):
    bot.add_cog(Test(bot))