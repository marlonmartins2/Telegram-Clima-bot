import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

hg_access = open('hg_access.txt')
hg_token = hg_access.read()
hg_access.close()
estado = open('estados.txt')
estados = estado.read()
estado.close()


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}, Welcome to Clima Bot\ '
        fr'I can help you to know the weather in your city\ '
        fr'Just type /commands to see the list of commands\!',
        reply_markup=ForceReply(selective=True),
    )


def commands(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'commands - List of commands\n'
        '/sky - How is the sky today?\n'
        '/creator - Creator of the bot\n'
        '/clima_ip - Weather in your IP\n'
        '/clima_rj - Weather in Rio de Janeiro\n'
        '/clima_sp - Weather in São Paulo\n'
        '/clima_mg - Weather in Minas Gerais\n'
    )


def clima_ip(update: Update, context: CallbackContext) -> None:
    request = requests.get(f"https://api.hgbrasil.com/weather?key={hg_token}&user_ip=remote")
    data = request.json()['results']
    update.message.reply_text(
        f"Cidade: {data['city']}\n"
        f"Data e hora : {data['date']} {data['time']}\n"
        f"Céu: {data['description']}\n"
        f"Atualmente é: {data['currently']}\n"
        f"Temperatura: {data['temp']}°C\n"
        f"Nascer do sol: {data['sunrise']}\n"
        f"Pôr do sol: {data['sunset']}\n"
    )

def clima_rj(update: Update, context: CallbackContext) -> None:
    request = requests.get(f"https://api.hgbrasil.com/weather?key={hg_token}&woeid=455825")
    data = request.json()['results']
    update.message.reply_text(
        f"Cidade: {data['city']}\n"
        f"Data e hora : {data['date']} {data['time']}\n"
        f"Céu: {data['description']}\n"
        f"Atualmente é: {data['currently']}\n"
        f"Temperatura: {data['temp']}°C\n"
        f"Nascer do sol: {data['sunrise']}\n"
        f"Pôr do sol: {data['sunset']}\n"
    )

def clima_sp(update: Update, context: CallbackContext) -> None:
    request = requests.get(f"https://api.hgbrasil.com/weather?key={hg_token}&woeid=455827")
    data = request.json()['results']
    update.message.reply_text(
        f"Cidade: {data['city']}\n"
        f"Data e hora : {data['date']} {data['time']}\n"
        f"Céu: {data['description']}\n"
        f"Atualmente é: {data['currently']}\n"
        f"Temperatura: {data['temp']}°C\n"
        f"Nascer do sol: {data['sunrise']}\n"
        f"Pôr do sol: {data['sunset']}\n"
    )

def clima_mg(update: Update, context: CallbackContext) -> None:
    request = requests.get(f"https://api.hgbrasil.com/weather?key={hg_token}&woeid=455821")
    data = request.json()['results']
    update.message.reply_text(
        f"Cidade: {data['city']}\n"
        f"Data e hora : {data['date']} {data['time']}\n"
        f"Céu: {data['description']}\n"
        f"Atualmente é: {data['currently']}\n"
        f"Temperatura: {data['temp']}°C\n"
        f"Nascer do sol: {data['sunrise']}\n"
        f"Pôr do sol: {data['sunset']}\n"
    )


def sky(update: Update, context: CallbackContext) -> None:
    request = requests.get(f"https://api.hgbrasil.com/weather?key={hg_token}&user_ip=remote")
    data = request.json()['results']
    update.message.reply_text(
        f"O tempo está {data['description']} hoje.\n"
    )

def creator(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Creator: @marllondjofficial\nGithub: https://github.com/marlonmartins2')

def main() -> None:
    token = open('token_access.txt')
    telegram_token = token.read()
    token.close()
    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("commands", commands))
    dispatcher.add_handler(CommandHandler("sky", sky))
    dispatcher.add_handler(CommandHandler("creator", creator))
    dispatcher.add_handler(CommandHandler("clima_ip", clima_ip))
    dispatcher.add_handler(CommandHandler("clima_rj", clima_rj))
    dispatcher.add_handler(CommandHandler("clima_sp", clima_sp))
    dispatcher.add_handler(CommandHandler("clima_mg", clima_mg))


    updater.start_polling()


    updater.idle()


if __name__ == '__main__':
    main()