# Underworld Telegram BOT!

## Configuration:
Create a virtual environment and install the required packages:
    ```
    python3 -m venv venv
    pip install -r requirements.txt
    ```
Create a file `.env` in the root directory of the projectand add variables with the following tokens generated in the urls below:
    ```
    1- [BOT_TOKEN](https://core.telegram.org/bots#botfather)
    2- [HG_TOKEN] (https://console.hgbrasil.com/users/sign_up)
    3- [x-rapidapi-key] (https://rapidapi.com/auth/sign-up?referral=/hub)
    4- [exchange_key] (https://www.exchangerate-api.com/)
    ```
Then run the bot:
    ```
        python3 underworld_bot.py
    ```
## how to use:
1- Send a message to the bot with the following format:
    
    ```
        /start\
        /commands\
        /creator\
        /w <city_name>
            For example: /w São Paulo
        /chuck
        /advice
        /movie <movie_name>
            For example: /movie The Matrix
        /currency <currency_code>
            For example: /currency USD
    ```
