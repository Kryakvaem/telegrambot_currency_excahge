import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start',"help"])
def info_help(message:telebot.types.Message):
    bot.reply_to(message,'''Чтобы начать работу введите команду боту в следующем формате:\n
<имя валюты цену которой хотите узнать> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты>\n
Узнать список доступной валюты:/values\n
Показать примеры команд бота:/examples''')


@bot.message_handler(commands=['examples'])
def info_examples(message: telebot.types.Message):
    text = '''Вот примеры команд для бота:\n
рубль доллар 1\n
доллар рубль 99\n
евро доллар 45
'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def info_values(message:telebot.types.Message):
    text = "Доступная валюта:"
    for i in keys.keys():
        text = "\n".join((text,i))
    bot.send_message(message.chat.id,text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException("Слишком много/мало параметеров")
        quote, base, amount = values
        price = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя, {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос {e}')
    else:

        text = f"Цена {amount} {quote} в {base} - {price}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)