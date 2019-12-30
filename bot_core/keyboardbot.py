from telegram import KeyboardButton, InlineKeyboardButton
################################################
# АДМИН
################################################

# РАССЫЛКА
mailing_photo = [[InlineKeyboardButton("✅ Да", callback_data='mailing_photo_yes'), InlineKeyboardButton("❌ Нет", callback_data='mailing_photo_no')],
                 [InlineKeyboardButton('Отмена', callback_data='mail_decline')]]

mailing_send = [[InlineKeyboardButton("❌ Отмена", callback_data='mailing_send_no')], [InlineKeyboardButton("📨 Начать", callback_data='mailing_send_yes')]]
# РАССЫЛКА
################################################
# ПОЛЬЗОВАТЕЛЬ
################################################

# КНОПКИ
d_language = {'ru': "🇷🇺 Русский",
              'uz': "🇺🇿 Узбекский"
              }

d_menu = {'ru': {'products': "💪 Продукция",
                 'about': "☎ О нас",
                 'news': "❓ Новости",
                 'actions': "🎁 Акции",
                 'main_menu': "⬅ Главное меню",
                 'change_language': "🇷🇺🔄🇺🇿 Сменить язык",
                 'basket': "🛒 Корзина",
                 'partnership': "🤝 Партнерка",
                 'cancel': "❌ Отмена"},

          'uz': {'products': "💪 Продукция",
                 'about': "☎ О нас",
                 'news': "❓ Новости",
                 'actions': "🎁 Акции",
                 'main_menu': "⬅ Главное меню",
                 'change_language': "🇺🇿🔄🇷🇺 Сменить язык",
                 'basket': "🛒 Корзина",
                 'partnership': "🤝 Партнерка",
                 'cancel': "❌ Отмена"}
          }

d_action = {'ru': {'next': "Далее ➡", 'back': "⬅ Назад"},
            'uz': {'next': "Далее ➡", 'back': "⬅ Назад"}
            }

d_products = {'ru': {'healthy': "🥦 Здоровое питание", 'sport': "🏋️‍♂️Спортвиное питание"},
              'uz': {'healthy': "🥦 Здоровое питание", 'sport': "🏋️‍♂️Спортвиное питание"}
              }

back = {'ru': "⬅ Назад",
        'uz': "⬅ Назад"}

add_basket = {'ru': '''🛒 Добавить в корзину''',
              'uz': '''🛒 Добавить в корзину'''}


d_basket = {'ru': {'clear_basket': "❌ Очистить корзину", 'order': "🚗 Заказать", 'promocode': "🔲 Промокод"},
            'uz': {'clear_basket': "❌ Очистить корзину", 'order': "🚗 Заказать", 'promocode': "🔲 Промокод"}
            }

d_partnership = {'ru': {'statistic': "📊 Статистика", 'application': "✏ Оставить заявку", 'info': "❓ О партнерстве"},
                 'uz': {'statistic': "📊 Статистика", 'application': "✏ Оставить заявку", 'info': "❓ О партнерстве"}
                 }

d_contact = {'ru': {'location': "📍 Поделиться локацией", 'contact': "📞 Поделиться контактом"},
             'uz': {'location': "📍 Поделиться локацией", 'contact': "📞 Поделиться контактом"}
             }

d_type_delivery = {'ru': {'self': "✋ Самовывоз", 'delivery': "🚗 Доставка"},
                   'uz': {'self': "✋ Самовывоз", 'delivery': "🚗 Доставка"}
                   }

d_type_payment = {'ru': {'cash': "💵 Наличные", 'payme': "💳 PayMe"},
                  'uz': {'cash': "💵 Наличные", 'payme': "💳 PayMe"}}

d_status_order = {'accept_order': "✅ Принять", 'decline_order': "❌ Отклонить"}
# КНОПКИ

################################################

# ЯЗЫК
language = [[d_language['uz']],
            [d_language['ru']]
            ]
# ЯЗЫК


# МЕНЮ
main_menu = {'ru': [[d_menu['ru']['products']],
                    [d_menu['ru']['about'], d_menu['ru']['basket']],
                    [d_menu['ru']['news'], d_menu['ru']['actions']],
                    [d_menu['ru']['partnership']],
                    [d_menu['ru']['change_language']]
                    ],

             'uz': [[d_menu['uz']['products']],
                    [d_menu['uz']['about'], d_menu['uz']['basket']],
                    [d_menu['uz']['news'], d_menu['uz']['actions']],
                    [d_menu['uz']['partnership']],
                    [d_menu['uz']['change_language']]
                    ],
             }
