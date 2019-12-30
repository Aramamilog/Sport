# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from .models import *

admin.site.unregister(Group)
admin.site.site_header = "Админ панель"
admin.site.site_title = "Админ панель"
admin.site.index_title = "Добро пожаловать"

# Register your models here.

### ПОЛЬЗОВАИЕЛИ ###
class UsersAdmin(admin.ModelAdmin):
    """Модель пользователей"""
    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


    list_display = ['first_name', 'user_name', 'contact', 'language', 'user_id']
    search_fields = ['user_name', 'first_name', 'contact', 'language']
    list_filter = ['language']
    exclude = ['user_id']

    class Meta:
        model = Users

admin.site.register(Users, UsersAdmin)
### ПОЛЬЗОВАИЕЛИ ###


### БРЕНДЫ ###
class BrandsAdmin(admin.ModelAdmin):
    """Бренды"""
    list_display = ['title_ru', 'position']

    class Meta:
        model = Brands

admin.site.register(Brands, BrandsAdmin)
### БРЕНДЫ ###


### КАТЕГОРИИ ЗДОРОВОЕ ПИТАНИЕ ###
class CategoryHealthyAdmin(admin.ModelAdmin):
    """Модель категорий здорового питания"""
    list_display = ['title_ru', 'position']

    class Meta:
        model = CategoryHealthy

admin.site.register(CategoryHealthy, CategoryHealthyAdmin)
### КАТЕГОРИИ ЗДОРОВОЕ ПИТАНИЕ ###


### ПРОДУКТЫ ЗДОРОВОЕ ПИТАНИЕ ###
class ProductsHealthyAdmin(admin.ModelAdmin):
    """Модель продуктов здорового питания"""
    def image_tag_product(self, obj):
        try:
            return format_html('<img src="{}" width="60px"/>'.format(obj.photo_path.url))
        except Exception:
            return None
    image_tag_product.short_description = 'Фото'

    def status_list(self, obj):
        d_status = {0: "❌", 1: "✅"}
        return d_status[obj.status]
    status_list.short_description = 'Статус'

    def description_text_list(self, obj):
        description = """{}""".format(obj.description_ru)
        for rep in ['<b>', '</b>', '<code>', '</code>', '<i>', '</i>']:
            description = description.replace(rep, '')
        return description[:50] + '...'
    description_text_list.short_description = 'Описание'

    list_display = ['title_ru', 'description_text_list', 'price', 'category', 'brand', 'status_list', 'image_tag_product']
    search_fields = ['title_ru', 'description_ru', 'price', 'category__title_ru']
    list_filter = ['category', 'brand', 'status']

    class Meta:
        model = ProductsHealthy

admin.site.register(ProductsHealthy, ProductsHealthyAdmin)
### ПРОДУКТЫ ЗДОРОВОЕ ПИТАНИЕ ###


### КАТЕГОРИИ СПОРТИВНОГО ПИТАНИЕ ###
class CategorySportAdmin(admin.ModelAdmin):
    """Модель категорий спортивного питания"""
    list_display = ['title_ru', 'position']

    class Meta:
        model = CategorySport

admin.site.register(CategorySport, CategorySportAdmin)
### КАТЕГОРИИ СПОРТИВНОГО ПИТАНИЕ ###


### ПРОДУКТЫ СПОРТИВНОГО ПИТАНИЕ ###
class ProductsSportAdmin(admin.ModelAdmin):
    """Модель продуктов спортивного питания"""
    def image_tag_product(self, obj):
        try:
            return format_html('<img src="{}" width="60px"/>'.format(obj.photo_path.url))
        except Exception:
            return None
    image_tag_product.short_description = 'Фото'

    def status_list(self, obj):
        d_status = {0: "❌", 1: "✅"}
        return d_status[obj.status]
    status_list.short_description = 'Статус'

    def description_text_list(self, obj):
        description = """{}""".format(obj.description_ru)
        for rep in ['<b>', '</b>', '<code>', '</code>', '<i>', '</i>']:
            description = description.replace(rep, '')
        return description[:50] + '...'
    description_text_list.short_description = 'Описание'

    list_display = ['title_ru', 'description_text_list', 'price', 'category', 'brand', 'status_list', 'image_tag_product']
    search_fields = ['title_ru', 'description_ru', 'price', 'category__title_ru']
    list_filter = ['category', 'brand', 'status']

    class Meta:
        model = ProductsSport

admin.site.register(ProductsSport, ProductsSportAdmin)
### ПРОДУКТЫ СПОРТИВНОГО ПИТАНИЕ ###


### ЗАКАЗЫ ###
class OrdersAdmin(admin.ModelAdmin):
    """Модель заказов"""
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def order_text_list(self, obj):
        food_text = """{}""".format(obj.order_text)
        for rep in ['<b>', '</b>', '<code>', '</code>', '<i>', '</i>', '--------------------']:
            food_text = food_text.replace(rep, '')
        return food_text[:50] + '...'
    order_text_list.short_description = 'Заказ'

    def list_count(self, obj):
        return "Заказ - #{}".format(obj.count)
    list_count.short_description = '№ Номер'

    def list_status(self, obj):
        d_status = {0: "🛒", 1: "✅", 2: "⌛", 3: "❌"}
        return d_status[obj.status]
    list_status.short_description = 'Статус заказа'

    list_display = ['list_count', 'first_name', 'contact', 'order_text_list', 'full_price', 'type_payment', 'type_delivery', 'date', 'list_status']
    search_fields = ['order_text', 'full_price', 'first_name', 'contact']
    exclude = ['user_id', 'user_name', 'date', 'message_id_chat', 'type_payment', 'status', 'count']
    list_filter = ['status', 'type_payment', 'type_delivery']

    class Meta:
        model = Orders

