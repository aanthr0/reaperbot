# -*- coding: utf-8 -*-


# Imports

import discord
from discord.ext import commands
import asyncio
import time
import os
import datetime
from datetime import timedelta, tzinfo, timezone
import random
import json
from discord.activity import Spotify
import sys
import traceback
from bs4 import BeautifulSoup
import requests
import lxml
from lyrics_extractor import SongLyrics

# Setup & Variables

client = commands.Bot(command_prefix=PREFIX_HERE)
activity = discord.Activity(name='the death calendar.', type=discord.ActivityType.watching)
client.remove_command('help')
launchtime = datetime.datetime.utcnow()
#
botVersion = BOT_VERSION_HERE
botAuthor = YOUR_TAG_HERE
#
owner_id = YOUR_ID_HERE
guild_id = MAIN_GUILD_ID_HERE
yes = POSITIVE_EMOJI_MENTION_HERE
no = NEGATIVE_EMOJI_MENTION_HERE
#
footer = 'ReaperBot ©2020 | r?help'
footer2 = 'ReaperBot ©2020'
#
responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Definately', 'You may rely on it.', 'Most likely.', 'Looks good.', 'Yes.', 'Signs point to yes.', 'Hazy. Try again.', 'Ask again later.', 'It is best to not answer right away.', 'Cannot predict that right now.', 'Concentrate, then ask again.', "Don't count on it.", 'No.', 'Doubtful.', 'My source says no.', "The outlook ain't so good."]
oneTo100 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '31', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100']
pp = ['8D', '8=D', '8==D', '8===D', '8====D', '8=====D', '8======D', '8=======D', '8========D', '8=========D', '8==========D', '8===========D', '8============D', '8=============D', '8==============D', '8===============D']


# Basic Events

@client.event
async def on_ready():
    print('-------------------------------------------------------------------------------------')
    print(f'   ReaperBot PY {botVersion} by {botAuthor} started up and ready to use.')
    print('-------------------------------------------------------------------------------------')
    await client.change_presence(status=discord.Status.online, activity=activity)
    cetTime = datetime.datetime.now()
    gmtTime = datetime.timedelta(hours=-1)
    startupTime = cetTime + gmtTime
    statusChannel = client.get_channel(STATUS_CHANNEL_ID_HERE)
    startup = discord.Embed(title='Bot launched' + yes, color=0x2DCF25)
    startup.add_field(name='The Reaper emerged from the depths of hell..', value='Bot started up at ' + startupTime.strftime('%I:%M %p GMT'))
    startup.set_footer(text=footer)
    await statusChannel.send(embed=startup)



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        cmd401 = discord.Embed(title='Error!' + no, color=0xF74F4F)
        cmd401.add_field(name='Unauthorized:', value='You do not have access to this command.')
        cmd401.set_footer(text=footer)
        await ctx.send(embed=cmd401)
    elif isinstance(error, commands.MissingAnyRole):
        cmd401 = discord.Embed(title='Error!' + no, color=0xF74F4F)
        cmd401.add_field(name='Unauthorized:', value='You do not have access to this command.')
        cmd401.set_footer(text=footer)
        await ctx.send(embed=cmd401)
    elif isinstance(error, commands.BotMissingPermissions):
        bot401 = discord.Embed(title='Error!' + no, color=0xF47F4F)
        bot401.add_field(name='Unauthorized:', value='I don\'t have permissions to do this!')
        bot401.set_footer(text=footer)
        await ctx.send(embed=bot401)
    else:
        if ctx.command == 'spotify' or ctx.command == 'userinfo':
            pass
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# Moderation Commands

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='You\'ve been banned!'):
    await member.ban(reason=reason)
    banE = discord.Embed(title='Ban' + yes, color =0x2DCF25)
    banE.add_field(name=f'{ctx.message.member} has been banned.', value='The Reaper will soon harvest their soul..')
    banE.set_footer(text=footer)
    await ctx.send(embed=banE)

