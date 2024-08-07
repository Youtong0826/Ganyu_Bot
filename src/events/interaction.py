import random

from discord import (
    ActionRow,
    Button as DiscordButton,
    ButtonStyle,
    Cog,
    Colour,
    Embed,
    EmbedField,
    EmbedFooter,
    EmbedMedia,
    Interaction,
    InputTextStyle,
    SelectMenu,
)

from discord.ui import (
    View,
    Button,
    Modal,
    InputText,
)

from core import CogExtension
from lib.role import choose_role
from lib.timing import get_now_time
from lib.api import calculator
from lib.wiki import wiki_info

class InteractionEvent(CogExtension):
    @Cog.listener()
    async def on_interaction(self, interaction:Interaction):
        if interaction.is_command() or not interaction.custom_id: return

        user = interaction.user
        guild = interaction.guild
        custom_id = interaction.custom_id
        message = interaction.message
        components: list[ActionRow | DiscordButton | SelectMenu] = message.components if message else None
        
        if custom_id and "info" in custom_id and not "roleinfo" in custom_id:
            try: 
                original = list(filter(lambda x: x, [self.bot.from_component(c, "allinfo_select") for c in components]))[0]
            
            except IndexError:
                original = View()
            
            except Exception as ex:
                print(ex)
        
        if custom_id.endswith("ping"):
            if interaction.custom_id == "PA_ping":
                await choose_role(user, 962261741050413096)

            if interaction.custom_id == "Bu_ping":  
                await choose_role(user, 1009478887140511915)
                
            return await interaction.response.send_message(content=f"已成功變更身分組✅",ephemeral=True)
    
        if custom_id == "help_select":
            return await interaction.response.edit_message(embed=self.bot.commands_list[self.bot.get_select_value(interaction, 0)])
        
        if custom_id == "allinfo_select":
            match self.bot.get_select_value(interaction, 0):
                case "bot":
                    return await interaction.response.edit_message(**self.bot.get_bot_data(original))
                
                case "user":
                    return await interaction.response.edit_message(**self.bot.get_user_data(user, original))
                    
                case "server":
                    return await interaction.response.edit_message(**self.bot.get_guild_data(guild, original))
            
        if custom_id == "userinfo_moreinfo":
            return await interaction.response.edit_message(
                embed=Embed(
                    title=f"{user.name} 的個人資訊 ",
                    color=0x9c8ff,
                    timestamp=get_now_time(),
                    thumbnail=interaction.user.avatar,
                    fields=[
                        EmbedField(**i) for i in {
                            {"name": "🖥️ 驗證", "value": f"`{"未驗證" if user.pending else "已驗證"}`"},
                            {"name": "🔱 加成的時間", "value": f"`{user.premium_since if user.premium_since else "尚未加成"}`"},
                            {"name": "⚜️ 徽章數", "value": f"`{len(user.public_flags.all())}`"},
                        }
                    ]
                ),
                view=self.bot.merge_view(View(
                    Button(
                        style = ButtonStyle.primary,
                        label="back",
                        emoji= "🔙",
                        custom_id="userinfo_back"
                    )
                ), original)
            )
        
        if custom_id == "userinfo_back":
            return await interaction.response.edit_message(**self.bot.get_user_data(interaction.user, original))
        
        if custom_id == "serverinfo_moreinfo":
            robot = len(list(filter(lambda x: x.bot, guild.members)))
            return await interaction.response.edit_message(
                embed=Embed(
                    title=guild,
                    color=Colour.random(),
                    thumbnail=EmbedMedia(guild.icon.url),
                    footer=EmbedFooter("serverinfo | 伺服器資訊", self.bot.icon_url),
                    fields=[
                        EmbedField(**i) for i in [
                            {"name": "⚜️ __加成次數__", "value": guild.premium_subscription_count},
                            {"name": "🔱 __加成等級__", "value": guild.premium_tier},
                            {"name": "📈 __活人__", "value": guild.member_count-robot},
                            {"name": "📊 __機器人__", "value": robot},
                            {"name": "🐷 __表情符號(靜態)__", "value": len(list(filter(lambda x: x.animated, guild.emojis)))},
                            {"name": "🐸 __表情符號(動態)__", "value": len(list(filter(lambda x: not x.animated, guild.emojis)))},
                        ]
                    ]
                ), 
                view=self.bot.merge_view(View(
                    Button(
                        style=ButtonStyle.success,
                        emoji="🔙",
                        label="back",
                        custom_id="serverinfo_back"
                    ),
                    timeout=None  
                ), original)
            )
            
        if custom_id == "serverinfo_booster":
            return await interaction.response.edit_message(
                embed=Embed(
                    title=f"加成者們 [{len(guild.premium_subscribers)}]",
                    description='\n'.join(guild.premium_subscribers) if guild.premium_subscribers else "無",
                    color=Colour.random(),
                    thumbnail=EmbedMedia(guild.icon.url),
                    footer=EmbedFooter("serverinfo | 伺服器資訊", self.bot.icon_url),
                ), 
                view=self.bot.merge_view(View(
                    Button(
                        style=ButtonStyle.success,
                        emoji="🔙",
                        label="back",
                        custom_id="serverinfo_back"
                    ),
                    timeout=None 
                ), original)
            )
            
        if custom_id == "serverinfo_roles":
            count = 0
            roles = list(filter(lambda x: x.name != "@everyone", guild.roles))
            while sum(map(lambda x: len(x.mention)+3, roles)) >= 1014:
                count += 1
                roles.pop()

            roles = "無" if not roles else ' | '.join(map(lambda x: x.mention, roles))
            if count: roles += f" +{count} Roles..."
            
            return await interaction.response.edit_message(
                embed=Embed(
                    title=f"身分組 [{len(guild.roles)-1}]",
                    description=roles,
                    color=Colour.random(),
                    thumbnail=EmbedMedia(guild.icon.url),
                    footer=EmbedFooter("serverinfo | 伺服器資訊", self.bot.icon_url),
                ), 
                view=self.bot.merge_view(View(
                    Button(
                        style=ButtonStyle.success,
                        emoji="🔙",
                        label="back",
                        custom_id="serverinfo_back"
                    ),
                    timeout=None 
                ), original)
            )
            
        if custom_id == "serverinfo_back":
            return await interaction.response.edit_message(**self.bot.get_guild_data(guild, original))
        
        if custom_id == "open_report_button":
            await interaction.response.send_modal(Modal(
                InputText(
                    style=InputTextStyle.short,
                    label="名稱",
                    placeholder="此次回報的名稱"
                ),
                InputText(
                    style=InputTextStyle.long,
                    label="詳細敘述",
                    placeholder="此次回報的敘述",
                    max_length=1024
                ),
                title="機器人Bug回報表單",
                custom_id="report_modal"
            ))
        
        if custom_id == "report_modal":
            title, description = self.bot.get_interaction_value(interaction)
            #def bug_callback(title,description,modal,user):
            #    with open("Error report.txt","a",encoding="utf-8") as f:
            #        return f.write(f"\
            #            \n[{datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime('%Y/%m/%d %H:%M:%S')}]\
            #            \n----名稱: {title}\
            #            \n----詳細敘述: {description}\
            #            \n----提出者: {interaction.user}  id:{interaction.user.id}")

            report_embed = Embed(
                title=title,
                description=description,
                timestamp=get_now_time(),
                color=Colour.random(),
                footer=EmbedFooter(f"{user} 提出回報", user.avatar)
            )

            await self.bot.get_channel(966010451643215912).send(embed=report_embed)
            await user.send(embed=Embed(
                title=f"感謝您提出回報!!",
                description=f"以下為您的回報內容",
                color=Colour.random(),
                timestamp=get_now_time(),
                footer=EmbedFooter("Error report", self.bot.icon_url),
                fields=[
                    EmbedField("回報名稱:", title),
                    EmbedField("詳細敘述:", description)
                ]
            ))
            return await interaction.response.send_message(content=f"✅ 已成功提出回報，詳細內容請查看私訊", ephemeral=True)
        
        if custom_id == "wiki_select":
            value = self.bot.get_select_value(interaction, 0)
            await interaction.response.defer()
            description = wiki_info(value)
            #await sleep(1.5)
            return await interaction.followup.edit_message(
                message_id=message.id,
                embed=Embed(
                    url=f"https://zh.wikipedia.org/wiki/{value}",
                    title=value,
                    description=description,
                    color=Colour.random(),
                    timestamp=get_now_time(),
                    footer=EmbedFooter("Wikipedia.org", self.bot.icon_url),
                    thumbnail="https://th.bing.com/th/id/R.d451e7b1661d71fc68ca02b19137497b?rik=MjNkZivLBibrOQ&pid=ImgRaw&r=0"
                )
            )
        
        if custom_id.startswith("rpc_punch"):
            _, _, s = custom_id.split('_')
            result = random.choice(["r", "s", "p"])
            emoji = {
                "s": "✂️", "r": "🪨", "p": "🌫️"
            }
            
            if s == result:
                return await interaction.response.edit_message(content=f"我出 {emoji[result]} ，平手!")
            
            match s:
                case 's':
                    win = True if result == 'r' else False
                        
                case 'r':
                    win = True if result == 'p' else False
                
                case 'p':
                    win = True if result == 's' else False

            return await interaction.response.edit_message(content=f"我出 {emoji[result]} ，我贏了!" if win else f"我出 {emoji[result]} ，是我輸了...")
        
        if custom_id.startswith("roleinfo_owner"):
            role = list(filter(lambda x: x.id == int(custom_id.split('_')[2]), guild.roles))[0]
            members = role.members
            count = 0
            while (s := sum(map(lambda x: len(x.mention)+3, members))) >= 1010:
                count += 1
                members.pop()
                
            members = "無" if not role.members else ' | '.join(map(lambda x: x.mention, role.members))
            if count: members += f" +{count} Members..."

            return await interaction.response.edit_message(
                embed=Embed(
                    title=f"擁有此身分組的人",
                    description=members,
                    color=Colour.random()
                ), 
                view=View(
                    Button(
                        style=ButtonStyle.primary,
                        label="回去",
                        emoji="🔙",
                        custom_id=f"roleinfo_back_{role.id}"
                    ),
                    timeout=None
                )
            )  
            
        if custom_id.startswith("roleinfo_back"):
            role = list(filter(lambda x: x.id == int(custom_id.split('_')[2]), guild.roles))[0]
            return await interaction.response.edit_message(
                embed=Embed(
                    title=f'有關 {role.name} 身分組的資訊',
                    color=role.color,
                    timestamp=get_now_time(),
                    fields=[
                        EmbedField(**i) for i in [
                            {"name": "🗒️ 名字", "value": role.mention},
                            {"name": "💳 id", "value": role.id},
                            {"name": "📊 人數", "value": len(role.members)},
                            {"name": "🗓️ 創建時間", "value": role.created_at.strftime('%Y/%m/%d')},
                            {"name": "👾 貼圖", "value": role.unicode_emoji if role.unicode_emoji else "無"},
                        ]
                    ]
                ),
                view=View(
                    Button(
                        style=ButtonStyle.success,
                        label="擁有者",
                        emoji="📊",
                        custom_id=f"roleinfo_owner_{role.id}"
                    ),
                    timeout=None
                )
            )
        
        if custom_id.startswith("clear"):
            _, choose, limit, id = custom_id.split('_')
            
            if user.id != int(id):
                return await interaction.response.send_message("只有指令使用者才能進行操作", ephemeral=True)
            
            await interaction.message.delete()
            if choose == "yes":
                deleted = await interaction.channel.purge(limit=int(limit))
                await interaction.response.send_message(embed=Embed(
                    title="已刪除訊息!",
                    description=f"成功刪除了**{len(deleted)}**則訊息",
                    color=0xff2e2e,
                    timestamp=get_now_time(),
                ), ephemeral=True)
                
                return await interaction.delete_original_message(delay=5.0)
    
            return await interaction.response.send_message("已取消刪除", ephemeral=True)
        
        if custom_id.startswith("math"):
            __, op, id = custom_id.split('_')
            if user.id != int(id):
                return await interaction.response.send_message("❌非此指令使用者無法操控!",ephemeral=True)
            
            value = interaction.message.embeds[0].description[3:-3].replace(' ', '')
            match op:
                case "=":
                    value = calculator(value) 
                case "ac":
                    value = " "
                case "c":
                    value = value[:-1]
                    
                case _:
                    value += op
                    
            await interaction.response.edit_message(embed=Embed(
                title="簡易計算機",
                description=f"```{(value+"                                      ")[:40]}```",
                color=Colour.nitro_pink(),
            ))
        
def setup(bot):
    bot.add_cog(InteractionEvent(bot))
