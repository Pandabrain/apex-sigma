from plugin import Plugin
from config import cmd_remind, donators, OwnerID as ownr, permitted_id
import asyncio
from utils import create_logger
from utils import bold
import time


class Reminder(Plugin):
    is_global = True
    log = create_logger(cmd_remind)

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + cmd_remind + ' '):
            await self.client.send_typing(message.channel)
            cmd_name = 'Reminder'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            remind_input = message.content[len(pfx) + len(cmd_remind) + 1:]
            try:
                time_q, ignore, remind_text = str(remind_input).partition(' ')
            except:
                remind_text = 'Nothing'
                time_q = '0'
                await self.client.send_message(message.channel,
                                               'Input missing parameters.\nThe command format is **' + pfx + cmd_remind + '[time in seconds] [message]**\nExample: ' + pfx + cmd_remind + ' 60 Leeroy jenkins!')
            try:
                time_conv = time.strftime('%H:%M:%S', time.gmtime(int(time_q)))
                if remind_text == '':
                    remind_text = 'Nothing'
                confirm_msg = await self.client.send_message(message.channel, 'Okay! Reminder for\n[' + bold(
                    str(remind_text)) + ']\nis set and will be activated in `' + time_conv + '`! :clock:')
                time_num = int(time_q)
                while time_num != 0:
                    time_num -= 1
                    time_conv_second = time.strftime('%H:%M:%S', time.gmtime(int(time_num)))
                    await self.client.edit_message(confirm_msg,'Okay! Reminder for\n[' + bold(
                    str(remind_text)) + ']\nis set and will be activated in `' + time_conv_second + '`! :clock:')
                    await asyncio.sleep(1)
                await self.client.send_typing(message.channel)
                await self.client.send_message(message.channel,
                                               '<@' + message.author.id + '> Time\'s up! Let\'s do this! :clock: \n :exclamation: ' + bold(
                                                   str(remind_text)) + ' :exclamation: ')
            except SyntaxError:
                await self.client.send_message(message.channel,
                                               'Something went wrong with setting the timer, are you sure you inputed a number?')


class Donators(Plugin):
    is_global = True
    log = create_logger('Donators')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'donors'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Reminder'
            self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                          message.author,
                          message.author.id, message.server.name, message.server.id, message.channel)
            out_text = ''
            for donor in donators:
                out_text += '\n' + bold(str(donor)) + ' :ribbon: '
            await self.client.send_message(message.channel, out_text)


class BulkMSG(Plugin):
    is_global = True
    log = create_logger('BulkMSG')

    async def on_message(self, message, pfx):
        if message.content.startswith(pfx + 'bulkmsg'):
            await self.client.send_typing(message.channel)
            cmd_name = 'Bulk Message'
            # Start Logger
            try:
                self.log.info('User %s [%s] on server %s [%s], used the ' + cmd_name + ' command on #%s channel',
                              message.author,
                              message.author.id, message.server.name, message.server.id, message.channel)
            except:
                self.log.info('User %s [%s], used the ' + cmd_name + ' command.',
                              message.author,
                              message.author.id)
            # Eng Logger
            input_message = message.content[len(pfx) + len('bulkmsg') + 1:]
            try:
                if message.author.id in permitted_id:
                    await self.client.send_message(message.channel,
                                                   'Starting bulk sending... Stand by for confirmation')
                    out = ''
                    for user in self.client.get_all_members():
                        if user.server.id == message.server.id and user.id != self.client.user.id:
                            try:
                                await self.client.start_private_message(user)
                                await self.client.send_message(user, input_message)
                                out += '\nSuccess: ' + user.name
                            except:
                                out += '\nFailed: ' + user.name
                    await self.client.send_message(message.channel, 'Bulk message sending complete...\n' + out[:1900])
                else:
                    await self.client.send_message(message.channel,
                                                   'Not enough permissions, due to security issues, only a permitted user can use this for now...')
            except:
                print('Something went wrong. Most likely a basic error with the sending.')