@client.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, length: int):
    await ctx.channel.edit(slowmode_delay=length)
    sm = discord.Embed(title='Slowmode' + yes, color=0x2DCF25)
    sm.add_field(name='A\'ight', value=f'Slowmode has been set to {length}s')
    sm.set_footer(footer2)
    await ctx.send(embed=sm)

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            unbanE = discord.Embed(title='Unban' + yes, color=0x2DCF25)
            unbanE.add_field(name=member_name + member_discriminator + ' has been unbanned', value='They\'ll have a hard time getting their soul back though..')
            await ctx.send(embed=unbanE)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason='You\'ve been kicked!'):
    await member.kick(reason=reason)
    kickE = discord.Embed(title='Kick' + yes, color=0x2DCF25)
    kickE.add_field(name=f'{member} has been kicked.', value='Did you tell them to prepare for extreme torture? I hope so..')
    kickE.set_footer(text=footer)
    await ctx.send(embed=kickE)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
    if amount == 0:
        clearNo = discord.Embed(title='Error!' + no, color=0xF74F4F)
        clearNo.add_field(name='You need so specify an amount of messages to clear.', value='\u200b')
        clearNo.set_footer(text=footer)
        await ctx.send(embed=clearNo)
    if amount < 0 or amount == str:
        clearInv = discord.Embed(title='Error!' + no, color=0xF47F4F)
        clearInv.add_field(name='Invalid amount specified', value='\u200b')
        clearInv.set_footer(text=footer)
        await ctx.send(embed=clearInv)
    if amount > 0:
        await ctx.channel.purge(limit=amount+1)
        cleared = discord.Embed(title='Clear' + yes, color=0x2DCF25)
        cleared.add_field(name='You have sucessfully cleared ' + amount + ' messages.', value='\u200b')
        cleared.set_footer(text=footer)
        await ctx.send(embed=cleared, delete_after=2)


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx):
    purgeE = discord.Embed(title='Purge' + yes, color=0x2DCF25)
    purgeE.add_field(name='Hey, did ya hear?', value='Tonight\'s the purge!')
    purgeE.set_footer(text=footer)
    await ctx.send(embed=purgeE)
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=99999999999)

@slowmode.error
async def smErr(ctx, error):
    if isinstance(error, commands.BadArgument):
        smErrE = discord.Embed(title='Slowmode' + no, color=0xF47F4F)
        smErrE.add_field(name='Error;', value='Please provide a valid amount of time (in seconds).')
        smErrE.set_footer(text=footer)
        await ctx.send(embed=smErrE)
    if isinstance(error, commands.MissingRequiredArgument):
        smErrE2 = discord.Embed(title='Slowmode' + no, oclor=0xF47F4F)
        smErrE2.add_field(name='Error;', value='Please provide an amount of time (in seconds).')

@ban.error
async def banError(ctx, error):
    if isinstance(error, commands.BadArgument):
        banEE = discord.Embed(title='Ban' + no, color=0xF47F4F)
        banEE.add_field(name='Error;', value='Member not found.')
        banEE.set_footer(text=footer)
        await ctx.send(embed=banEE)


@unban.error
async def unbanError(ctx, error):
    if isinstance(error, commands.BadArgument):
        unbanEE = discord.Embed(title='Unban' + no, color=0xF47F4F)
        unbanEE.add_field(name='Error;', value='Member not found.')
        unbanEE.set_footer(text=footer)
        await ctx.send(embed=unbanEE)


@kick.error
async def kickError(ctx, error):
    if isinstance(error, commands.BadArgument):
        kickEE = discord.Embed(title='Kick' + no, color=0xF47F4F)
        kickEE.add_field(name='Error;', value='Member not found.')
        kickEE.set_footer(text=footer)
        await ctx.send(embed=kickEE)


# OwnerOnly Commands

