from discord.ext import commands
from lib.classes import CogExtension
from lib.functions import mustFieldEmbed, SendBGM
from lib.bot_config import ganyuCommands
from command_lib import help
import discord


class Help(CogExtension):
    @commands.command()
    async def help(self, ctx):
        await help.help(ctx)

    @commands.command()
    async def fun(self, ctx):
        await ctx.send(embed=ganyuCommands["fun"])
        SendBGM(ctx)

    @commands.command()
    async def info(self, ctx):
        await ctx.send(embed=ganyuCommands["info"])
        SendBGM(ctx)

    @commands.command()
    async def cucmd(self, ctx):
        await ctx.send(embed=ganyuCommands["cmd"])
        SendBGM(ctx)

    @commands.command()
    async def manage(self, ctx):
        await ctx.send(embed=ganyuCommands["manage"])
        SendBGM(ctx)

    @commands.command()
    async def tool(self, ctx):
        await ctx.send(embed=ganyuCommands["tool"])
        SendBGM(ctx)


def setup(bot):
    bot.add_cog(Help(bot))
