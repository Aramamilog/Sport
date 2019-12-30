# -*- coding: utf-8 -*-
from telegram.ext import BaseFilter
from . import keyboardbot as kb


class FilterButton(BaseFilter):
    """Фильтрация по тексту для кнопок"""
# ЯЗЫК
    @staticmethod
    def language(message):
        return (kb.d_language['ru'] in (message.text or '')) or (kb.d_language['uz'] in (message.text or ''))
# ЯЗЫК


# МЕНЮ
    @staticmethod
    def products(message):
        return (kb.d_menu['ru']['products'] in (message.text or '')) or (kb.d_menu['uz']['products'] in (message.text or ''))

    @staticmethod
    def about(message):
        return (kb.d_menu['ru']['about'] in (message.text or '')) or (kb.d_menu['uz']['about'] in (message.text or ''))

    @staticmethod
    def news(message):
        return (kb.d_menu['ru']['news'] in (message.text or '')) or (kb.d_menu['uz']['news'] in (message.text or ''))

    @staticmethod
    def actions(message):
        return (kb.d_menu['ru']['actions'] in (message.text or '')) or (kb.d_menu['uz']['actions'] in (message.text or ''))

    @staticmethod
    def main_menu(message):
        return (kb.d_menu['ru']['main_menu'] in (message.text or '')) or (kb.d_menu['uz']['main_menu'] in (message.text or ''))

    @staticmethod
    def change_language(message):
        return (kb.d_menu['ru']['change_language'] in (message.text or '')) or (kb.d_menu['uz']['change_language'] in (message.text or ''))

    @staticmethod
    def basket(message):
        return (kb.d_menu['ru']['basket'] in (message.text or '')) or (kb.d_menu['uz']['basket'] in (message.text or ''))

    @staticmethod
    def partnership(message):
        return (kb.d_menu['ru']['partnership'] in (message.text or '')) or (kb.d_menu['uz']['partnership'] in (message.text or ''))
# МЕНЮ


# ПРОДУКТЫ
    @staticmethod
    def healthy(message):
        return (kb.d_products['ru']['healthy'] in (message.text or '')) or (kb.d_products['uz']['healthy'] in (message.text or ''))

    @staticmethod
    def sport(message):
        return (kb.d_products['ru']['sport'] in (message.text or '')) or (kb.d_products['uz']['sport'] in (message.text or ''))
# ПРОДУКТЫ


# КОРЗИНА
    @staticmethod
    def clear_basket(message):
        return (kb.d_basket['ru']['clear_basket'] in (message.text or '')) or (kb.d_basket['uz']['clear_basket'] in (message.text or ''))

    @staticmethod
    def order(message):
        return (kb.d_basket['ru']['order'] in (message.text or '')) or (kb.d_basket['ru']['order'] in (message.text or ''))

    @staticmethod
    def promocode(message):
        return (kb.d_basket['ru']['promocode'] in (message.text or '')) or (kb.d_basket['uz']['promocode'] in (message.text or ''))

    @staticmethod
    def cancel(message):
        return (kb.d_menu['ru']['cancel'] in (message.text or '')) or (kb.d_menu['uz']['cancel'] in (message.text or ''))
# КОРЗИНА


# ПАРТНЕРКА
    @staticmethod
    def statistic(message):
        return (kb.d_partnership['ru']['statistic'] in (message.text or '')) or (kb.d_partnership['uz']['statistic'] in (message.text or ''))

    @staticmethod
    def application(message):
        return (kb.d_partnership['ru']['application'] in (message.text or '')) or (kb.d_partnership['uz']['application'] in (message.text or ''))

    @staticmethod
    def info(message):
        return (kb.d_partnership['ru']['info'] in (message.text or '')) or (kb.d_partnership['uz']['info'] in (message.text or ''))
# ПАРТНЕРКА


# ЗАКАЗ
    @staticmethod
    def self(message):
        return (kb.d_type_delivery['ru']['self'] in (message.text or '')) or (kb.d_type_delivery['uz']['self'] in (message.text or ''))

    @staticmethod
    def delivery(message):
        return (kb.d_type_delivery['ru']['delivery'] in (message.text or '')) or (kb.d_type_delivery['uz']['delivery'] in (message.text or ''))

    @staticmethod
    def cash(message):
        return (kb.d_type_payment['ru']['cash'] in (message.text or '')) or (kb.d_type_payment['uz']['cash'] in (message.text or ''))

    @staticmethod
    def payme(message):
        return (kb.d_type_payment['ru']['payme'] in (message.text or '')) or (kb.d_type_payment['uz']['payme'] in (message.text or ''))
# ЗАКАЗ


filter_obj = FilterButton()