@client.command()
async def rules(ctx):
    if ctx.message.author.id == owner_id:
        rE = discord.Embed(title='Server Rules:', color=0x2DCF25)
        rE.add_field(name='\u200b', value='\u200b')
        rE.add_field(name='1.1', value='No blank nicknames.', inline=False)
        rE.add_field(name='1.2', value='No inapproprate, offensive or sexually explicit nicknames.', inline=False)
        rE.add_field(name='1.3', value='Unicode/ascii nicknames are allowed as long as they are readable, otherwise, they will be changed.', inline=False)
        rE.add_field(name='1.4', value='No blank profile pictures.', inline=False)
        rE.add_field(name='1.5', value='No inappropriate, offensive or sexually explicit profile pictures.', inline=False)
        rE.add_field(name='1.6', value='No abuse of bugs, glitches, exploits, etc.', inline=False)
        rE.add_field(name='1.7', value='Exploiting loopholes will result in a ban. If you find a loophole, create a ticket in <#746806667353653380>.', inline=False)
        rE.add_field(name='\u200b', value='\u200b', inline=False)
        rE.add_field(name='2.1', value='No mentioning staff for support, refer to rule 1.7.', inline=False)
        rE.add_field(name='2.2', value='No role-begging.', inline=False)
        rE.add_field(name='2.3', value='Mention spamming will result in a mute.', inline=False)
        rE.add_field(name='2.4', value='NFSW content is ONLY allowed in <#746978868371521597>.', inline=False)
        rE.add_field(name='2.5', value='No modding/hacking/piracy/illegal content/publishing personal information/personal attacks/harassment/sexism/racism/hate speech/religious, political or sexual discussion/flirting/flaming/trolling/spamming/excessive CAPS/emoji or reaction overuse/advertisement (with the exception of <#746806535199653969>', inline=False)
        rE.add_field(name='2.6', value='No walls of text. If you need to post a large sum of text, use pastebin, and link your paste in <#746816810925555714>', inline=False)
        rE.add_field(name='2.7', value='Any message that\'s against the rules can and will be deleted.', inline=False)
        rE.add_field(name='2.8', value='Keep your conversations in English.', inline=False)
        rE.add_field(name='\u200b', value='\u200b', inline=False)
        rE.add_field(name='3.1', value='No channel hopping.', inline=False)
        rE.add_field(name='3.2', value='No ear-rape.', inline=False)
        rE.add_field(name='3.3', value='No NSFW music.', inline=False)
        rE.add_field(name='3.4', value='Playing music is only allowed in the Music voice channel.', inline=False)
        rE.add_field(name='\u200b', value='\u200b', inline=False)
        rE.add_field(name='4.1', value='Any attempt to copy ReaperBot or buy the source code will result in a permanant ban.', inline=False)
        rE.add_field(name='4.2', value='Glitching the bot will result in the same punishment mentioned above.', inline=False)
        rE.set_footer(text=footer)
        await ctx.send(embed=rE)
    else:
        perm = discord.Embed(title='Error!' + no, color=0xF47F4F)
        perm.add_field(name='You\'re not authorized to run this command.', value='\u200b')
        perm.set_footer(text=footer)
        await ctx.send(embed=perm)


@client.command()
async def sponsor(ctx):
    if ctx.message.author.id == owner_id:
        servername = ctx.message.guild.name
        channel = ctx.message.channel
        invite = await channel.create_invite()
        sE = discord.Embed(title='Sponsor' + yes, color=0x2DCF25)
        sE.add_field(name='Success!', value=f'Successfully sponsored `{servername}`')
        sE.set_footer(text=footer2)
        sponsorChannel = client.get_channel(747177846862250046)
        s = discord.Embed(title='Sponsorship', color=0x2DCF5)
        s.add_field(name=f'`{servername}` is now our sponsor!', value=f'[Join here!]({invite})')
        await ctx.send(embed=sE)
        await sponsorChannel.send(embed=s)
    else:
        perm = discord.Embed(title='Error!' + no, color=0xF47F4F)
        perm.add_field(name='You\'re not authorized to run this command.', value='\u200b')
        perm.set_footer(text=footer)
        await ctx.send(embed=perm)


# Utility Commands


@client.command()
async def tag(ctx, *, tag='tags'):
    if tag == 'tags':
        tags = discord.Embed(title='Tags' + yes, color=0x2DCF25)
        tags.add_field(name='Tags:', value='`preference`, `f`, `wtf` \n**more to come..**')
        tags.set_footer(text=footer)
        await ctx.send(embed=tags)
    elif tag == 'preference':
        await ctx.send('everyone has their personal preference \nno matter how good or bad something is, someone still may prefer it over something else, so shut the fuck up')
    elif tag == 'f':
        await ctx.send('i have paid my respects')
    elif tag == 'wtf':
        await ctx.send('what the fuck are you on about')
    elif tag == 'weeb':
        guild = ctx.message.guild.name
        await ctx.send(f'We here at {guild} do not accept weebs, therefore, \n BEGONE THOT')
    else:
        notag = discord.Embed(title='Error!' + no, color=0xF47F4F)
        notag.add_field(name='Invalid tag', value='This tag either doesn\'t exist, or you spelled it wrong!')
        notag.set_footer(text=footer)
        await ctx.send(embed=notag)


