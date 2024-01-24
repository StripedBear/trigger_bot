import asyncio
import codecs
import configparser
from telethon.sync import TelegramClient
from telethon.sync import events
import logging
from datetime import datetime


"""
show - Show all settings
launch - Launch posting
stop - Stop posting
settime - Set time hh:mm
setmes - Set message(/setmes message)
logon - logon
logoff - logoff
"""


# Logging
current_datetime = datetime.now()
logging.basicConfig(level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=f'logs/{current_datetime.strftime("%H_%M_%S-%d_%m_%Y")}.log')

# Config
config = configparser.ConfigParser()
config.read_file(codecs.open("config.ini", 'r', 'utf8'))

api_Id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
bot_token = config['Telegram']['bot_token']
# sender_id = int(config['Telegram']['sender'])

# Disable sender loop before start and enable logging
config['variables']['work'] = 'Off'
config['variables']['logging'] = 'On'
with open('config.ini', 'w') as configfile:
    config.write(configfile)

# Start the bot
bot = TelegramClient('telegram_bot', api_Id, api_hash)
bot.start(bot_token=bot_token)
logging.debug(f'STRIPED>> Started')
print('Started')


@bot.on(events.NewMessage(pattern='/start'))
async def main_menu(event):
    logging.debug(f'STRIPED>> Start button')
    await handler(event)


# Menu
@bot.on(events.NewMessage(pattern="/show"))
async def handler(event):
    logging.debug(f'STRIPED>> Menu')

    await bot.send_message(event.chat_id,
                           f"Опции"
                           f"\nСостояние: {config['variables']['work']}"
                           f"\nЛогирование: {config['variables']['logging']}"
                           f"\nСообщение: {config['variables']['message']}"
                           f"\nВремя: {config['variables']['time']}")


"""Commands"""


@bot.on(events.NewMessage(pattern="/launch"))
async def launcher(event):
    text = 'Запустил.'
    print(text)
    # await bot.send_message(event.chat_id, text, parse_mode="HTML")
    config['variables']['work'] = 'On'
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    await sending(event)


@bot.on(events.NewMessage(pattern="/settime"))
async def set_msg(event):
    logging.debug(f'STRIPED>> Set tine')
    new_time = event.raw_text.replace('/settime ', '')
    try:
        if 23 < int(new_time.split(':')[0]) < 0 or  59 < int(new_time.split(':')[1]) < 0:
            # await bot.send_message(event.chat_id, 'Wrong time set', parse_mode="HTML")
            print('Wrong time set')
        else:
            config['variables']['time'] = new_time
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            logging.debug(f"STRIPED>> Time changed for: {config['variables']['time']}")
            # await bot.send_message(event.chat_id, 'Время изменено', parse_mode="HTML")
            print('Время изменено')
    except Exception as e:
        logging.debug(f'STRIPED>> [!] {e}')
        print(e)


@bot.on(events.NewMessage(pattern="/setmes"))
async def set_msg(event):
    logging.debug(f'STRIPED>> Set messaging')
    new_mes = event.raw_text.replace('/setmes ', '')
    config['variables']['message'] = new_mes
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    logging.debug(f"STRIPED>> Message changed for: {config['variables']['message']}")
    print('Сообщение изменено')
    # await bot.send_message(event.chat_id, 'Сообщение изменено', parse_mode="HTML")


@bot.on(events.NewMessage(pattern="/logon"))
async def set_logging(event):
    logging.debug(f'STRIPED>> Logging func')
    config['variables']['logging'] = 'On'
    logging.disable(0)
    logging.debug(f'STRIPED>> Logging enable')
    text = 'Включил логирование.'
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(text)
    # await bot.send_message(event.chat_id, text, parse_mode="HTML")


@bot.on(events.NewMessage(pattern="/logoff"))
async def set_logging(event):
    logging.debug(f'STRIPED>> Logging func')
    config['variables']['logging'] = 'Off'
    logging.debug(f'STRIPED>> Logging disable')
    logging.disable(logging.CRITICAL)
    text = 'Выключил логирование.'
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(text)
    # await bot.send_message(event.chat_id, text, parse_mode="HTML")


@bot.on(events.NewMessage(pattern="/stop"))
async def stop_all(event):
    if config['variables']['work'] == 'On':
        config['variables']['work'] = 'Off'
    logging.debug(f'STRIPED>> Loop stopped')
    text = 'Остановлен.'
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(text)
    # await bot.send_message(event.chat_id, text, parse_mode="HTML")


"""Funcs"""


async def sending(event):
    logging.debug('STRIPED>> Sender func')

    target_time_str = config['variables']['time']
    receiver = event.chat_id
    message = config['variables']['message']

    target_time = datetime.strptime(target_time_str, "%H:%M").time()

    while config['variables']['work'] == 'On':
        #await bot.send_message(receiver, 'Начал отправлять', parse_mode="HTML")
        print('Начал отправлять')
        logging.debug('STRIPED>> Check sending')

        current_time = datetime.now().time()
        if current_time >= target_time:
            await bot.send_message(entity=receiver, message=message)
            logging.debug('STRIPED>> Sent')
            break

        time_until_target = datetime.combine(datetime.now().date(), target_time) - datetime.combine(
            datetime.now().date(), current_time)
        await asyncio.sleep(time_until_target.seconds)

    logging.debug('STRIPED>> Finish sending')
    print('Готово')
    # await bot.send_message(receiver, 'Готово', parse_mode="HTML")

bot.run_until_disconnected()


