from sigma.core.permission import check_man_roles
from sigma.core.rolecheck import matching_role, user_matching_role
import discord


async def takerole(cmd, message, args):
    if not check_man_roles(message.author, message.channel):
        out_content = discord.Embed(type='rich', color=0xDB0000,
                                    title=':no_entry: Insufficient Permissions. Server Admin Only.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if len(args) < 2:
        out_content = discord.Embed(type='rich', color=0xDB0000, title=':exclamation: Error')
        out_content.add_field(name='Missing Arguments', value=cmd.help())
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    if not message.mentions:
        out_content = discord.Embed(type='rich', color=0xDB0000, title=':exclamation: Error')
        out_content.add_field(name='Missing Target User', value=cmd.help())
        await cmd.bot.send_message(message.channel, None, embed=out_content)
        return
    role_qry = ' '.join(args[1:])
    target_role = matching_role(message.server, role_qry)
    target_user = message.mentions[0]
    user_contained_role = user_matching_role(target_user, role_qry)
    if not target_role:
        out_content = discord.Embed(type='rich', color=0xFF9900, title=':exclamation: Error')
        out_content.add_field(name='Role Not Found', value='I was unable to find **' + role_qry + '** on this server.')
        await cmd.bot.send_message(message.channel, None, embed=out_content)
    else:
        if user_contained_role:
            await cmd.bot.remove_roles(target_user, target_role)
            out_content = discord.Embed(type='rich', color=0x66cc66,
                                        title=':white_check_mark: Role ' + role_qry + ' removed from **' + target_user.name + '**.')
            await cmd.bot.create_role(message.server, name=role_qry)
            await cmd.bot.send_message(message.channel, None, embed=out_content)
        else:
            out_content = discord.Embed(type='rich', color=0xFF9900, title=':exclamation: Error')
            out_content.add_field(name='User Missing Role',
                                  value='I was unable to find **' + role_qry + '** in ' + target_user.name + '\'s roles.')
            await cmd.bot.send_message(message.channel, None, embed=out_content)
