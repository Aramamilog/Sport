from bot import main_object, delivery_object
from concurrent.futures import ThreadPoolExecutor
from bot_core.dict_keyboard import dict_update
from bot_core.bot_scheduler import schedule_start


# Запуск отдельных потоков
pool = ThreadPoolExecutor(max_workers=20)


#СТАРТ
def thread_start(bot, update):
    """Старт бота"""
    pool.submit(main_object.start, bot, update)
# СТАРТ


# КАСТОМНАЯ КЛАВИАТУРА
def thread_start_update(bot, update):
    """Запуск потоков reply клавиатуры"""
    update_user = update.message.text
    pool.submit(dict_update[update_user], bot, update)
# КАСТОМНАЯ КЛАВИАТУРА


# АКЦИИ
def thread_action_switch(bot, update):
    """Переключение акций"""
    pool.submit(main_object.action_switch, bot, update)
# АКЦИИ


# НОВОСТИ
def thread_news_switch(bot, update):
    """Переключение новостей"""
    pool.submit(main_object.news_switch, bot, update)
# НОВОСТИ


# ПРОДУКТЫ
def thread_healthy(bot, update):
    """Выбор категории здорового питания"""
    pool.submit(main_object.products_healthy, bot, update)

def thread_back_category_healthy(bot, update):
    """Категории - здоровое питание"""
    pool.submit(main_object.healthy, bot, update)

def thread_healthy_product(bot, update):
    """Выбор продукта здоровое питание"""
    pool.submit(main_object.healthy_product, bot, update)


def thread_sport(bot, update):
    """Выбор категории здорового питания"""
    pool.submit(main_object.products_sport, bot, update)

def thread_back_category_sport(bot, update):
    """Категории - здоровое питание"""
    pool.submit(main_object.sport, bot, update)

def thread_sport_product(bot, update):
    """Выбор продукта здоровое питание"""
    pool.submit(main_object.sport_product, bot, update)


def thread_add_product(bot, update):
    """Добавить продукт"""
    pool.submit(delivery_object.add_product, bot, update)
# ПРОДУКТЫ


# PAYMENT
def thread_precheckout_callback(bot, update):
    """Пречек оплаты"""
    pool.submit(delivery_object.pre_checkout_callback, bot, update)

def thread_successful(bot, update):
    """Пречек оплаты"""
    pool.submit(delivery_object.successful_payment_callback, bot, update)
# PAYMENT


# ЗАКАЗЫ
def thread_accept_order(bot, update):
    """Подтверждение заказа"""
    pool.submit(delivery_object.accept_order, bot, update)
# ЗАКАЗЫ


# ПРОМОКОДЫ
def thread_promo_code(bot, update):
    """Генерация промокода"""
    pool.submit(main_object.promo_code, bot, update)
# ПРОМОКОДЫ


# СТАТИСТИКА
def thread_statistic_admin(bot, update):
    """Статистик админу"""
    pool.submit(main_object.statistic_admin, bot, update)
# СТАТИСТИКА


# РАССЫЛКА
def thread_send(bot, update):
    """Рассылка"""
    pool.submit(main_object.send, bot, update)

def mailing_photo(bot, update):
    """Статус фото к рассылке"""
    pool.submit(main_object.mailing_photo_status, bot, update)

def mailing_send(bot, update):
    """Начать рассылку"""
    pool.submit(main_object.start_mailing, bot, update)

def thread_mail_decline(bot, update):
    """Отмена рассылки"""
    pool.submit(main_object.mail_decline, bot, update)
# РАССЫЛКА



# ЗАГЛУШКА
def thread_none_button(bot, update):
    """Обработка кнопок заглушек"""
    pool.submit(main_object.none_button, bot, update)
# ЗАГЛУШКА


# ФИЛЬТРЫ
def thread_filter_text(bot, update):
    """Фильтр текста"""
    pool.submit(main_object.filter_text, bot, update)

def thread_filter_location(bot, update):
    """Фильтр локации"""
    pool.submit(main_object.filter_location, bot, update)

def thread_filter_contact(bot, update):
    """Фильтр контакта"""
    pool.submit(main_object.filter_contact, bot, update)

def thread_filter_photo(bot, update):
    """Фильтр фото"""
    pool.submit(main_object.filter_photo, bot, update)

def thread_filter_document(bot, update):
    """Фильтр документа"""
    pool.submit(main_object.filter_document, bot, update)
# ФИЛЬТРЫ


# SCHEDULER
pool.submit(schedule_start)
# SCHEDULER