# МЕНЮ


# ПРОДУКТЫ
products = {'ru': [[d_products['ru']['healthy'], d_products['ru']['sport']],
                   [d_menu['ru']['main_menu']]
                   ],

            'uz': [[d_products['ru']['healthy'], d_products['ru']['sport']],
                   [d_menu['ru']['main_menu']]
                   ],
            }

back_category_healthy = {'ru': [InlineKeyboardButton(back['ru'], callback_data='back_category_healthy')],
                         'uz': [InlineKeyboardButton(back['uz'], callback_data='back_category_healthy')]
                         }

back_category_sport = {'ru': [InlineKeyboardButton(back['ru'], callback_data='back_category_sport')],
                       'uz': [InlineKeyboardButton(back['uz'], callback_data='back_category_sport')]
                       }
# ПРОДУКТЫ


# ДОБАВЛЕНИЕ ПРОДУКТА
count_product = [['1', '2', '3'],
                 ['4', '5', '6'],
                 ['7', '8', '9']]

basket = {'ru': [[d_basket['ru']['order']],
                 [d_basket['ru']['clear_basket'], d_basket['ru']['promocode']],
                 [d_menu['ru']['main_menu']]],

          'uz': [[d_basket['uz']['order']],
                 [d_basket['uz']['clear_basket'], d_basket['uz']['promocode']],
                 [d_menu['uz']['main_menu']]]
          }

cancel = {'ru': [[d_menu['ru']['cancel']]
                 ],

          'uz': [[d_menu['uz']['cancel']]
                 ],
          }
# ДОБАВЛЕНИЕ ПРОДУКТА


# ПАРТНЕРКА
partnership = {'ru': [[d_partnership['ru']['application']],
                      [d_partnership['ru']['info']],
                      [d_menu['ru']['main_menu']]
                      ],

               'uz': [[d_partnership['uz']['application']],
                      [d_partnership['uz']['info']],
                      [d_menu['uz']['main_menu']]
                      ]
               }


partnership_already = {'ru': [[d_partnership['ru']['info']],
                              [d_menu['ru']['main_menu']]
                              ],

                       'uz': [[d_partnership['uz']['info']],
                              [d_menu['uz']['main_menu']]
                              ]
                       }

partnership_statistic = {'ru': [[d_partnership['ru']['statistic']],
                                [d_partnership['ru']['info']],
                                [d_menu['ru']['main_menu']]
                                ],

                         'uz': [[d_partnership['ru']['statistic']],
                                [d_partnership['uz']['info']],
                                [d_menu['uz']['main_menu']]
                                ]
                       }
# ПАРТНЕРКА


# КОНТАКТЫ
contact = {'ru': [[KeyboardButton(d_contact['ru']['contact'], request_contact=True)],
                  [d_menu['ru']['main_menu']]
                  ],
           'uz': [[KeyboardButton(d_contact['uz']['contact'], request_contact=True)],
                  [d_menu['uz']['main_menu']]
                  ]
           }

location = {'ru': [[KeyboardButton(d_contact['ru']['location'], request_location=True)],
                   [d_menu['ru']['basket']],
                   [d_menu['ru']['main_menu']]
                  ],

           'uz': [[KeyboardButton(d_contact['uz']['location'], request_location=True)],
                  [d_menu['ru']['basket']],
                  [d_menu['uz']['main_menu']]
                  ]
           }
# КОНТАКТЫ


# ЗАКАЗ
type_delivery = {'ru': [[d_type_delivery['ru']['self'], d_type_delivery['ru']['delivery']],
                        [d_menu['ru']['basket']],
                        [d_menu['ru']['main_menu']]
                        ],

                 'uz': [[d_type_delivery['uz']['self'], d_type_delivery['uz']['delivery']],
                        [d_menu['uz']['basket']],
                        [d_menu['uz']['main_menu']]
                        ]
                 }

type_payment = {'ru': [[d_type_payment['ru']['cash'], d_type_payment['ru']['payme']],
                       [d_menu['ru']['basket']],
                       [d_menu['ru']['main_menu']]
                       ],

                'uz': [[d_type_payment['uz']['cash'], d_type_payment['uz']['payme']],
                       [d_menu['ru']['basket']],
                       [d_menu['ru']['main_menu']]
                       ]
                }

status_order = [[InlineKeyboardButton(d_status_order['accept_order'], callback_data='accept_order')],
                [InlineKeyboardButton(d_status_order['decline_order'], callback_data='decline_order')]]
# ЗАКАЗ