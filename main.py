import requests
import telebot

# Токен вашего Telegram-бота
TOKEN = '6233704086:AAFPlG8nYq9S-KDZ99uFE3U32vfhwJE2aD0'
# Токен API Giphy
GIPHY_TOKEN = 'diKrGHs6MeiY0Qz3StpV08hezrB2B2pz'

# Инициализация бота
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я Giphy-бот. Отправь мне ключевое слово, и я найду для тебя гифку!")


@bot.message_handler(func=lambda message: True)
def search_gif(message):
    # Получение ключевого слова из сообщения пользователя
    search_query = message.text
    
    # Параметры запроса к API Giphy
    params = {
        'api_key': GIPHY_TOKEN,
        'q': search_query,
        'limit': 1  # Количество гифок, которое мы хотим получить
    }
    
    try:
        # Запрос к API Giphy
        response = requests.get('https://api.giphy.com/v1/gifs/search', params=params)
        data = response.json()
        
        if data['data']:
            # Получение URL первой найденной гифки
            gif_url = data['data'][0]['images']['original']['url']
            
            # Отправка гифки пользователю
            bot.send_animation(message.chat.id, gif_url)
        else:
            bot.reply_to(message, "К сожалению, я не смог найти гифку по этому запросу.")
    
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при поиске гифки.")
        print(e)


# Запуск бота
bot.polling()

