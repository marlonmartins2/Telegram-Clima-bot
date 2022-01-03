import telebot
from decouple import config
import requests

bot = telebot.TeleBot(config('BOT_TOKEN'))
hg_token = config('HG_TOKEN')


messages_error = {
    400: 'solicitação invalida, tente novamente mais tarde',
    401: 'Não autorizado.',
    403: 'Não Autorizado, contate a API.',
    404: 'não encontrado tente novamente mais tarde',
    500: 'Indisponibilidade, tente novamente mais tarde',
    504: 'Timeout, tente novamente mais tarde',

}

""" core commands """

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message,
        f'Hi {message.from_user.first_name}, Welcome to Underworld Bot!\n'
        'I can help you to know a little everything \n'
        'test "/w <city_name>" for query weather, and other commands\n'
        'Just type /commands to see the list of commands\n'    
    )


@bot.message_handler(commands=['commands'])
def commands(message):
    bot.reply_to(message,
        'The commands are:\n'
        '/start\n'
        '/commands\n'
        '/creator\n'
        '/w <city_name>\n'
            'For example: /w São Paulo\n'
        '/chuck\n'
        '/advice\n'
        '/movie <movie_name>\n'
            'For example: /movie The Matrix\n'
        '/currency <currency_code>\n'
            'For example: /currency USD\n'
    )


@bot.message_handler(commands=['creator'])
def creator(message):
    bot.reply_to(message,
        'The creator of this bot is @MarlonMartins\n'
        'You can find him on GitHub: https://github.com/marlonmartins2/\n'
    )


def handle_response(response):
    try:
        response.raise_for_status()
    except requests.RequestException:
        return
    return response.json()

"""  end core commands """

""" weather commands """
def weather_result(response, message):
    data = response.json()['results']
    bot.reply_to(message,
        f"Cidade: {data['city']}\n"
        f"Data e hora : {data['date']} {data['time']}\n"
        f"Céu: {data['description']}\n"
        f"Atualmente é: {data['currently']}\n"
        f"Temperatura: {data['temp']}°C\n"
        f"Nascer do sol: {data['sunrise']}\n"
        f"Pôr do sol: {data['sunset']}\n"
    )
    

@bot.message_handler(['w'])
def weather_query(message):
    text = message.text.split('/w')[1]
    response = requests.get(f"https://api.hgbrasil.com/weather?key={hg_token}&city_name={text}")
    data = handle_response(response)
    if not data:
        bot.reply_to(message, messages_error.get(response.status_code, 'Erro inesperado, contate o desenvolvedor.'))
        return
    result = weather_result(response, message)
    bot.reply_to(message, result)


""" end weather commands """

""" chuck norris jokes commands """

@bot.message_handler(['chuck'])
def chuck_norris(message):
    response = requests.get("https://api.chucknorris.io/jokes/random")
    data = handle_response(response)
    if not data:
        bot.reply_to(message, messages_error.get(response.status_code, 'Erro inesperado, contate o desenvolvedor.'))
        return
    result = data['value']
    bot.reply_to(message, result)

""" end chuck norris jokes commands """

""" advice commands """

@bot.message_handler(['advice'])
def advice(message):
    response = requests.get("https://api.adviceslip.com/advice")
    data = handle_response(response)
    if not data:
        bot.reply_to(message, messages_error.get(response.status_code, 'Erro inesperado, contate o desenvolvedor.'))
        return
    result = data['slip']['advice']
    bot.reply_to(message, result)

""" end advice commands """

""" imdb commands """
def imdb_result(response, message):
    data = response.json()['d']
    bot.reply_to(message,
        f"url_poster: {data[0]['i']['imageUrl']}\n"
        f"Title: {data[0]['l']}\n"
        f"Type: {data[0]['q']}\n"
        f"Rank: {data[0]['rank']}\n"
        f"Stars: {data[0]['s']}\n"
        f"Year: {data[0]['y']}\n"
    )

@bot.message_handler(['movie'])
def imdb(message):
    text = message.text.split('/movie')[1]
    if not text:
        return bot.reply_to(message, 'Insert the movie name')
    url = "https://imdb8.p.rapidapi.com/auto-complete"
    query = {'q': text}
    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': config('x-rapidapi-key')
    }
    response = requests.get(url, params=query, headers=headers)
    data = handle_response(response)
    if not data:
        bot.reply_to(message, messages_error.get(response.status_code, 'Erro inesperado, contate o desenvolvedor.'))
        return
    result = imdb_result(response, message)
    bot.reply_to(message, result)

""" end imdb commands """

""" Currency commands """

def currency_result(response, message, text):
    data = response.json()
    bot.reply_to(message,
        f"Currency select: {data['base_code']}\n"
        f"Last update (UTC): {data['time_last_update_utc']}\n"
        f"Next update (UTC): {data['time_next_update_utc']}\n"
        f"Conversion Rates:\n"
        f"Selected currency {text}: {data['conversion_rates'][text]}\n"
        f"USD: {data['conversion_rates']['USD']}\n"
        f"EUR: {data['conversion_rates']['EUR']}\n"
        f"GBP: {data['conversion_rates']['GBP']}\n"
        f"BRL: {data['conversion_rates']['BRL']}\n"
        f"JPY: {data['conversion_rates']['JPY']}\n"
        f"CAD: {data['conversion_rates']['CAD']}\n"
    )

@bot.message_handler(['currency'])
def currency(message):
    text = message.text.split('/currency')[1].strip()
    if not text:
        return bot.reply_to(message, 'Insert the currency code')
    response = requests.get(f"https://v6.exchangerate-api.com/v6/{config('exchange_key')}/latest/{text}")
    data = handle_response(response)
    if not data:
        bot.reply_to(message, messages_error.get(response.status_code, 'Erro inesperado, contate o desenvolvedor.'))
        return
    result = currency_result(response, message, text)
    bot.reply_to(message, result)
bot.infinity_polling(interval=0 ,timeout=20)