@client.command(aliases=['latency'])
async def ping(ctx):
    pingE = discord.Embed(title='Ping' + yes, color=0x2DCF25)
    pingE.add_field(name='The bot\'s ping is', value=f'`{round(client.latency * 1000)}ms`')
    pingE.set_footer(text=footer)
    await ctx.send(embed=pingE)


@client.command()
async def spotify(ctx, user: discord.Member):
    for activity in user.activities:
        if isinstance(activity, Spotify):
            songartists = activity.artist
            songtitle = activity.title
            songalbum = activity.album
            songid = activity.track_id
            albumcover = activity.album_cover_url
            listening2 = discord.Embed(title='Spotify', color=0x1ED760)
            listening2.add_field(name=f'{user} is currently listening to:', value=f'{songartists} - {songtitle} ({songalbum}) \nListen to the song [here](https://open.spotify.com/track/{songid})', inline=False)
            listening2.set_thumbnail(url=f'{albumcover}')
            listening2.set_footer(text=footer)
            await ctx.send(embed=listening2)


@spotify.error
async def spErr(ctx, error):
    if isinstance(error, commands.BadArgument):
        spEE = discord.Embed(title='Error!' + no, color=0xF47F4F)
        spEE.add_field(name='Member not found.', value='\u200b')
        spEE.set_footer(text=footer)
        await ctx.send(embed=spEE)
    if isinstance(error, commands.MissingRequiredArgument):
        for activity in ctx.author.activities:
            if isinstance(activity, Spotify):
                songartists = activity.artist
                songtitle = activity.title
                songalbum = activity.album
                songid = activity.track_id
                albumcover = activity.album_cover_url
                listening2 = discord.Embed(title='Spotify', color=0x1ED760)
                listening2.add_field(name='You are currently listening to:', value=f'{songartists} - {songtitle} ({songalbum}) \nListen to the song [here](https://open.spotify.com/track/{songid})', inline=False)
                listening2.set_thumbnail(url=f'{albumcover}')
                listening2.set_footer(text=footer)
                await ctx.send(embed=listening2)




@client.command(aliases=['statistics', 'info'])
async def stats(ctx):
    uptime = datetime.datetime.utcnow() - launchtime
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    guilds = client.guilds
    guildcount = len(guilds)

    statsEmbed = discord.Embed(title='Statistics', color=0x2DCF25)
    statsEmbed.set_footer(text=footer)
    if days > 0 and hours > 0 and minutes > 0:
        statsEmbed.add_field(name='Uptime:', value=f'{days}d {hours}h {minutes}m', inline=True)
    elif days < 1 and hours < 1 and minutes > 0:
        statsEmbed.add_field(name='Uptime:', value=f'{minutes}m', inline=True)
    elif days < 1:
        statsEmbed.add_field(name='Uptime:', value=f'{hours}h {minutes}m', inline=True)
    else:
        statsEmbed.add_field(name='Developer:', value='<@278872386877784065>', inline=True)
        statsEmbed.add_field(name='Version:', value=f'ReaperBot {botVersion}', inline=True)
        statsEmbed.add_field(name='Language:', value='Python 3.8.5', inline=True)
        statsEmbed.add_field(name='Library:', value='discord.py v1.4.1', inline=True)
        statsEmbed.add_field(name='Date created:', value='24ᵗʰ August 2020', inline=True)
        statsEmbed.add_field(name='Host:', value='[BlueFox Hosting](https://bluefoxhost.com/)', inline=True)
        statsEmbed.add_field(name='Servers:', value=f'{guildcount}', inline=True)

    await ctx.send(embed=statsEmbed)

