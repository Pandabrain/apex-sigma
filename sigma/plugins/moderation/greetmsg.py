import discord
from sigma.core.permission import check_admin


async def greetmsg(cmd, message, args):
    if not args:
        greet_message = cmd.db.get_settings(message.server.id, 'GreetMessage')
        embed = discord.Embed(color=0x0099FF)
        embed.add_field(name=':information_source: Current Greet Message', value='```\n' + greet_message + '\n```')
    else:
        if not check_admin(message.author, message.channel):
            embed = discord.Embed(title=':no_entry: Unpermitted', color=0xDB0000)
        else:
            new_message = ' '.join(args)
            cmd.db.set_settings(message.server.id, 'GreetMessage', new_message)
            embed = discord.Embed(title=':white_check_mark: New Greet Message Set', color=0x66CC66)
    await cmd.bot.send_message(message.channel, None, embed=embed)
