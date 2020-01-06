# -*- coding: utf-8 -*-

# import scripts
from bot_core import bot_handlers
# from config import logging_bot


# import data
# import modules
import pyexcel
import datetime as d
import re, random, string
from time import sleep
from copy import deepcopy
from collections import OrderedDict
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, LabeledPrice

from bot_core import keyboardbot, textbot
from config import update_data, query_data, config, db_requests
from config.error_decorator import error_catch_decorator


class MainBot:
    """Функционал бота"""
    def __init__(self):
        self.registration_form = {}
        self.partnership_form = {}
        self.mailing_form = {}

# СТАРТ
    def start(self, bot, update):
        """Старт/Главное меню"""
        user_id = update_data.user_id(update)
        user_db = db_requests.select_user({'user_id': user_id})
        first_name = update_data.first_name(update)

        self.registration_form.pop(user_id, None)
        self.partnership_form.pop(user_id, None)

        if user_db is None:
            user_name = update_data.user_name(update)
            self.registration_form[user_id] = {'user_id': user_id, 'user_name': user_name, 'first_name': first_name}

            text = textbot.language
            keyboard = keyboardbot.language

        else:
            text = textbot.main_menu[user_db['language']].format(first_name=first_name)
            keyboard = keyboardbot.main_menu[user_db['language']]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

        db_admin = db_requests.select_user_admin({'user_id': user_id})
        if db_admin:
            text_admin = textbot.admin
            bot.send_message(chat_id=user_id, text=text_admin, parse_mode='HTML')
# СТАРТ


# СТАТИСТИКА
    @staticmethod
    def statistic_admin(bot, update):
        """Статистик админу"""
        user_id = update_data.user_id(update)
        db_admin = db_requests.select_user_admin({'user_id': user_id})
        if db_admin:
            result_users = db_requests.select_users_statistic()
            result_partnership = db_requests.select_partnership_statistic()
            result_order = db_requests.select_order_statistic()

            array_table = {}
            if result_users:
                array_table['Клиенты'] = result_users
            if result_partnership:
                array_table['Партнерка'] = result_partnership
            if result_order:
                for ind, item in enumerate(result_order):
                    d_type_payment = {'cash': 'Наличные', 'payme': 'PayMe'}
                    d_type_delivery = {'self': 'Самовывоз', 'delivery': 'Доставка'}
                    d_status = {0: "🛒 Новый", 1: "✅ Принят", 2: "⌛ Ожидание", 3: "❌ Отклонен"}

                    result_order[ind]['ТИП ОПЛАТЫ'] = d_type_payment[item['ТИП ОПЛАТЫ']]
                    result_order[ind]['ТИП ДОСТАВКИ'] = d_type_delivery[item['ТИП ДОСТАВКИ']]
                    result_order[ind]['СТАТУС ЗАКАЗА'] = d_status[item['СТАТУС ЗАКАЗА']]

                array_table['Заказы'] = result_order

            if array_table == {}:
                bot.send_message(chat_id=user_id, text=textbot.statistic_empty, parse_mode='HTML')
                return

            array = OrderedDict()

            for result in array_table:
                sheet_name = result
                array[sheet_name] = [[key for key in array_table[result][0]]
                                     ]
                for data in array_table[result]:
                    array[sheet_name].append([data[key] for key in data])

            pyexcel.save_book_as(bookdict=array, dest_file_name="statistic.xls")

            bot.send_message(chat_id=user_id, text=textbot.statistic, parse_mode='HTML')

            with open('statistic.xls', 'rb') as f:
                bot.sendDocument(chat_id=user_id, document=f, timeout=1000)
# СТАТИСТИКА


# ЯЗЫК
    def language(self, bot, update):
        """Язык"""
        user_id = update_data.user_id(update)
        user_text = update_data.text(update)

        d_key = {keyboardbot.d_language['ru']: 'ru', keyboardbot.d_language['uz']: 'uz'}
        language = d_key[user_text]

        if self.registration_form.get(user_id):
            self.registration_form[user_id]['language'] = language
            main_object.contact(bot, update)

        else:
            main_object.start(bot, update)


    def contact(self, bot, update):
        """Контакт при регистрации"""
        user_id = update_data.user_id(update)
        self.registration_form[user_id]['contact'] = None

        text = textbot.contact[self.registration_form[user_id]['language']]
        keyboard = deepcopy(keyboardbot.contact[self.registration_form[user_id]['language']])[:1]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


    def insert_user(self, bot, update):
        """Добавление пользователя в базу"""
        user_id = update_data.user_id(update)

        db_requests.insert_user(self.registration_form[user_id])
        main_object.start(bot, update)
# ЯЗЫК|