@client.command(aliases=['ui'])
async def userinfo(ctx, member: discord.Member):
    username = member.name
    userid = member.id
    userimage = member.avatar_url
    discordrep = member.system
    usernick = member.display_name
    discordsince = member.created_at
    if username == usernick:
        user = discord.Embed(title='User Information', color=0x2DCF25)
        user.add_field(name='Username:', value=f'`{username}`', inline=False)
        user.add_field(name='ID:', value=f'`{userid}`', inline=True)
        user.add_field(name='Sys User:', value=f'`{discordrep}`', inline=False)
        user.add_field(name='Has Discord since:', value=f'`{discordsince}`', inline=True)
        user.set_thumbnail(url=f'{userimage}')
        user.set_footer(text=footer)
        await ctx.send(embed=user)
    
    else:
        username = member.name
        userid = member.id
        userimage = member.avatar_url
        discordrep = member.system
        usernick = member.display_name
        discordsince = member.created_at
        user2 = discord.Embed(title='User Information', color=0x2DCF25)
        user2.add_field(name='Username:', value=f'`{username}`', inline=False)
        user2.add_field(name='ID:', value=f'`{userid}`', inline=True)
        user2.add_field(name='Guild nickname:', value=f'`{usernick}`', inline=False)
        user2.add_field(name='Sys User:', value=f'`{discordrep}`', inline=True)
        user2.add_field(name='Has Discord since:', value=f'`{discordsince}`', inline=False)
        user2.set_thumbnail(url=f'{userimage}')
        user2.set_footer(text=footer)
        await ctx.send(embed=user2)



@userinfo.error
async def uiE(ctx, error):
    if isinstance(error, commands.BadArgument):
        uiEE = discord.Embed(title='Error!' + no, color=0xF47F4F)
        uiEE.add_field(name='Member not found.', value='\u200b')
        uiEE.set_footer(text=footer)
        await ctx.send(embed=uiEE)
    if isinstance(error, commands.MissingRequiredArgument):
        username = ctx.message.author.name
        userid = ctx.message.author.id
        userimage = ctx.message.author.avatar_url
        discordrep = ctx.message.author.system
        usernick = ctx.message.author.display_name
        discordsince = ctx.message.author.created_at
        if username == usernick:
            user = discord.Embed(title='User Information', color=0x2DCF25)
            user.add_field(name='Username:', value=f'`{username}`', inline=False)
            user.add_field(name='ID:', value=f'`{userid}`', inline=True)
            user.add_field(name='Sys User:', value=f'`{discordrep}`', inline=False)
            user.add_field(name='Has Discord since:', value=f'`{discordsince}`', inline=True)
            user.set_thumbnail(url=f'{userimage}')
            user.set_footer(text=footer)
            await ctx.send(embed=user)
        else:
            user2 = discord.Embed(title='User Information', color=0x2DCF25)
            user2.add_field(name='Username:', value=f'`{username}`', inline=False)
            user2.add_field(name='ID:', value=f'`{userid}`', inline=True)
            user2.add_field(name='Guild nickname:', value=f'`{usernick}`', inline=False)
            user2.add_field(name='Sys User:', value=f'`{discordrep}`', inline=True)
            user2.add_field(name='Has Discord since:', value=f'`{discordsince}`', inline=False)
            user2.set_thumbnail(url=f'{userimage}')
            user2.set_footer(text=footer)
            await ctx.send(embed=user2)



@client.command(aliases=['si'])
async def serverinfo(ctx):
    servername = ctx.guild.name
    serverregion = ctx.guild.region
    servericon = ctx.guild.icon_url
    serverowner = ctx.guild.owner_id
    boosts = ctx.guild.premium_subscription_count
    creationdate = ctx.guild.created_at
    channelList= ctx.guild.text_channels
    categoryList = ctx.guild.categories
    memberList = ctx.guild.members
    channels = len(channelList)
    categories = len(categoryList)
    members = len(memberList)
    si = discord.Embed(title='Server Information', color=0x2DCF25)
    si.set_thumbnail(url=f'{servericon}')
    si.set_footer(text=footer)
    si.add_field(name='Name:', value=f'`{servername}`', inline=False)
    si.add_field(name='Owner:', value=f'<@{serverowner}> ({serverowner})`', inline=True)
    si.add_field(name='Members:', value=f'`{members}', inline=False)
    si.add_field(name='Region:', value=f'`{serverregion}`', inline=True)
    si.add_field(name='Boosts:', value=f'`{boosts}`', inline=False)
    si.add_field(name='Created at:', value=f'`{creationdate}`', inline=True)
    si.add_field(name='Channels:', value=f'`{channels}`', inline=False)
    si.add_field(name='Categories:', value=f'`{categories}`', inline=True)
    await ctx.send(embed=si)


