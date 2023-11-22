import telebot
from telebot import types


tastes = []
taste_dict = {}
with open('info.txt', encoding='utf-8') as file:
    brands_count = len(file.readlines()) - 1
with open('info.txt', encoding='utf-8') as file:
    for i in range(brands_count):
        line = file.readline().replace('\n', '')
        tastes.append(line.split(':'))
for item in tastes:
    taste_dict.update({item[0]: item[1].split(',')})


token = '6359656393:AAHKR2E0ufM91bNJNPAClyVgT7l7rqTEdkY'
bot = telebot.TeleBot(token)
my_chat_id = 853793148
current_brand = ''
result_dict = {}
result_message = ''
contact = ''


@bot.message_handler(commands=['start'])
def info_func(message):
    main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    main_button = types.KeyboardButton(text='Выбрать товар')
    main_keyboard.add(main_button)
    bot.send_message(message.chat.id, 'Приветствуем в магазине', reply_markup=main_keyboard)


@bot.message_handler(content_types=['text'])
def menu_func(message):
    global result_dict
    if message.text.lower() == 'выбрать товар':
        menu_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for key in taste_dict.keys():
            button = types.KeyboardButton(text=key)
            menu_keyboard.add(button)
        back_button = types.KeyboardButton(text='Назад')
        menu_keyboard.add(back_button)
        bot.send_message(message.chat.id, 'Выберите что хотитите заказать', reply_markup=menu_keyboard)
        bot.register_next_step_handler(message, taste_func)

    if message.text == 'Очистить корзину':
        result_dict = {}

        main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        main_button = types.KeyboardButton(text='Выбрать товар')
        main_keyboard.add(main_button)
        bot.send_message(message.chat.id, 'Козина пуста', reply_markup=main_keyboard)

    if message.text.lower() == 'оформить заказ':
        if len(result_dict) == 0:
            main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            main_button = types.KeyboardButton(text='Выбрать товар')
            main_keyboard.add(main_button)
            bot.send_message(message.chat.id, 'Козина пуста', reply_markup=main_keyboard)
        else:
            bot.send_message(message.chat.id, 'Введите имя')
            bot.register_next_step_handler(message, get_contact)


def taste_func(message):
    if message.text in taste_dict.keys():

        global current_brand
        current_brand = message.text

        taste_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        for item in taste_dict[message.text]:
            button = types.KeyboardButton(text=item)
            taste_keyboard.add(button)
        back_button = types.KeyboardButton(text='Назад')
        taste_keyboard.add(back_button)
        bot.send_message(message.chat.id, 'Выберите вкус', reply_markup=taste_keyboard)
        bot.register_next_step_handler(message, choice_func)

    elif message.text.lower() == 'назад':
        main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        main_button = types.KeyboardButton(text='Выбрать товар')
        result_button = types.KeyboardButton(text='Оформить заказ')
        main_keyboard.add(main_button, result_button)
        bot.send_message(message.chat.id, 'Приветствуем в магазине', reply_markup=main_keyboard)


def choice_func(message):
    if message.text.lower() == 'назад':
        main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        main_button = types.KeyboardButton(text='Выбрать товар')
        result_button = types.KeyboardButton(text='Оформить заказ')
        main_keyboard.add(main_button, result_button)
        bot.send_message(message.chat.id, 'Приветствуем в магазине', reply_markup=main_keyboard)
    else:
        if current_brand in result_dict.keys():
            result_dict[current_brand] += [message.text]
        else:
            result_dict.update({current_brand: [message.text]})
        global result_message
        result_message = ''
        for key in result_dict:
            for item in result_dict[key]:
                result_message += f'\n{key.upper()} {item}'

        main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        main_button = types.KeyboardButton(text='Выбрать товар')
        result_button = types.KeyboardButton(text='Оформить заказ')
        cart_button = types.KeyboardButton(text='Очистить корзину')
        main_keyboard.add(main_button, result_button, cart_button)
        bot.send_message(message.chat.id, f'Корзина:\n{result_message}', reply_markup=main_keyboard)


def get_contact(message):
    global contact
    contact += message.text
    bot.send_message(message.chat.id, 'Введите номер телефона')
    bot.register_next_step_handler(message, result_func)


def result_func(message):
    global contact, result_dict, result_message
    contact += f'\n{message.text}'
    bot.send_message(my_chat_id, f'Новый заказ:\n{contact}\n{result_message}')
    contact = ''
    result_dict = {}
    result_message = ''

    main_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    main_button = types.KeyboardButton(text='Выбрать товар')
    main_keyboard.add(main_button)
    bot.send_message(message.chat.id, 'Заказ успешно оформлен\nВ ближайшее время с вами свяжутся',
                     reply_markup=main_keyboard)


if __name__ == '__main__':
    bot.infinity_polling()