# МЕНЮ
    @staticmethod
    def change_language(bot, update):
        """Сменить язык"""
        user_id = update_data.user_id(update)
        user_db = db_requests.select_user({'user_id': user_id})

        d_language = {'ru': 'uz', 'uz': 'ru'}
        language = d_language[user_db['language']]

        data = {'language': language, 'user_id': user_id}
        db_requests.update_language(data)

        main_object.start(bot, update)


    @staticmethod
    def products(bot, update):
        """Виды продукций"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        text = textbot.products[language]
        keyboard = keyboardbot.products[language]
        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


    @staticmethod
    def about(bot, update):
        """О нас"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        text = textbot.about[language]
        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')


    @staticmethod
    def news(bot, update):
        """Новости"""
        try:
            user_id = update_data.user_id(update)
        except Exception:
            user_id = query_data.user_id(update)

        language = db_requests.select_user({'user_id': user_id})['language']

        data = {'offset': 0, 'offset_id_back': -1, 'offset_id_next': 1, 'language': language}
        data_product = main_object.generator_inline_news(data=data)

        if data_product is None:
            text = textbot.not_news[language]
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
            return

        photo = data_product['photo']
        caption = data_product['caption']
        keyboard = data_product['keyboard']

        with open(photo, 'rb') as p:
            bot.send_photo(chat_id=user_id, photo=p, caption=caption,
                           parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    def actions(bot, update):
        """Акции"""
        try:
            user_id = update_data.user_id(update)
        except Exception:
            user_id = query_data.user_id(update)

        language = db_requests.select_user({'user_id': user_id})['language']

        data = {'offset': 0, 'offset_id_back': -1, 'offset_id_next': 1, 'language': language}
        data_product = main_object.generator_inline_actions(data=data)

        if data_product is None:
            text = textbot.not_actions[language]
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
            return

        photo = data_product['photo']
        caption = data_product['caption']
        keyboard = data_product['keyboard']

        with open(photo, 'rb') as p:
            bot.send_photo(chat_id=user_id, photo=p, caption=caption,
                           parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    def basket(bot, update):
        """Корзина"""
        delivery_object.basket(bot, update)

    @staticmethod
    def partnership(bot, update):
        """Партнерка"""
        user_id = update_data.user_id(update)
        db_user = db_requests.select_user({'user_id': user_id})
        language = db_user['language']

        db_partner = db_requests.select_partnership({'user_id_id': db_user['id']})

        if db_partner:
            if db_partner['brand_id']:
                text = textbot.partnership_statistic[language]
                keyboard = keyboardbot.partnership_statistic[language]

            else:
                text = textbot.partnership_already[language]
                keyboard = keyboardbot.partnership_already[language]

        else:
            text = textbot.partnership[language]
            keyboard = keyboardbot.partnership[language]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
# МЕНЮ


# ПАРТНЕРКА
    @staticmethod
    def info_partnership(bot, update):
        """Информация о партнерке"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        text = textbot.info_partnership[language]
        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')


    @staticmethod
    def statistic(bot, update):
        """Статистика по партнерке"""
        user_id = update_data.user_id(update)
        db_user = db_requests.select_user({'user_id': user_id})
        language = db_user['language']

        db_partner = db_requests.select_partnership({'user_id_id': db_user['id']})

        if db_partner:
            if db_partner['brand_id']:
                result_partnership = db_requests.select_for_partnership_statistic({'brand_id': db_partner['brand_id']})

                array_table = {}
                if result_partnership:
                    array_table['Статистика'] = result_partnership

                if array_table == {}:
                    bot.send_message(chat_id=user_id, text=textbot.statistic_empty, parse_mode='HTML')
                    return

                array = OrderedDict()

                for result in array_table:
                    sheet_name = result
                    array[sheet_name] = [[key for key in array_table[result][0]]
                                         ]
                    for data in array_table[result]:
                        array[sheet_name].append([data[key] for key in data])

                pyexcel.save_book_as(bookdict=array, dest_file_name="statistic.xls")

                bot.send_message(chat_id=user_id, text=textbot.statistic, parse_mode='HTML')

                with open('statistic.xls', 'rb') as f:
                    bot.sendDocument(chat_id=user_id, document=f, timeout=1000)

                return

        text = textbot.partnership_already[language]
        keyboard = keyboardbot.partnership_already[language]
        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))



    def application(self, bot, update):
        """Отзыв на партнерку"""
        user_id = update_data.user_id(update)
        db_user = db_requests.select_user({'user_id': user_id})
        language = db_user['language']

        db_partner = db_requests.select_partnership({'user_id_id': db_user['id']})

        if db_partner:
            text = textbot.partnership_already[language]
            keyboard = keyboardbot.partnership_already[language]

        else:
            self.partnership_form[user_id] = {'user_id': user_id, 'user_id_id': db_user['id'], 'brand_name': None}

            text = textbot.brand_name[language]
            keyboard = [[keyboardbot.d_menu[language]['main_menu']]]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


    def partnership_full_name(self, bot, update):
        """Партнерка заполнение имени"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        self.partnership_form[user_id]['full_name'] = None

        text = textbot.partnership_full_name[language]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')


    def partnership_contact(self, bot, update):
        """Партнерка контакт"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        self.partnership_form[user_id]['contact'] = None

        text = textbot.partnership_contact[language]
        keyboard = keyboardbot.contact[language]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


    def partnership_document(self, bot, update):
        """Партнерка документ"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        self.partnership_form[user_id]['comment'] = None
        self.partnership_form[user_id]['document'] = None

        text = textbot.partnership_document[language]
        keyboard = [[keyboardbot.d_menu[language]['main_menu']]]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


    def partnership_done(self, bot, update):
        """Законичть оформление заявки"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        data_application = self.partnership_form[user_id]
        self.partnership_form.pop(user_id, None)

        text = textbot.partnership_done[language]
        keyboard = keyboardbot.main_menu[language]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

        main_object.partnership_to_channel(bot, update, data_application)


    @staticmethod
    def partnership_to_channel(bot, update, data_application):
        """Добавить в базу новую заявку и оповестить в канал"""
        document = None
        application = data_application['comment']

        if data_application['document']:
            file_path = 'partnership/{user_id}.{exp}'.format(user_id=data_application['user_id'], exp=data_application['exp'])
            document = file_path
            application = textbot.document_url.format(link=config.host_url.format(file_path))


            path = config.media_path.format(file_path)
            obj = bot.get_file(file_id=data_application['document'])
            obj.download(path)

        data = {'user_id_id': data_application['user_id_id'],
                'full_name': data_application['full_name'],
                'contact': data_application['contact'],
                'brand_name': data_application['brand_name'],
                'comment': data_application['comment'],
                'document': document}

        db_requests.insert_partnership(data)


        text = textbot.partnership_to_channel.format(user_id=data_application['user_id'],
                                                     full_name=data_application['full_name'],
                                                     contact=data_application['contact'],
                                                     brand_name=data_application['brand_name'],
                                                     application=application)

        bot.send_message(chat_id=config.id_channel_partnership, text=text, parse_mode='HTML')
# ПАРТНЕРКА


# АКЦИИ
    @staticmethod
    def action_switch(bot, update):
        """переключение акций"""
        user_id = query_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        message_id = query_data.message_id(update)
        data = query_data.data(update).split('_')
        callback_query_id = query_data.callback_query_id(update)
        bot.answer_callback_query(callback_query_id=callback_query_id)

        offset = int(data[-1])

        offset_id_back = offset - 1
        offset_id_next = offset + 1

        data = {'offset': offset, 'offset_id_back': offset_id_back,
                'offset_id_next': offset_id_next,
                'language': language}

        data_product = main_object.generator_inline_actions(data=data)
        if data_product:
            photo = data_product['photo']
            caption = data_product['caption']
            keyboard = data_product['keyboard']

            with open(photo, 'rb') as p:
                bot.editMessageMedia(chat_id=user_id,
                                     media=InputMediaPhoto(media=p, caption=caption, parse_mode='HTML'),
                                     message_id=message_id,
                                     reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            try:
                bot.delete_message(chat_id=user_id, message_id=message_id)
            except Exception:
                try:
                    bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=InlineKeyboardMarkup([]))
                except Exception:
                    pass

            main_object.actions(bot, update)
# АКЦИИ


# НОВОСТИ
    @staticmethod
    def news_switch(bot, update):
        """переключение новостей"""
        user_id = query_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        message_id = query_data.message_id(update)
        data = query_data.data(update).split('_')
        callback_query_id = query_data.callback_query_id(update)
        bot.answer_callback_query(callback_query_id=callback_query_id)

        offset = int(data[-1])

        offset_id_back = offset - 1
        offset_id_next = offset + 1

        data = {'offset': offset, 'offset_id_back': offset_id_back,
                'offset_id_next': offset_id_next,
                'language': language}

        data_product = main_object.generator_inline_news(data=data)
        if data_product:
            photo = data_product['photo']
            caption = data_product['caption']
            keyboard = data_product['keyboard']

            with open(photo, 'rb') as p:
                bot.editMessageMedia(chat_id=user_id,
                                     media=InputMediaPhoto(media=p, caption=caption, parse_mode='HTML'),
                                     message_id=message_id,
                                     reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            try:
                bot.delete_message(chat_id=user_id, message_id=message_id)
            except Exception:
                try:
                    bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id,
                                                  reply_markup=InlineKeyboardMarkup([]))
                except Exception:
                    pass

            main_object.news(bot, update)
# НОВОСТИ


# ГЕНЕРАТОР ИНЛАЙН МЕНЮ
    @staticmethod
    def generator_inline_actions(data):
        """Генерация карточки акции"""
        offset_max = len(db_requests.select_all_actions())
        data['limit'] = offset_max
        action_data = db_requests.select_action(data)

        if action_data is None:
            return None

        photo = config.media_path.format(action_data['photo_path'])

        caption = action_data['title']

        keyboard = [[InlineKeyboardButton(keyboardbot.d_action[data['language']]['back'],
                                          callback_data='action_switch_back_{offset_id_back}'.format(offset_id_back=data['offset_id_back'])),
                     InlineKeyboardButton(keyboardbot.d_action[data['language']]['next'],
                                          callback_data='action_switch_next_{offset_id_next}'.format(offset_id_next=data['offset_id_next']))],
                    ]


        if (data['offset_id_back'] == -1) and (offset_max == data['offset'] + 1):
            keyboard = []
        elif data['offset_id_back'] == -1:
            keyboard[0].pop(0)
        elif offset_max == data['offset'] + 1:
            keyboard[0].pop(1)

        data_product = {'keyboard': keyboard, 'caption': caption, 'photo': photo}
        return data_product


    @staticmethod
    def generator_inline_news(data):
        """Генерация карточки новости"""
        offset_max = len(db_requests.select_all_news())
        data['limit'] = offset_max
        action_data = db_requests.select_one_news(data)

        if action_data is None:
            return None

        photo = config.media_path.format(action_data['photo_path'])

        caption = action_data['title']

        keyboard = [[InlineKeyboardButton(keyboardbot.d_action[data['language']]['back'],
                                          callback_data='news_switch_back_{offset_id_back}'.format(
                                              offset_id_back=data['offset_id_back'])),
                     InlineKeyboardButton(keyboardbot.d_action[data['language']]['next'],
                                          callback_data='news_switch_next_{offset_id_next}'.format(
                                              offset_id_next=data['offset_id_next']))],
                    ]

        if (data['offset_id_back'] == -1) and (offset_max == data['offset'] + 1):
            keyboard = []
        elif data['offset_id_back'] == -1:
            keyboard[0].pop(0)
        elif offset_max == data['offset'] + 1:
            keyboard[0].pop(1)

        data_product = {'keyboard': keyboard, 'caption': caption, 'photo': photo}
        return data_product


    @staticmethod
    def generator_inline(call_back='default', row=3, data=None):
        """Генератор инлайн меню"""
        if call_back == 'healthy':
            results = db_requests.select_categories_healthy(data)
        elif call_back == 'products_healthy':
            results = db_requests.select_products_healthy(data)
        elif call_back == 'sport':
            results = db_requests.select_categories_sport(data)
        elif call_back == 'products_sport':
            results = db_requests.select_products_sport(data)
        else:
            results = None

        if results is None:
            return None

        keyboard = []
        for i in range(row, len(results) + row, row):
            transition = results[i - row: i]
            try:
                keyboard.append([InlineKeyboardButton(transition[0]['button_name'],
                                                      callback_data='{}_{}'.format(call_back, transition[0]['id'])),
                                 InlineKeyboardButton(transition[1]['button_name'],
                                                      callback_data='{}_{}'.format(call_back, transition[1]['id'])),
                                 InlineKeyboardButton(transition[2]['button_name'],
                                                      callback_data='{}_{}'.format(call_back,
                                                                                   transition[2]['id']))])
            except Exception:
                try:
                    keyboard.append([InlineKeyboardButton(transition[0]['button_name'],
                                                          callback_data='{}_{}'.format(call_back,
                                                                                       transition[0]['id'])),
                                     InlineKeyboardButton(transition[1]['button_name'],
                                                          callback_data='{}_{}'.format(call_back,
                                                                                       transition[1]['id']))])
                except Exception:
                    keyboard.append(
                        [InlineKeyboardButton(transition[0]['button_name'],
                                              callback_data='{}_{}'.format(call_back, transition[0]['id']))])
        return keyboard
# ГЕНЕРАТОР ИНЛАЙН МЕНЮ


# ПРОДУКТЫ
    @staticmethod
    def healthy(bot, update):
        """Категории - здоровое питание"""
        try:
            user_id = query_data.user_id(update)
            message_id = query_data.message_id(update)
            callback_query_id = query_data.callback_query_id(update)
            flag_update = True
        except Exception:
            user_id = update_data.user_id(update)
            flag_update = False
            callback_query_id = None
            message_id = None

        language = db_requests.select_user({'user_id': user_id})['language']

        text = textbot.category[language]
        keyboard = main_object.generator_inline(call_back='healthy', row=2, data={'language': language})

        if keyboard is None:
            text_empty = textbot.category_empty[language]

            if flag_update:
                bot.answer_callback_query(callback_query_id=callback_query_id, text=text, cache_time=10,
                                          show_alert=True)
            else:
                bot.send_message(chat_id=user_id, text=text_empty, parse_mode='HTML')
            return

        if flag_update:
            bot.answer_callback_query(callback_query_id=callback_query_id)
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text=text,
                                  parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=InlineKeyboardMarkup(keyboard))


    @staticmethod
    def products_healthy(bot, update):
        """Выбор категории здоровое питание"""
        user_id = query_data.user_id(update)
        message_id = query_data.message_id(update)
        category_id = query_data.data(update).split('_')[-1]
        callback_query_id = query_data.callback_query_id(update)

        language = db_requests.select_user({'user_id': user_id})['language']

        data = {'id': category_id, 'language': language}
        keyboard = main_object.generator_inline(call_back='products_healthy', row=2, data=data)

        if keyboard is None:
            text = textbot.product_empty[language]
            bot.answer_callback_query(callback_query_id=callback_query_id, text=text, cache_time=10,
                                      show_alert=True)
            return

        bot.answer_callback_query(callback_query_id=callback_query_id)
        text = textbot.product[language]

        keyboard.append(keyboardbot.back_category_healthy[language])

        try:
            bot.edit_message_text(chat_id=user_id, text=text, parse_mode='HTML',
                                  message_id=message_id, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
            bot.delete_message(chat_id=user_id, message_id=message_id)
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=InlineKeyboardMarkup(keyboard))


    @staticmethod
    def healthy_product(bot, update):
        """Выбор продукта здоровое питание"""
        user_id = query_data.user_id(update)
        message_id = query_data.message_id(update)
        product_id = query_data.data(update).split('_')[-1]
        callback_query_id = query_data.callback_query_id(update)

        language = db_requests.select_user({'user_id': user_id})['language']

        data = {'product_id': product_id, 'language': language}
        result = db_requests.select_healthy_product(data)

        if result is None:
            text = textbot.product_none[language]
            bot.answer_callback_query(callback_query_id=callback_query_id, text=text, cache_time=10, show_alert=True)
            return

        bot.answer_callback_query(callback_query_id=callback_query_id)

        if (result['description'] is None) or (result['description'] == ''):
            description = ''
        else:
            description = '\n\n' + result['description']

        caption = textbot.product_template[language].format(title=result['title'], description=description, price=result['price'])

        keyboard = [[InlineKeyboardButton(keyboardbot.add_basket[language],
                                          callback_data='add_healthy_{}_{}'.format(result['category_id'], product_id))],
                    [InlineKeyboardButton(keyboardbot.back[language],
                                          callback_data='healthy_{}'.format(result['category_id']))]]

        bot.answer_callback_query(callback_query_id=callback_query_id)

        bot.delete_message(chat_id=user_id, message_id=message_id)
        with open(config.media_path.format(result['photo_path']), 'rb') as photo:
            bot.send_photo(chat_id=user_id, photo=photo, caption=caption,
                           parse_mode='HTML',
                           reply_markup=InlineKeyboardMarkup(keyboard))


    @staticmethod
    def sport(bot, update):
        """Категории - спортивное питание"""
        try:
            user_id = query_data.user_id(update)
            message_id = query_data.message_id(update)
            callback_query_id = query_data.callback_query_id(update)
            flag_update = True
        except Exception:
            user_id = update_data.user_id(update)
            flag_update = False
            callback_query_id = None
            message_id = None

        language = db_requests.select_user({'user_id': user_id})['language']

        text = textbot.category[language]
        keyboard = main_object.generator_inline(call_back='sport', row=2, data={'language': language})

        if keyboard is None:
            text_empty = textbot.category_empty[language]

            if flag_update:
                bot.answer_callback_query(callback_query_id=callback_query_id, text=text, cache_time=10,
                                          show_alert=True)
            else:
                bot.send_message(chat_id=user_id, text=text_empty, parse_mode='HTML')
            return

        if flag_update:
            bot.answer_callback_query(callback_query_id=callback_query_id)
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text=text,
                                  parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=InlineKeyboardMarkup(keyboard))


    @staticmethod
    def products_sport(bot, update):
        """Выбор категории спортивное питание"""
        user_id = query_data.user_id(update)
        message_id = query_data.message_id(update)
        category_id = query_data.data(update).split('_')[-1]
        callback_query_id = query_data.callback_query_id(update)

        language = db_requests.select_user({'user_id': user_id})['language']

        data = {'id': category_id, 'language': language}
        keyboard = main_object.generator_inline(call_back='products_sport', row=2, data=data)

        if keyboard is None:
            text = textbot.product_empty[language]
            bot.answer_callback_query(callback_query_id=callback_query_id, text=text, cache_time=10,
                                      show_alert=True)
            return

        bot.answer_callback_query(callback_query_id=callback_query_id)
        text = textbot.product[language]

        keyboard.append(keyboardbot.back_category_sport[language])

        try:
            bot.edit_message_text(chat_id=user_id, text=text, parse_mode='HTML',
                                  message_id=message_id, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
            bot.delete_message(chat_id=user_id, message_id=message_id)
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=InlineKeyboardMarkup(keyboard))


    @staticmethod
    def sport_product(bot, update):
        """Выбор продукта спортивное питание"""
        user_id = query_data.user_id(update)
        message_id = query_data.message_id(update)
        product_id = query_data.data(update).split('_')[-1]
        callback_query_id = query_data.callback_query_id(update)

        language = db_requests.select_user({'user_id': user_id})['language']

        data = {'product_id': product_id, 'language': language}
        result = db_requests.select_sport_product(data)

        if result is None:
            text = textbot.product_none[language]
            bot.answer_callback_query(callback_query_id=callback_query_id, text=text, cache_time=10, show_alert=True)
            return

        bot.answer_callback_query(callback_query_id=callback_query_id)

        if (result['description'] is None) or (result['description'] == ''):
            description = ''
        else:
            description = '\n\n' + result['description']

        caption = textbot.product_template[language].format(title=result['title'], description=description,
                                                            price=result['price'])

        keyboard = [[InlineKeyboardButton(keyboardbot.add_basket[language],
                                          callback_data='add_sport_{}_{}'.format(result['category_id'], product_id))],
                    [InlineKeyboardButton(keyboardbot.back[language],
                                          callback_data='sport_{}'.format(result['category_id']))]]

        bot.answer_callback_query(callback_query_id=callback_query_id)

        bot.delete_message(chat_id=user_id, message_id=message_id)
        with open(config.media_path.format(result['photo_path']), 'rb') as photo:
            bot.send_photo(chat_id=user_id, photo=photo, caption=caption,
                           parse_mode='HTML',
                           reply_markup=InlineKeyboardMarkup(keyboard))
# ПРОДУКТЫ


# ЗАКАЗАТЬ
    @staticmethod
    def order(bot, update):
        """Заказать"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']


        if delivery_object.user_basket_healthy.get(user_id) or delivery_object.user_basket_sport.get(user_id):
            text = textbot.type_delivery[language]
            keyboard = keyboardbot.type_delivery[language]

            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

        else:
            delivery_object.basket(bot, update)
            main_object.start(bot, update)


    @staticmethod
    def type_payment(bot, update):
        """Выбор типа оплаты"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        if delivery_object.user_basket_healthy.get(user_id) or delivery_object.user_basket_sport.get(user_id):
            text = textbot.type_payment[language]
            keyboard = keyboardbot.type_payment[language]

            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        else:
            delivery_object.basket(bot, update)
            main_object.start(bot, update)


    @staticmethod
    def location(bot, update):
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        delivery_object.user_order_form[user_id]['location'] = None

        text = textbot.location[language]
        keyboard = keyboardbot.location[language]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

    @staticmethod
    def type_payment_choose(bot, update):
        """Выбор типа оплаты"""
        user_id = update_data.user_id(update)
        button_name = update_data.text(update)
        language = db_requests.select_user({'user_id': user_id})['language']


        if delivery_object.user_basket_healthy.get(user_id) or delivery_object.user_basket_sport.get(user_id):
            d_type_payment = {'ru': {keyboardbot.d_type_payment['ru']['cash']: 'cash',
                                     keyboardbot.d_type_payment['ru']['payme']: 'payme'},
                              'uz': {keyboardbot.d_type_payment['uz']['cash']: 'cash',
                                     keyboardbot.d_type_payment['uz']['payme']: 'payme'}}

            delivery_object.user_order_form[user_id]['type_payment'] = d_type_payment[language][button_name]
            delivery_object.send_order(bot, update)
        else:
            delivery_object.basket(bot, update)
            main_object.start(bot, update)
# ЗАКАЗАТЬ


# ФИЛЬТРЫ
    def filter_text(self, bot, update):
        """Фильтр текста"""
        user_id = update_data.user_id(update)
        user_text = update_data.text(update)
        message_id = update_data.message_id(update)


        if delivery_object.user_product.get(user_id): # если выбран продукт для ввода количества menu
            language = db_requests.select_user({'user_id': user_id})['language']
            if delivery_object.user_product[user_id]['count'] is None:
                if user_text.isdigit():
                    delivery_object.user_product[user_id]['count'] = int(user_text)
                    data_select = {'product_id': delivery_object.user_product[user_id]['product'], 'language': language}

                    if delivery_object.user_product[user_id]['kind'] == 'healthy':
                        result = db_requests.select_healthy_product(data_select)
                    else: # sport
                        result = db_requests.select_sport_product(data_select)

                    title = result['title']
                    caption = textbot.add_product[language].format(title, user_text)

                    try:
                        bot.editMessageCaption(chat_id=user_id, caption=caption, parse_mode='HTML',
                                               message_id=delivery_object.user_product[user_id]['message_id'])
                    except Exception:
                        pass

                    try:
                        bot.delete_message(chat_id=user_id, message_id=delivery_object.user_product[user_id]['message_id'] + 1)
                    except Exception:
                        pass

                    try:
                        bot.delete_message(chat_id=user_id, message_id=message_id)
                    except Exception:
                        pass

                    text_more = textbot.more[language]
                    keyboard_more = keyboardbot.main_menu[language]
                    bot.send_message(chat_id=user_id, text=text_more, parse_mode='HTML',
                                     reply_markup=ReplyKeyboardMarkup(keyboard_more, resize_keyboard=True))

                    delivery_object.add_parameters(bot, update)
                    delivery_object.add_basket(bot, update)

                else:
                    text = textbot.not_integer[language]
                    bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')

                return

        if delivery_object.promocode_form.get(user_id): # при вводе помокода
            user_db = db_requests.select_user({'user_id': user_id})
            language = user_db['language']
            user_text = user_text.upper()

            if delivery_object.promocode_form[user_id]['promocode'] is None:
                if user_text in delivery_object.promocode_form[user_id]['list_of_promocodes']: # если пытается добавить повторно
                    text = textbot.promocode_already[language]
                    bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
                    return

                promocode = db_requests.select_promocode_by_user({'promocode': user_text, 'user_id_id': user_db['id']})
                if promocode: # если уже активирован пользователем
                    text = textbot.promocode_used[language]
                    bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
                    return

                promocode = main_object.check_promocode_not_exist({'promocode': user_text})
                if promocode: # если не существует или не активен
                    text = textbot.promocode_not_exist[language]
                    bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
                    return

                text = textbot.promocode_apply[language]
                bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')

                delivery_object.promocode_form[user_id]['promocode'] = 'None'
                delivery_object.promocode_form[user_id]['list_of_promocodes'].append(user_text)
                main_object.basket(bot, update)


        if self.partnership_form.get(user_id): # при заполнение заявки на партнерку
            if self.partnership_form[user_id]['brand_name'] is None:
                self.partnership_form[user_id]['brand_name'] = user_text
                main_object.partnership_full_name(bot, update)
                return

            elif self.partnership_form[user_id]['full_name'] is None:
                self.partnership_form[user_id]['full_name'] = user_text
                main_object.partnership_contact(bot, update)
                return

            elif self.partnership_form[user_id]['contact'] is None:
                date = re.match(r'^(9989\d{8})$', user_text)
                if date:
                    self.partnership_form[user_id]['contact'] = '+{}'.format(user_text)
                    main_object.partnership_document(bot, update)
                else:
                    main_object.partnership_contact(bot, update)

                return

            elif self.partnership_form[user_id]['comment'] is None:
                self.partnership_form[user_id]['comment'] = user_text
                main_object.partnership_done(bot, update)
                return


        if self.registration_form.get(user_id): # при регистрации
            if self.registration_form[user_id]['contact'] is None:
                date = re.match(r'^(9989\d{8})$', user_text)
                if date:
                    self.registration_form[user_id]['contact'] = '+{}'.format(user_text)
                    main_object.insert_user(bot, update)
                    return
                else:
                    main_object.contact(bot, update)


        if self.mailing_form.get(user_id): # рассылка
            if self.mailing_form[user_id]['text'] is None:
                if len(user_text) <= 4000:
                    self.mailing_form[user_id]['text'] = user_text

                    text = textbot.mailing_photo
                    keyboard = keyboardbot.mailing_photo

                    bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                                     reply_markup=InlineKeyboardMarkup(keyboard))
                else:
                    text = textbot.mailing_error
                    bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
                return


    def filter_location(self, bot, update):
        """Фильтр локации"""
        user_id = update_data.user_id(update)
        location = update_data.location(update)

        if delivery_object.user_order_form.get(user_id): # при заказе
            if 'location' in delivery_object.user_order_form[user_id]:
                if delivery_object.user_order_form[user_id]['location'] is None:
                    delivery_object.user_order_form[user_id]['location'] = location
                    main_object.type_payment(bot, update)
                    return


    def filter_contact(self, bot, update):
        """Фильтр контакта"""
        user_id = update_data.user_id(update)
        contact = update_data.contact(update)

        if self.partnership_form.get(user_id): # при заполнение заявки на партнерку
            if self.partnership_form[user_id]['contact'] is None:
                self.partnership_form[user_id]['contact'] = contact
                main_object.partnership_document(bot, update)
                return


        if self.registration_form.get(user_id): # при регистрации
            if self.registration_form[user_id]['contact'] is None:
                self.registration_form[user_id]['contact'] = contact
                main_object.insert_user(bot, update)
                return


    def filter_photo(self, bot, update):
        """Фильтр фото"""
        user_id = update_data.user_id(update)
        photo = update_data.photo_file_id(update)

        if self.partnership_form.get(user_id): # при заполнение заявки на партнерку
            if self.partnership_form[user_id]['document'] is None:
                self.partnership_form[user_id]['document'] = photo
                self.partnership_form[user_id]['exp'] = 'png'
                main_object.partnership_done(bot, update)
                return


        if self.mailing_form.get(user_id):  # рассылка
            if self.mailing_form[user_id]['photo_id'] is None:
                self.mailing_form[user_id]['photo_id'] = photo
                main_object.done_mailing(bot, update)
                return


    def filter_document(self, bot,update):
        """Фильтр документа"""
        user_id = update_data.user_id(update)
        document = update_data.document(update)
        document_exp = update_data.document_exp(update)

        if self.partnership_form.get(user_id): # при заполнение заявки на партнерку
            if self.partnership_form[user_id]['document'] is None:
                self.partnership_form[user_id]['document'] = document
                self.partnership_form[user_id]['exp'] = document_exp
                main_object.partnership_done(bot, update)
                return

# ФИЛЬТРЫ


# ПРОМОКОД
    @staticmethod
    def check_promocode_not_exist(data):
        """Проверка промокода на существование"""
        healthy = db_requests.select_promocode_healhty({'promocode': data['promocode'], 'status': 1})
        sport = db_requests.select_promocodesport({'promocode': data['promocode'], 'status': 1})
        brand = db_requests.select_promocode_brand({'promocode': data['promocode'], 'status': 1})

        if healthy or sport or brand:
            return False
        else:
            return True

    @staticmethod
    def promo_code(bot, update):
        """Генерация промокода"""
        user_id = update_data.user_id(update)

        db_admin = db_requests.select_user_admin({'user_id': user_id})
        if db_admin:
            while True:
                new_promo = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(config.promo_size)).upper()
                promo_not_exist = db_requests.select_promo({'promocode': new_promo})

                if promo_not_exist:
                    bot.send_message(chat_id=user_id, text=textbot.promo_generate.format(new_promo), parse_mode='HTML')
                    return
# ПРОМОКОД


# РАССЫЛКА
    def send(self, bot, update):
        """Рассылка"""
        user_id = update_data.user_id(update)

        db_admin = db_requests.select_user_admin({'user_id': user_id})
        if db_admin:
            self.mailing_form[user_id] = {'text': None}

            text = textbot.mailing

            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')


    def mail_decline(self, bot, update):
        """Отмена рассылки"""
        user_id = query_data.user_id(update)
        message_id = query_data.message_id(update)
        text = textbot.decline_mailing
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=text)

        self.mailing_form.pop(user_id, None)


    def mailing_photo_status(self, bot, update):
        """Статус фото к рассылке"""
        user_id = query_data.user_id(update)
        message_id = query_data.message_id(update)
        data = query_data.data(update)

        callback_query_id = query_data.callback_query_id(update)
        bot.answer_callback_query(callback_query_id=callback_query_id)

        if data == 'mailing_photo_yes':
            self.mailing_form[user_id]['photo_id'] = None
            bot.delete_message(chat_id=user_id, message_id=message_id)

            text = textbot.mailing_photo_yes
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')

        else:
            main_object.done_mailing(bot, update)


    def done_mailing(self, bot, update):
        """Закончить форму рассылки"""
        try:
            user_id = update_data.user_id(update)
        except Exception:
            user_id = query_data.user_id(update)

        text = textbot.mailing_form
        text_mailing = self.mailing_form[user_id]['text']
        keyboard = keyboardbot.mailing_send

        if 'photo_id' in self.mailing_form[user_id]:
            photo_id = self.mailing_form[user_id]['photo_id']

            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
            bot.send_photo(chat_id=user_id, photo=photo_id, caption=text_mailing, parse_mode='HTML',
                           reply_markup=InlineKeyboardMarkup(keyboard))

        else:
            message_id = query_data.message_id(update)
            bot.delete_message(chat_id=user_id, message_id=message_id)
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
            bot.send_message(chat_id=user_id, text=text_mailing, parse_mode='HTML',
                             reply_markup=InlineKeyboardMarkup(keyboard))


    def start_mailing(self, bot, update):
        """Начать рассылку"""
        user_id = query_data.user_id(update)
        message_id = query_data.message_id(update)
        data = query_data.data(update)

        if data == 'mailing_send_yes':
            text = textbot.accept_mailing

            try:
                bot.editMessageCaption(chat_id=user_id, message_id=message_id, parse_mode='HTML',
                                       caption=text)
            except Exception:
                bot.edit_message_text(chat_id=user_id, message_id=message_id, parse_mode='HTML',
                                      text=text)

            main_object.mailing_users(bot, update)
        else:
            text = textbot.decline_mailing
            self.mailing_form.pop(user_id, None)

            try:
                bot.editMessageCaption(chat_id=user_id, message_id=message_id, parse_mode='HTML',
                                       caption=text)
            except Exception:
                bot.edit_message_text(chat_id=user_id, message_id=message_id, parse_mode='HTML',
                                      text=text)


    def mailing_users(self, bot, update):
        """Рассылка цикл"""
        user_id = query_data.user_id(update)
        db_users = db_requests.select_users()

        text_mailing = self.mailing_form[user_id]['text']

        if db_users is not None:
            if 'photo_id' in self.mailing_form[user_id]:
                photo_id = self.mailing_form[user_id]['photo_id']
                for user in db_users:
                    try:
                        bot.send_photo(chat_id=user['user_id'], photo=photo_id, caption=text_mailing, parse_mode='HTML')
                        sleep(0.3)
                    except Exception:
                        pass

            else:
                for user in db_users:
                    try:
                        bot.send_message(chat_id=user['user_id'], text=text_mailing, parse_mode='HTML')
                        sleep(0.3)
                    except Exception:
                        pass

        self.mailing_form.pop(user_id, None)
# РАССЫЛКА


main_object = MainBot()
########################################################################################################################


class Delivery:
    """Корзина и заказы"""
    def __init__(self):
        self.user_basket_healthy = {}
        self.user_basket_sport = {}
        self.user_product = {}
        self.user_order_form = {}
        self.promocode_form = {}


# КОРЗИНА
    def basket(self, bot, update):
        """Корзина"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        self.user_order_form.pop(user_id, None)

        basket_bill_menu = ''
        full_price_menu = 0

        if self.user_basket_healthy.get(user_id):
            basket_bill = delivery_object.calculate(bot, update, kind_product='healthy')

            full_price_menu += basket_bill['full_price']
            basket_bill_menu += textbot.basket_bill_healthy[language].format(basket_bill_menu=basket_bill['bill'])

        if self.user_basket_sport.get(user_id):
            basket_bill = delivery_object.calculate(bot, update, kind_product='sport')

            full_price_menu += basket_bill['full_price']
            basket_bill_menu += textbot.basket_bill_sport[language].format(basket_bill_menu=basket_bill['bill'])


        if basket_bill_menu == '':
            text = textbot.empty_basket[language]
            keyboard = keyboardbot.main_menu[language]
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        else:
            full_price = full_price_menu
            text = textbot.basket_bill[language].format(bill=basket_bill_menu, full_price=full_price)
            if self.promocode_form.get(user_id):
                text += '\n{}'.format(textbot.basket_bill_promo[language])
            keyboard = keyboardbot.basket[language]

            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


    def calculate(self, bot, update, kind_product=None):
        """Рассчет корзины здорового питания"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        bill = ''
        full_price = 0

        if kind_product == 'healthy':
            data = self.user_basket_healthy[user_id]
        else: # sport
            data = self.user_basket_sport[user_id]

        for id_category in data:
            if kind_product == 'healthy':
                title = db_requests.select_healthy_category({'id': id_category, 'language': language})['title']
            else:
                title = db_requests.select_sport_category({'id': id_category, 'language': language})['title']

            bill += "\n\n<b>{}</b>".format(title)
            for product in data[id_category]:
                if self.promocode_form.get(user_id):
                    promocodes = self.promocode_form[user_id]
                else:
                    promocodes = None

                discount = delivery_object.calculate_discount({'product': product, 'price': data[id_category][product]['price'], 'promocodes': promocodes, 'kind_product': kind_product})
                full_price += data[id_category][product]['count'] * discount

                bill += '''\n{title} - <code>{count}</code> x <code>{price}</code> сум'''.format(
                    title=data[id_category][product]['title'],
                    count=data[id_category][product]['count'],
                    price=data[id_category][product]['price'])

        data = {'bill': bill, 'full_price': full_price}

        return data


    @staticmethod
    def calculate_discount(parameters):
        """Рассчет суммы продукта с скидкой"""
        promocodes = parameters['promocodes']
        price = parameters['price']

        if promocodes:
            product = int(parameters['product'])
            kind_product = parameters['kind_product']

            for promocode in promocodes['list_of_promocodes']:
                if kind_product == 'healthy':
                    healthy = db_requests.select_discount_health({'promocode': promocode, 'status': 1, 'id': product})
                    if healthy:
                        price = int(price * (1 - healthy['discount'] / 100))

                else: # sport
                    sport = db_requests.select_discount_sport({'promocode': promocode, 'status': 1, 'id': product})
                    if sport:
                        price = int(price * (1 - sport['discount'] / 100))

                brand = db_requests.select_discount_brand({'promocode': promocode, 'status': 1, 'id': product})
                if brand:
                    price = int(price * (1 - brand['discount'] / 100))

            return price

        return price


    def clear_basket(self, bot, update):
        """Очистить корзину"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        self.user_basket_healthy.pop(user_id, None)
        self.user_basket_sport.pop(user_id, None)
        self.promocode_form.pop(user_id, None)

        text = textbot.clear_basket[language]
        keyboard = keyboardbot.main_menu[language]

        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


    def promocode(self, bot, update):
        """Промокод"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        if delivery_object.user_basket_healthy.get(user_id) or delivery_object.user_basket_sport.get(user_id):
            if self.promocode_form.get(user_id):
                self.promocode_form[user_id]['promocode'] = None
            else:
                self.promocode_form[user_id] = {'promocode': None, 'list_of_promocodes': []}

            text = textbot.promocode[language]
            keyboard = keyboardbot.cancel[language]

            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                             reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

        else:
            delivery_object.basket(bot, update)
            main_object.start(bot, update)


    def cancel(self, bot, update):
        """Отмена промокода"""
        user_id = update_data.user_id(update)

        if self.promocode_form.get(user_id):
            if self.promocode_form[user_id] == {'promocode': None, 'list_of_promocodes': []}:
                self.promocode_form.pop(user_id, None)
            else:
                self.promocode_form[user_id]['promocode'] = 'None'

        main_object.basket(bot, update)
# КОРЗИНА


# ДОБАВЛЕНИЕ ПРОДУКТА
    def add_product(self, bot, update):
        """Добавить продукт"""
        user_id = query_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        message_id = query_data.message_id(update)
        data = query_data.data(update).split('_')

        callback_query_id = query_data.callback_query_id(update)
        bot.answer_callback_query(callback_query_id=callback_query_id)

        self.user_product[user_id] = {'product': data[-1], 'type': data[2], 'count': None, 'message_id': message_id, 'kind': data[1]}
        caption = textbot.count_product[language]

        bot.editMessageCaption(chat_id=user_id, message_id=message_id, parse_mode='HTML',
                               caption=caption, reply_markup=InlineKeyboardMarkup([]))

        text_count = textbot.count_product_mark
        keyboard_count = deepcopy(keyboardbot.count_product)
        keyboard_count.append([keyboardbot.d_menu[language]['main_menu']])
        bot.send_message(chat_id=user_id, text=text_count, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard_count, resize_keyboard=True))


    def add_parameters(self, bot, update):
        """Добавление параметров продукта"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        data_menu = {'product_id': self.user_product[user_id]['product'], 'language': language}

        if self.user_product[user_id]['kind'] == 'healthy':
            result = db_requests.select_healthy_product(data_menu)
        else: # sport
            result = db_requests.select_sport_product(data_menu)

        if result is None:
            try:
                bot.delete_message(chat_id=user_id, message_id=self.user_product[user_id]['message_id'])
            except Exception:
                pass
            text = textbot.product_none[language]
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
            self.user_product.pop(user_id, None)
            return

        self.user_product[user_id]['title'] = result['title']
        self.user_product[user_id]['price'] = result['price']


    def add_basket(self, bot, update):
        """Добавление в корзину"""
        user_id = update_data.user_id(update)
        data = self.user_product[user_id]

        if self.user_product[user_id]['kind'] == 'healthy':
            data_basket = self.user_basket_healthy
        else: # sport
            data_basket = self.user_basket_sport

        if data_basket.get(user_id): # если уже есть продукты в корзине
            if data['type'] in data_basket[user_id]: # если продукт из тоже же категории
                if data['product'] in data_basket[user_id][data['type']]: # если продукт уже в корзине
                    data_basket[user_id][data['type']][data['product']]['count'] = data_basket[user_id][data['type']][data['product']]['count'] + data['count']
                else: # добавить новый продукт
                    data_basket[user_id][data['type']][data['product']] = {'count': data['count'],
                                                                           'title': data['title'],
                                                                           'price': data['price']}
            else: # добавить новую категорию
                data_basket[user_id][data['type']] = {data['product']: {'count': data['count'],
                                                                        'title': data['title'],
                                                                        'price': data['price']}}
        else: # создается новая корзина
            data_basket[user_id] = {data['type']: {data['product']: {'count': data['count'],
                                                                     'title': data['title'],
                                                                     'price': data['price']}}}

        self.user_product.pop(user_id, None)
# ДОБАВЛЕНИЕ ПРОДУКТА


# ЗАКАЗ
    def type_delivery(self, bot, update):
        """Выбор типа доставки"""
        user_id = update_data.user_id(update)
        button_name = update_data.text(update)

        if delivery_object.user_basket_healthy.get(user_id) or delivery_object.user_basket_sport.get(user_id):
            d_type = {keyboardbot.d_type_delivery['ru']['self']: 'self', keyboardbot.d_type_delivery['uz']['self']: 'self',
                      keyboardbot.d_type_delivery['ru']['delivery']: 'delivery', keyboardbot.d_type_delivery['uz']['delivery']: 'delivery'}

            self.user_order_form[user_id] = {'type_delivery': d_type[button_name]}

            if self.user_order_form[user_id]['type_delivery'] == 'self':
                main_object.type_payment(bot, update)

            else:
                main_object.location(bot, update)
        else:
            delivery_object.basket(bot, update)
            main_object.start(bot, update)


    def send_order(self, bot, update):
        """Отправка заявки в канал"""
        user_id = update_data.user_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']
        order_form = self.user_order_form[user_id]
        self.user_order_form.pop(user_id, None)

        basket_bill_menu = ''
        full_price_menu = 0

        if self.user_basket_healthy.get(user_id):
            basket_bill = delivery_object.calculate(bot, update, kind_product='healthy')

            full_price_menu += basket_bill['full_price']
            basket_bill_menu += textbot.basket_bill_healthy[language].format(basket_bill_menu=basket_bill['bill'])

        if self.user_basket_sport.get(user_id):
            basket_bill = delivery_object.calculate(bot, update, kind_product='sport')

            full_price_menu += basket_bill['full_price']
            basket_bill_menu += textbot.basket_bill_sport[language].format(basket_bill_menu=basket_bill['bill'])


        type_delivery = {'self': 'Самовывоз', 'delivery': 'Доставка'}
        type_payment = {'cash': 'Наличные', 'payme': 'PayMe'}
        db_user = db_requests.select_user({'user_id': user_id})
        count_order = db_requests.select_update_count_order()


        ### клиенту ###
        text = textbot.order_done[language].format(count_order=count_order,
                                                   contact=db_user['contact'],
                                                   type_payment=type_payment[order_form['type_payment']],
                                                   type_delivery=type_delivery[order_form['type_delivery']],
                                                   basket_bill_menu=basket_bill_menu,
                                                   full_price_menu=full_price_menu
                                                   )

        if self.promocode_form.get(user_id):
            text += '\n{}'.format(textbot.basket_bill_promo[language])

        keyboard = keyboardbot.main_menu[language]
        bot.send_message(chat_id=user_id, text=text, parse_mode='HTML',
                         reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        ### клиенту ###


        ### админу ###
        text = textbot.send_order.format(count_order=count_order,
                                         user_id=user_id, first_name=db_user['first_name'],
                                         contact=db_user['contact'], basket_bill_menu=basket_bill_menu,
                                         full_price_menu=full_price_menu,
                                         type_payment=type_payment[order_form['type_payment']],
                                         type_delivery=type_delivery[order_form['type_delivery']])

        if self.promocode_form.get(user_id):
            text += '\n{}'.format(textbot.basket_bill_promo['ru'])

        keyboard = keyboardbot.status_order
        box = bot.send_message(chat_id=config.id_channel, text=text, parse_mode='HTML',
                               reply_markup=InlineKeyboardMarkup(keyboard))

        if 'location' in order_form:
            bot.send_location(chat_id=config.id_channel,
                              latitude=order_form['location']['latitude'],
                              longitude=order_form['location']['longitude'])
        ### админу ###


        data = {'count': count_order,
                'user_id': user_id,
                'first_name': db_user['first_name'],
                'contact': db_user['contact'],
                'order_text': basket_bill_menu,
                'full_price': full_price_menu,
                'date': (d.datetime.now() + d.timedelta(hours=config.time_zone)).strftime("%d.%m.%y / %H:%M"),
                'status': 0,
                'message_id_chat': box['message_id'],
                'type_payment': order_form['type_payment'],
                'type_delivery': order_form['type_delivery']
                }

        db_requests.insert_new_order(data)

        if self.promocode_form.get(user_id):
            db_requests.insert_promo_user({'user_id_id': db_user['id'], 'list_of_promocodes': self.promocode_form[user_id]['list_of_promocodes'],
                                           'date_time': (d.datetime.today() + d.timedelta(hours=config.time_zone)).strftime("%d.%m.%y/%H:%M")})

            db_requests.update_decrement_promo({'list_of_promocodes': self.promocode_form[user_id]['list_of_promocodes']})


        # добавить в статистику партнерки
        if self.user_basket_healthy.get(user_id):
            healthy_basket = self.user_basket_healthy[user_id]
        else:
            healthy_basket = None

        if self.user_basket_sport.get(user_id):
            sport_basket = self.user_basket_sport[user_id]
        else:
            sport_basket = None


        db_requests.insert_partnership_statistic({'sport_basket': sport_basket, 'healthy_basket': healthy_basket,
                                                  'date_time': (d.datetime.today() + d.timedelta(hours=config.time_zone)).strftime("%d.%m.%y/%H:%M")})
        # добавить в статистику партнерки


        self.promocode_form.pop(user_id, None)
        self.user_basket_healthy.pop(user_id, None)
        self.user_basket_sport.pop(user_id, None)


    @staticmethod
    def accept_order(bot, update):
        """Подтверждение заказа"""
        user_id = query_data.user_id(update)
        message_id = query_data.message_id(update)
        data = query_data.data(update)
        user_data = db_requests.select_order_data(message_id)
        language = db_requests.select_user({'user_id': user_data['user_id']})['language']


        if data == 'decline_order':
            keyboard = [[InlineKeyboardButton(textbot.decline_order, callback_data='None')]]
            bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id,
                                          reply_markup=InlineKeyboardMarkup(keyboard))
            status = 3
            text = textbot.decline_order_user[language].format(count_order=user_data['count_order'])
        else:
            if user_data['type_payment'] in ['payme']:
                keyboard = [[InlineKeyboardButton(textbot.wait_order, callback_data='None')],
                            [InlineKeyboardButton(keyboardbot.d_status_order['decline_order'], callback_data='decline_order')]]
                bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id,
                                              reply_markup=InlineKeyboardMarkup(keyboard))
                status = 2

                data_order = {'message_id_chat': message_id, 'status': status}
                db_requests.update_order_status(data_order)

                delivery_object.send_invoice(bot, update)
                return

            else:
                keyboard = [[InlineKeyboardButton(textbot.accept_order, callback_data='None')],
                            [InlineKeyboardButton(keyboardbot.d_status_order['decline_order'], callback_data='decline_order')]]
                bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id,
                                              reply_markup=InlineKeyboardMarkup(keyboard))
                status = 1
                text = textbot.accept_order_user[language].format(count_order=user_data['count_order'])

        data_order = {'message_id_chat': message_id, 'status': status}
        db_requests.update_order_status(data_order)

        try:
            bot.send_message(chat_id=user_data['user_id'], text=text, parse_mode='HTML')
        except Exception:
            pass


    @staticmethod
    def send_invoice(bot, update):
        """Отправить оплату"""
        message_id = query_data.message_id(update)
        order_db = db_requests.select_order_data(message_id)
        user_id = order_db['user_id']
        language = db_requests.select_user({'user_id': user_id})['language']


        payment_token = config.token_payment[order_db['type_payment']]
        payload = "{}_{}".format(order_db['user_id'], message_id)
        pay_bill = order_db['full_price']
        label = textbot.label[language]
        title = textbot.title[language].format(count_order=order_db['count_order'])
        description = textbot.description[language]
        currency = "UZS"
        # 100,00 сто сум 0 тиин
        price = 100 * pay_bill
        bot.send_invoice(chat_id=user_id, title=title, description=description,
                         payload=payload,
                         provider_token=payment_token, start_parameter='None', currency=currency,
                         prices=[LabeledPrice(label=label, amount=price)])


    @staticmethod
    def pre_checkout_callback(bot, update):
        """Пречек оплаты"""
        user_id = query_data.pre_checkout_user_id(update)
        invoice_payload = query_data.pre_checkout_invoice_payload(update).split('_')
        db_order = db_requests.select_order_data(invoice_payload[-1])
        language = db_requests.select_user({'user_id': user_id})['language']
        pre_checkout_query_id = query_data.pre_checkout_query_id(update)

        try:
            if db_order and (invoice_payload[0] == str(user_id)):
                bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query_id, ok=True)

            else:
                bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query_id, ok=False,
                                              error_message=textbot.error_payment[language])
        except Exception:
            bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query_id, ok=False,
                                          error_message=textbot.error_payment[language])


    @staticmethod
    def successful_payment_callback(bot, update):
        """При выполненой оплате"""
        user_id = update_data.chat_id(update)
        language = db_requests.select_user({'user_id': user_id})['language']

        invoice_payload = update_data.invoice_payload(update)
        message_id_chat = invoice_payload.split('_')[-1]
        db_order = db_requests.select_order_data(message_id_chat)

        ### админу ###
        keyboard = [[InlineKeyboardButton(textbot.accept_order, callback_data='None')],
                    [InlineKeyboardButton(keyboardbot.d_status_order['decline_order'], callback_data='decline_order')]]
        bot.edit_message_reply_markup(chat_id=config.id_channel, message_id=message_id_chat,
                                      reply_markup=InlineKeyboardMarkup(keyboard))

        text = textbot.payed_order.format(count_order=db_order['count_order'])
        bot.send_message(chat_id=config.id_channel, text=text, parse_mode='HTML')
        ### админу ###


        ### клиенту ###
        try:
            text = textbot.invoice_done[language].format(count_order=db_order['count_order'])
            bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')
        except Exception:
            pass
        ### клиенту ###


        data_order = {'message_id_chat': message_id_chat, 'status': 1}
        db_requests.update_order_status(data_order)
# ЗАКАЗ


delivery_object = Delivery()