admin.site.register(Orders, OrdersAdmin)
### ЗАКАЗЫ ###


### АКЦИИ ###
class ActionsAdmin(admin.ModelAdmin):
    """Модель акций"""
    def image_tag_light(self, obj):
        try:
            return format_html('<img src="{}" width="80px"/>'.format(obj.photo_path.url))
        except Exception:
            return None
    image_tag_light.short_description = 'Фото акции'

    def list_status(self, obj):
        d_status = {0: "❌", 1: "✅"}
        return d_status[obj.status]
    list_status.short_description = 'Статус'

    list_display = ['title_ru', 'category', 'list_status', 'image_tag_light']
    search_fields = ['title_ru', 'category']
    list_filter = ['category']

    class Meta:
        model = Actions

admin.site.register(Actions, ActionsAdmin)
### АКЦИИ ###


### НОВОСТИ ###
class NewsAdmin(admin.ModelAdmin):
    """Модель новостей"""
    def image_tag_light(self, obj):
        try:
            return format_html('<img src="{}" width="80px"/>'.format(obj.photo_path.url))
        except Exception:
            return None
    image_tag_light.short_description = 'Фото новости'

    def list_status(self, obj):
        d_status = {0: "❌", 1: "✅"}
        return d_status[obj.status]
    list_status.short_description = 'Статус'

    list_display = ['title_ru', 'category', 'list_status', 'image_tag_light']
    search_fields = ['title_ru', 'category']
    list_filter = ['category']

    class Meta:
        model = News

admin.site.register(News, NewsAdmin)
### НОВОСТИ ###


### ПАРТНЕРКА ###
class PartnershipAdmin(admin.ModelAdmin):
    """Партнерка"""
    def has_add_permission(self, request):
        return False

    def document_tag(self, obj):
        try:
            return format_html('<a href="{}">СКАЧАТЬ</a>'.format(obj.document.url))
        except Exception:
            return None
    document_tag.short_description = 'Документ'


    def comment_list(self, obj):
        return '{}...'.format(str(obj.comment)[:15])
    comment_list.short_description = 'Комментарий'

    list_display = ['full_name', 'contact', 'brand_name', 'document_tag', 'comment_list', 'brand']
    search_fields = ['full_name', 'contact', 'brand_name', 'document', 'comment']
    list_filter = ['brand']
    exclude = ['user_id']

    class Meta:
        model = Partnership

admin.site.register(Partnership, PartnershipAdmin)
### ПАРТНЕРКА ###


### ПРОМОКОДЫ ###
class PromocodesHealthAdmin(admin.ModelAdmin):
    """Промокоды"""
    def list_status(self, obj):
        d_status = {0: "❌", 1: "✅"}
        return d_status[obj.status]
    list_status.short_description = 'Статус'

    list_display = ['promocode', 'discount', 'list_status', 'type_active', 'date_active', 'count_active']
    search_fields = ['promocode', 'discount', 'date_active', 'count_active', 'products__title_ru']
    list_filter = ['type_active', 'status']

    class Meta:
        model = PromocodesHealth

admin.site.register(PromocodesHealth, PromocodesHealthAdmin)


class PromocodesSportAdmin(admin.ModelAdmin):
    """Промокоды"""
    def list_status(self, obj):
        d_status = {0: "❌", 1: "✅"}
        return d_status[obj.status]
    list_status.short_description = 'Статус'

    list_display = ['promocode', 'discount', 'list_status', 'type_active', 'date_active', 'count_active']
    search_fields = ['promocode', 'discount', 'date_active', 'count_active', 'products__title_ru']
    list_filter = ['type_active', 'status']

    class Meta:
        model = PromocodesSport

admin.site.register(PromocodesSport, PromocodesSportAdmin)


class PromocodesBrandsAdmin(admin.ModelAdmin):
    """Промокоды"""
    def list_status(self, obj):
        d_status = {0: "❌", 1: "✅"}
        return d_status[obj.status]
    list_status.short_description = 'Статус'

    list_display = ['promocode', 'discount', 'list_status', 'type_active', 'date_active', 'count_active']
    search_fields = ['promocode', 'discount', 'date_active', 'count_active', 'brands__title_ru']
    list_filter = ['type_active', 'status']

    class Meta:
        model = PromocodesBrands

admin.site.register(PromocodesBrands, PromocodesBrandsAdmin)


class PromocodesActivateAdmin(admin.ModelAdmin):
    """Активированные промокоды"""
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ['promocode', 'user_id', 'date_time']
    search_fields = ['promocode', 'user_id_id__first_name',  'date_time']

    class Meta:
        model = PromocodesActivate

admin.site.register(PromocodesActivate, PromocodesActivateAdmin)
### ПРОМОКОДЫ ###


### АДМИН БОТА ###
class BotAdminAdmin(admin.ModelAdmin):
    """Администраторы бота"""
    list_display = ['user_id']
    search_fields = ['user_id']

    class Meta:
        model = BotAdmin
admin.site.register(BotAdmin, BotAdminAdmin)
### АДМИН БОТА ###


# ## НОМЕР ЗАКАЗА ###
# class CountOrderAdmin(admin.ModelAdmin):
#     """Номер заказа"""
#     list_display = ['count']
#
#     class Meta:
#         model = CountOrder
#
# admin.site.register(CountOrder, CountOrderAdmin)
# ## НОМЕР ЗАКАЗА ###