@client.command()
async def links(ctx):
    link = 'https://discord.com/api/oauth2/authorize?client_id=747404344638439517&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.gg%2F8uTNbPC&scope=bot'
    inv = discord.Embed(title='Click away.. to your death!', color=0x000001)
    inv.add_field(name='Important links:', value=f'[Bot Invite]({link}) \n[Support Server](https://discord.gg/8uTNbPC) \n[Hosting Service](https://discord.gg/rx89wWB) \n[Source Code](https://www.youtube.com/watch?v=DLzxrzFCyOs&ab_channel=AllKindsOfStuff)')
    inv.set_footer(text=footer)
    await ctx.send(embed=inv)


# Fun Commands


@client.command()
async def luck(ctx):
    luckrate = random.choice(oneTo100)
    
    lucky = discord.Embed(title='Luckrate' + yes, color=0x2DCF25)
    lucky.add_field(name=f'You are {luckrate}% lucky.', value=f'We\'ll see how that turns out though, <@{ctx.message.author.id}>')
    lucky.set_footer(text=footer)
    lucky.set_thumbnail(url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=lucky)


@client.command(aliases=['gay%', 'gayrate'])
async def gay(ctx):
    gayrate = random.choice(oneTo100)

    gay = discord.Embed(title='Gay%' + yes, color=0x2DCF25)
    gay.add_field(name=f'You are {gayrate}% gay.', value=f'\u200b')
    gay.set_footer(text=footer)
    gay.set_thumbnail(url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=gay)


@client.command(aliases=['simp%', 'simprate'])
async def simp(ctx):
    simprate = random.choice(oneTo100)

    simp = discord.Embed(title='Simp%' + yes, color=0x2DCF25)
    simp.add_field(name=f'You are {simprate}% simp.', value=f'\u200b')
    simp.set_footer(text=footer)
    simp.set_thumbnail(url=f'{ctx.message.author.avatar_url}')
    await ctx.send(embed=simp)


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    ateBall = random.choice(responses)

    pool = discord.Embed(title='ðﾟﾎﾱ 8Ball', color=0x121212)
    pool.add_field(name='Question:', value=f'`{question}`')
    pool.add_field(name='Answer:', value=f'`{ateBall}`')
    pool.set_thumbnail(url=f'{ctx.message.author.avatar_url}')
    pool.set_footer(text=footer)
    await ctx.send(embed=pool)


