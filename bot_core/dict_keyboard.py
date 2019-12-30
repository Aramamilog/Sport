# -*- coding: utf-8 -*-
from bot import main_object, delivery_object
from . import keyboardbot as kb

dict_update = {
    # ЯЗЫК
    kb.d_language['ru']: main_object.language,
    kb.d_language['uz']: main_object.language,
    # ЯЗЫК

    # МЕНЮ
    kb.d_menu['ru']['products']: main_object.products,
    kb.d_menu['ru']['about']: main_object.about,
    kb.d_menu['ru']['news']: main_object.news,
    kb.d_menu['ru']['actions']: main_object.actions,
    kb.d_menu['ru']['main_menu']: main_object.start,
    kb.d_menu['ru']['change_language']: main_object.change_language,
    kb.d_menu['ru']['basket']: main_object.basket,
    kb.d_menu['ru']['partnership']: main_object.partnership,

    kb.d_menu['uz']['products']: main_object.products,
    kb.d_menu['uz']['about']: main_object.about,
    kb.d_menu['uz']['news']: main_object.news,
    kb.d_menu['uz']['actions']: main_object.actions,
    kb.d_menu['uz']['main_menu']: main_object.start,
    kb.d_menu['uz']['change_language']: main_object.change_language,
    kb.d_menu['uz']['basket']: main_object.basket,
    kb.d_menu['uz']['partnership']: main_object.partnership,
    # МЕНЮ

    # ПРОДУКТЫ
    kb.d_products['ru']['healthy']: main_object.healthy,
    kb.d_products['ru']['sport']: main_object.sport,

    kb.d_products['uz']['healthy']: main_object.healthy,
    kb.d_products['uz']['sport']: main_object.sport,
    # ПРОДУКТЫ


    # КОРЗИНА
    kb.d_basket['ru']['clear_basket']: delivery_object.clear_basket,
    kb.d_basket['ru']['order']: main_object.order,
    kb.d_basket['ru']['promocode']: delivery_object.promocode,
    kb.d_menu['ru']['cancel']: delivery_object.cancel,

    kb.d_basket['uz']['clear_basket']: delivery_object.clear_basket,
    kb.d_basket['uz']['order']: main_object.order,
    kb.d_basket['uz']['promocode']: delivery_object.promocode,
    kb.d_menu['uz']['cancel']: delivery_object.cancel,
    # КОРЗИНА


    # ПАРТНЕРКА
    kb.d_partnership['ru']['statistic']: main_object.statistic,
    kb.d_partnership['ru']['application']: main_object.application,
    kb.d_partnership['ru']['info']: main_object.info_partnership,

    kb.d_partnership['uz']['statistic']: main_object.statistic,
    kb.d_partnership['uz']['application']: main_object.application,
    kb.d_partnership['uz']['info']: main_object.info_partnership,
    # ПАРТНЕРКА


    # ЗАКАЗ
    kb.d_type_delivery['ru']['self']: delivery_object.type_delivery,
    kb.d_type_delivery['ru']['delivery']: delivery_object.type_delivery,
    kb.d_type_payment['ru']['cash']: main_object.type_payment_choose,
    kb.d_type_payment['ru']['payme']: main_object.type_payment_choose,

    kb.d_type_delivery['uz']['self']: delivery_object.type_delivery,
    kb.d_type_delivery['uz']['delivery']: delivery_object.type_delivery,
    kb.d_type_payment['uz']['payme']: main_object.type_payment_choose,
    kb.d_type_payment['uz']['cash']: main_object.type_payment_choose,
    # ЗАКАЗ

}