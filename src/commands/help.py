import discord
import datetime
from discord.ext import commands
from core.classes import Cog_ExtenSion
from lib.function import mustFieldEmbed, SendBGM
from lib.bot_config import ganyuCommands

class Help(Cog_ExtenSion):

    @commands.command()
    async def help(self, ctx):
        main_select = discord.ui.Select(
            placeholder="選擇要查看的指令清單",
            options=[
                discord.SelectOption(
                    label=" Ganyu help ",
                    value="ganyu",
                    description="查看指令清單",
                    emoji="🤖"
                ), discord.SelectOption(
                    label=" Fun ",
                    value="fun",
                    description="查看 Fun 指令清單",
                    emoji="🎉"
                ), discord.SelectOption(
                    label=" Info ",
                    value="info",
                    description="查看 Info 指令清單",
                    emoji="📘"
                ), discord.SelectOption(
                    label=" Cucmd ",
                    value="cmd",
                    description="查看Cucmd 指令清單",
                    emoji="📰"
                ), discord.SelectOption(
                    label=" Manage ",
                    value="manage",
                    description="查看 Manage 指令清單",
                    emoji="⚙️"
                ),
                discord.SelectOption(
                    label=" Tool ",
                    value="tool",
                    description="查看 Tool 指令清單",
                    emoji="🛠️"
                )
            ]
        )

        main_view = discord.ui.View(timeout=None)
        main_view.add_item(main_select)

        async def main_select_callback(interaction):

            await interaction.response.edit_message(
                embed=ganyuCommands[main_select.values[0]],
                view=main_view
            )

        main_select.callback = main_select_callback

        await ctx.send(
            embed=ganyuCommands["ganyu"],
            view=main_view
        )

        SendBGM(ctx)

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