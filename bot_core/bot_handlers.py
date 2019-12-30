from config.config import token
from bot_core import thread_pool, filter_bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, PreCheckoutQueryHandler

updater = Updater(token)
upd_dispatcher = updater.dispatcher

# СТАРТ
upd_dispatcher.add_handler(CommandHandler('start', thread_pool.thread_start))
# СТАРТ

# ПРОМОКОДЫ
upd_dispatcher.add_handler(CommandHandler('promo_code', thread_pool.thread_promo_code))
# ПРОМОКОДЫ


# ЯЗЫК
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.language, thread_pool.thread_start_update))
# ЯЗЫК


# МЕНЮ
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.products, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.about, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.news, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.actions, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.main_menu, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.change_language, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.basket, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.partnership, thread_pool.thread_start_update))
# МЕНЮ


# ПРОДУКТЫ
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.healthy, thread_pool.thread_start_update))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_healthy, pattern='^(healthy_)'))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_back_category_healthy, pattern='^(back_category_healthy)'))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_healthy_product, pattern='^(products_healthy_)'))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_add_product, pattern='^(add_healthy_)'))


upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.sport, thread_pool.thread_start_update))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_sport, pattern='^(sport_)'))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_back_category_sport, pattern='^(back_category_sport)'))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_sport_product, pattern='^(products_sport_)'))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_add_product, pattern='^(add_sport_)'))
# ПРОДУКТЫ


# КОРЗИНА
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.clear_basket, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.order, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.promocode, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.cancel, thread_pool.thread_start_update))
# КОРЗИНА


# ЗАКАЗ
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.self, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.delivery, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.cash, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.payme, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.payme, thread_pool.thread_start_update))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_accept_order, pattern='^(accept_order)'))
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_accept_order, pattern='^(decline_order)'))
# ЗАКАЗ


# ПАРТНЕРКА
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.statistic, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.application, thread_pool.thread_start_update))
upd_dispatcher.add_handler(MessageHandler(filter_bot.filter_obj.info, thread_pool.thread_start_update))
# ПАРТНЕРКА


# АКЦИИ
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_action_switch, pattern='^(action_switch_back|action_switch_next)'))
# АКЦИИ


# НОВОСТИ
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_news_switch, pattern='^(news_switch_back|news_switch_next)'))
# НОВОСТИ


# PAYMENT
updater.dispatcher.add_handler(PreCheckoutQueryHandler(thread_pool.thread_precheckout_callback))
updater.dispatcher.add_handler(MessageHandler(Filters.successful_payment, thread_pool.thread_successful))
# PAYMENT


# РАССЫЛКА
updater.dispatcher.add_handler(CommandHandler('send', thread_pool.thread_send))
updater.dispatcher.add_handler(CallbackQueryHandler(thread_pool.mailing_photo, pattern='^(mailing_photo_)'))
updater.dispatcher.add_handler(CallbackQueryHandler(thread_pool.mailing_send, pattern='^(mailing_send_)'))
updater.dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_mail_decline, pattern='^(mail_decline)'))
# РАССЫЛКА


# ЗАГЛУШКА
upd_dispatcher.add_handler(CallbackQueryHandler(thread_pool.thread_none_button, pattern='^(None)$'))
# ЗАГЛУШКА


# ФИЛЬТРЫ
upd_dispatcher.add_handler(MessageHandler(Filters.text, thread_pool.thread_filter_text))
upd_dispatcher.add_handler(MessageHandler(Filters.location, thread_pool.thread_filter_location))
upd_dispatcher.add_handler(MessageHandler(Filters.contact, thread_pool.thread_filter_contact))
upd_dispatcher.add_handler(MessageHandler(Filters.photo, thread_pool.thread_filter_photo))
upd_dispatcher.add_handler(MessageHandler(Filters.document, thread_pool.thread_filter_document))
# ФИЛЬТРЫ


updater.start_polling(poll_interval=0.5, timeout=20)
updater.idle()