@_8ball.error
async def aB(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        noArg = discord.Embed(title='Error!' + no, color=0xF47F4F)
        noArg.add_field(name='Please ask a question!', value='\u200b')
        noArg.set_footer(text=footer)
        await ctx.send(embed=noArg)


@client.command(aliases=['rs'])
async def reapersays(ctx, *, message):
    await ctx.send(message)


@reapersays.error
async def rse(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        noMsg = discord.Embed(title='Error!' + no, color=0xF47F4F)
        noMsg.add_field(name='Please specify your message.', value='\u200b')
        noMsg.set_footer(text=footer)
        await ctx.send(embed=noMsg)


@client.command(aliases=['pp'])
async def penis(ctx):
    d1ck = random.choice(pp)
    dick = discord.Embed(title='Penis Size :flushed:', color=0x2DCF25)
    dick.add_field(name=f'{ctx.message.author.name}\'s penis:', value=d1ck)
    dick.set_footer(text=footer)
    await ctx.send(embed=dick)


@client.command()
async def help(ctx, category='categories'):
    if category == 'categories':
        cats = discord.Embed(title='Help' + yes, color=0x2DCF25)
        cats.add_field(name='┌── ADMINISTRATION ──┐', value='`r?help admin(istration)`', inline=False)
        cats.add_field(name='┌── UTILITY ──┐', value='`r?help utlity`', inline=True)
        cats.add_field(name='┌── MEME ──┐', value='`r?help meme`', inline=False)
        cats.add_field(name='┌── FUN ──┐', value='`r?help fun`', inline=True)
        cats.add_field(name='┌── ECONOMY ──┐', value='`r?help eco(nomy)`', inline=False)
        cats.add_field(name='┌── LEVELS ──┐', value='`r?help levels`', inline=True)
        cats.set_footer(text=footer2)
        await ctx.send(embed=cats)
    if category == 'administration' or category == 'admin':
        admin = discord.Embed(title='Help: ADMINISTRATION', color=0x2DCF25)
        admin.add_field(name='kick', value='Kicks a user from the server, must have `KICK` permissions. \nUsage: r?kick <@user>', inline=False)
        admin.add_field(name='ban', value='Bans a user from the server, must have `BAN` permissions. \nUsage: r?ban <@user>', inline=False)
        admin.add_field(name='unban', value='Unbans a user from the sevrer, must have `BAN` permissions. \nUsage: r?unban <user#tag>', inline=False)
        admin.add_field(name='clear', value='Clears a defined amount of messages, must have `MANAGE MESSAGES` permission. \nUsage: r?clear <amount>', inline=False)
        admin.add_field(name='purge', value='Clears all messaages in a channel, must have `MANAGE MESSAGES` permission. \nUsage: r?purge', inline=False)
        admin.set_footer(text=footer2)
        await ctx.send(embed=admin)
    if category == 'utility':
        utility = discord.Embed(title='Help: UTILITY', color=0x2DCF25)
        utility.add_field(name='stats', value='Shows bot stats. \nUsage: r?stats', inline=False)
        utility.add_field(name='userinfo/ui', value='Shows info about a user. \nUsage: r?userinfo <@member> `OR` r?ui <@member>', inline=False)
        utility.add_field(name='me', value='Shows info about you. \nUsage: r?me', inline=False)
        utility.add_field(name='serverinfo/si', value='Shows info about the server. \nUsage: r?serverinfo `OR` r?si', inline=False)
        utility.add_field(name='ping/latency', value='Returns the bot\'s Discord connection latency. \nUsage: r?ping', inline=False)
        utility.add_field(name='links', value='Returns important bot links. \nUsage: r?invite', inline=False)
        utility.add_field(name='tag', value='Great for use in pointless arguments. \nUsage: r?tag <tag>')
        utility.set_footer(text=footer2)
        await ctx.send(embed=utility)
    if category == 'fun':
        fun = discord.Embed(title='Help: FUN', color=0x2DCF25)
        fun.add_field(name='spotify', value='Displays what song you\'re listening to on Spotify. `SPOTIFY MUST BE IN YOUR RICH PRESENCE!` \nUsage: r?spotify', inline=False)
        fun.add_field(name='luck', value='Shows how lucky you are! \nUsage: r?luck', inline=False)
        fun.add_field(name='gay/gayrate/gay%', value='Shows how gay you are! \nUsage: r?gay `OR` r?gayrate `OR` r?gay%', inline=False)
        fun.add_field(name='simp/simprate/simp%', value='Shows how much of a simp you are! \nUsage: r?simp `OR` r?simprate `OR` r?simp%', inline=False)
        fun.add_field(name='penis/pp', value='Shows the size of your penis. \nUsage: r?penis `OR` r?pp', inline=False)
        fun.add_field(name='8ball', value='Classic 8ball. \nUsage: r?8ball <question>', inline=False)
        fun.set_footer(text=footer2)
        await ctx.send(embed=fun)
    if category == 'economy' or category == 'eco':
        eco = discord.Embed(title='Help: ECONOMY', color=0x2DCF25)
        eco.set_footer(text=footer2)
        eco.add_field(name='Coming soon!', value='\u200b')
        await ctx.send(embed=eco)
    if category == 'meme':
        meme = discord.Embed(title='Help: MEME', color=0x2DCF25)
        meme.add_field(name='Coming soon!', value='\u200b')
        meme.set_footer(text=footer2)
        await ctx.send(embed=meme)
    if category == 'levels':
        levels = discord.Embed(title='Help: LEVELS', color=0x2DCF25)
        levels.add_field(name='Coming soon!', value='\u200b')
        levels.set_footer(text=footer2)
        await ctx.send(embed=levels)
    if category != 'fun' and category != 'utility' and category != 'administration' and category != 'admin' and category != 'categories' and category != 'economy' and category != 'eco' and category != 'meme':
        hE = discord.Embed(title='Error' + no, color=0xF47F4F)
        hE.set_footer(text=footer2)
        hE.add_field(name='Invalid category', value='Please specify a valid category.')
        await ctx.send(embed=hE)

<<<<<<< HEAD
client.run('YOUR TOKEN HERE')
=======
client.run('YOUR TOKEN HERE')
>>>>>>> 92abddcf8481eef5eab2576b1fb2696ddd320ef9
