from django.db import models
from .generate_name import generate_name
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator


def photo_validator(value):
    limit_mb = 2
    if value.file.size > limit_mb * 1024 * 1024:
        raise ValidationError("Фото не должно быть больше 2мб")

    if str(value.file).split('.')[1] not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('''Фото должно быть в формате jpg, jpeg, png''')

def promo_validator(value):
    if len(value) != 12:
        raise ValidationError("Длина прокомода 12 символов (латинские буквы и цифры)")

    if value != value.upper():
        raise ValidationError("Промокод должен быть введен только заглавными буквами и цифрами")


### ПОЛЬЗОВАТЕЛИ ###
class Users(models.Model):
    """Модель пользователей"""
    user_id = models.IntegerField(verbose_name='ID пользователя')
    user_name = models.CharField(max_length=100, verbose_name='User_name')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    contact = models.CharField(max_length=100, verbose_name='Контакт')
    language = models.CharField(max_length=100, verbose_name='Язык', choices=(('ru', 'Русский'), ('uz', 'Узбекский')), blank=True, null=True)

    def __str__(self):
        return self.first_name[:50]

    class Meta:
        verbose_name = "клиента"
        verbose_name_plural = "  👤 КЛИЕНТЫ"
### ПОЛЬЗОВАТЕЛИ ###


### БРЕНДЫ ###
class Brands(models.Model):
    """Бренды"""
    title_ru = models.CharField(max_length=20, verbose_name='Бренд', help_text='Русский')
    title_uz = models.CharField(max_length=20, verbose_name='Бренд', help_text='Узбекский')
    position = models.IntegerField(verbose_name='Позиция для пользователей', default=0, help_text='Чем выше число, тем выше бренд будет показан пользователю')

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = "бренд"
        verbose_name_plural = "    ⭐ БРЕНДЫ"
### БРЕНДЫ ###


### КАТЕГОРИИ ЗДОРОВОЕ ПИТАНИЕ ###
class CategoryHealthy(models.Model):
    """Модель категорий здорового питания"""
    title_ru = models.CharField(max_length=20, verbose_name='Категория', help_text='Русский')
    title_uz = models.CharField(max_length=20, verbose_name='Категория', help_text='Узбекский')
    position = models.IntegerField(verbose_name='Позиция для пользователей', default=0, help_text='Чем выше число, тем выше категория будет показан пользователю')

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = "категорию здорового питания"
        verbose_name_plural = "   🥦 ЗДОРОВОЕ ПИТАНИЕ - КАТЕГОРИИ"
### КАТЕГОРИИ ЗДОРОВОЕ ПИТАНИЕ ###


### ПРОДУКТЫ ЗДОРОВОЕ ПИТАНИЕ ###
def image_folder_healthy(instance, filename):
    """Путь сохранения картинок для продуктов здорового питания"""
    prefix = generate_name(8) + '.' + filename.split('.')[1]
    return "healthy/{prefix}".format(prefix=prefix)

class ProductsHealthy(models.Model):
    """Модель продуктов здорового питания"""
    title_ru = models.CharField(max_length=100, verbose_name='Продукт', help_text='Русский')
    title_uz = models.CharField(max_length=100, verbose_name='Продукт', help_text='Узбекский')
    description_ru = models.TextField(max_length=1000, verbose_name='Описание', help_text='Русский', null=True, blank=True)
    description_uz = models.TextField(max_length=1000, verbose_name='Описание', help_text='Узбекский', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена')
    photo_path = models.ImageField(upload_to=image_folder_healthy, verbose_name='Фото', validators = [photo_validator])
    category = models.ForeignKey(CategoryHealthy, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    brand = models.ForeignKey(Brands, on_delete=models.SET_NULL, verbose_name='Бренд', null=True)
    status = models.IntegerField(verbose_name='Статус', choices=((0, 'Отключенно'), (1, 'Включенно')), default=1)

    def __str__(self):
        return '{} - {}'.format(self.title_ru, self.brand)

    class Meta:
        verbose_name = "продукт здорового питания"
        verbose_name_plural = "   🥦 ЗДОРОВОЕ ПИТАНИЕ - ПРОДУКТЫ"
### ПРОДУКТЫ ЗДОРОВОЕ ПИТАНИЕ ###


### КАТЕГОРИИ СПОРТИВНОГО ПИТАНИЕ ###
class CategorySport(models.Model):
    """Модель категорий спортивного питания"""
    title_ru = models.CharField(max_length=20, verbose_name='Категория', help_text='Русский')
    title_uz = models.CharField(max_length=20, verbose_name='Категория', help_text='Узбекский')
    position = models.IntegerField(verbose_name='Позиция для пользователей', default=0, help_text='Чем выше число, тем выше категория будет показан пользователю')

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = "категорию спортивного питания"
        verbose_name_plural = "  🏋️‍♂ СПОРТИВНОЕ ПИТАНИЕ - КАТЕГОРИИ"
### КАТЕГОРИИ СПОРТИВНОГО ПИТАНИЕ ###


### ПРОДУКТЫ СПОРТИВНОГО ПИТАНИЕ ###
def image_folder_sport(instance, filename):
    """Путь сохранения картинок для продуктов спортивного питания"""
    prefix = generate_name(8) + '.' + filename.split('.')[1]
    return "sport/{prefix}".format(prefix=prefix)

class ProductsSport(models.Model):
    """Модель продуктов спортивного питания"""
    title_ru = models.CharField(max_length=100, verbose_name='Продукт', help_text='Русский')
    title_uz = models.CharField(max_length=100, verbose_name='Продукт', help_text='Узбекский')
    description_ru = models.TextField(max_length=1000, verbose_name='Описание', help_text='Русский', null=True, blank=True)
    description_uz = models.TextField(max_length=1000, verbose_name='Описание', help_text='Узбекский', null=True, blank=True)
    price = models.IntegerField(verbose_name='Цена')
    photo_path = models.ImageField(upload_to=image_folder_sport, verbose_name='Фото', validators = [photo_validator])
    category = models.ForeignKey(CategorySport, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    brand = models.ForeignKey(Brands, on_delete=models.SET_NULL, verbose_name='Бренд', null=True)
    status = models.IntegerField(verbose_name='Статус', choices=((0, 'Отключенно'), (1, 'Включенно')), default=1)

    def __str__(self):
        return '{} - {}'.format(self.title_ru, self.brand)

    class Meta:
        verbose_name = "продукт спортивного питания"
        verbose_name_plural = "  🏋️‍♂ СПОРТИВНОЕ ПИТАНИЕ - ПРОДУКТЫ"
### ПРОДУКТЫ СПОРТИВНОГО ПИТАНИЕ ###


### НОМЕР ЗАКАЗА ###
class CountOrder(models.Model):
    """Номер заказа"""
    count = models.IntegerField(verbose_name='Номер заказа')
### НОМЕР ЗАКАЗА ###


### ЗАКАЗЫ ###
class Orders(models.Model):
    """Заказы"""
    count = models.IntegerField(verbose_name='№ Номер')
    user_id = models.IntegerField(verbose_name='ID пользователя')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    contact = models.CharField(max_length=100, verbose_name='Контакт')
    order_text = models.TextField(verbose_name='Заказ')
    full_price = models.IntegerField(verbose_name='Цена')
    date = models.CharField(max_length=100, verbose_name='Дата / Время')
    type_payment = models.CharField(max_length=100, verbose_name='Тип оплаты', choices=(('cash', 'Наличные'), ('payme', 'PayMe')))
    type_delivery = models.CharField(max_length=100, verbose_name='Тип доставки', choices=(('self', 'Самовывоз'), ('delivery', 'Доставка')))
    status = models.IntegerField(verbose_name='Статус заказа', choices=((0, "🛒 Новый"), (1, "✅ Принят"), (2, "⌛ Ожидание"), (3, "❌ Отклонен")))
    message_id_chat = models.IntegerField(verbose_name='ID сообщения заказа в канале')

    def __str__(self):
        return self.order_text[:10]

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = " 🛒 ЗАКАЗЫ"
### ЗАКАЗЫ ####


### АКЦИИ ###
def image_folder_actions(instance, filename):
    prefix = generate_name(10) + '.' + filename.split('.')[1]
    return "actions/{prefix}".format(prefix=prefix)

class Actions(models.Model):
    """Акции"""
    title_ru = models.TextField(max_length=1000, verbose_name='Описание акции', help_text='Русский')
    title_uz = models.TextField(max_length=1000, verbose_name='Описание акции', help_text='Узбекский')
    category = models.CharField(max_length=100, verbose_name='Категория', blank=True, null=True, help_text='Необязательное поле.<br>Для удобной сортировки в админ панели')
    status = models.IntegerField(verbose_name='Статус', choices=((0, 'Отключена'), (1, 'Включена')), default=1)
    photo_path = models.ImageField(upload_to=image_folder_actions, verbose_name='Фото акции', validators=[photo_validator])

    def __str__(self):
        return self.title_ru[:30]

    class Meta:
        verbose_name = "акцию"
        verbose_name_plural = "🎁 АКЦИИ"
### АКЦИИ ###


### НОВОСТИ ###
def image_folder_news(instance, filename):
    prefix = generate_name(10) + '.' + filename.split('.')[1]
    return "news/{prefix}".format(prefix=prefix)

class News(models.Model):
    """Новости"""
    title_ru = models.TextField(max_length=1000, verbose_name='Описание новости', help_text='Русский')
    title_uz = models.TextField(max_length=1000, verbose_name='Описание новости', help_text='Узбекский')
    category = models.CharField(max_length=100, verbose_name='Категория', blank=True, null=True, help_text='Необязательное поле.<br>Для удобной сортировки в админ панели')
    status = models.IntegerField(verbose_name='Статус', choices=((0, 'Отключена'), (1, 'Включена')), default=1)
    photo_path = models.ImageField(upload_to=image_folder_news, verbose_name='Фото акции', validators=[photo_validator])

    def __str__(self):
        return self.title_ru[:30]

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "❓ НОВОСТИ"
### НОВОСТИ ###


### ПАРТНЕРКА ###
class Partnership(models.Model):
    """Партнерка"""
    user_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    brand_name = models.CharField(max_length=100, verbose_name='Название бренда')
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    contact = models.CharField(max_length=100, verbose_name='Контакт')
    document = models.FileField(verbose_name='Документ', null=True, blank=True)
    comment = models.TextField(max_length=4000, verbose_name='Комментарий', null=True, blank=True)
    brand = models.ForeignKey(Brands, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Статистика по бренду', help_text='Оставьте пустым для того, чтобы пользователь не мог видеть статистику')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "бренд"
        verbose_name_plural = "  🤝 ПАРТНЕРКА"
### ПАРТНЕРКА ###


### ПРОМОКОДЫ ###
class PromocodesHealth(models.Model):
    """Промокоды"""
    products = models.ManyToManyField(ProductsHealthy, verbose_name='Продукты')
    type_active = models.CharField(max_length=100, verbose_name='Активен по', choices=(('date', 'ДАТЕ/ВРЕМЕНИ'), ('count', 'КОЛИЧЕСТВУ АКТИВАЦИЙ')))

    date_active = models.DateTimeField(verbose_name='Дата/Время активности', null=True, blank=True, help_text='Установите, если выбрали<br></b>Активен по ДАТЕ/ВРЕМЕНИ</b>')
    count_active = models.IntegerField(verbose_name='Количество активаций', null=True, blank=True, validators=[MinValueValidator(1)],
                                       help_text='Установите, если выбрали<br></b>Активен по КОЛИЧЕСТВУ АКТИВАЦИЙ</b>')

    promocode = models.CharField(max_length=12, verbose_name='Промокод', validators=[promo_validator])
    discount = models.IntegerField(verbose_name='Скидка (%)', validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.IntegerField(verbose_name='Статус', choices=((0, 'Не активный'), (1, 'Актинвый')), default=1)

    def __str__(self):
        return self.promocode

    class Meta:
        verbose_name = "промокод"
        verbose_name_plural = "🔲 ПРОМОКОДЫ - ЗДОРОВОЕ ПИТАНИЕ"


class PromocodesSport(models.Model):
    """Промокоды"""
    products = models.ManyToManyField(ProductsSport, verbose_name='Продукты')
    type_active = models.CharField(max_length=100, verbose_name='Активен по', choices=(('date', 'ДАТЕ/ВРЕМЕНИ'), ('count', 'КОЛИЧЕСТВУ АКТИВАЦИЙ')))

    date_active = models.DateTimeField(verbose_name='Дата/Время активности', null=True, blank=True, help_text='Установите, если выбрали<br></b>Активен по ДАТЕ/ВРЕМЕНИ</b>')
    count_active = models.IntegerField(verbose_name='Количество активаций', null=True, blank=True, validators=[MinValueValidator(1)],
                                       help_text='Установите, если выбрали<br></b>Активен по КОЛИЧЕСТВУ АКТИВАЦИЙ</b>')

    promocode = models.CharField(max_length=12, verbose_name='Промокод', validators=[promo_validator])
    discount = models.IntegerField(verbose_name='Скидка (%)', validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.IntegerField(verbose_name='Статус', choices=((0, 'Не активный'), (1, 'Актинвый')), default=1)

    def __str__(self):
        return self.promocode

    class Meta:
        verbose_name = "промокод"
        verbose_name_plural = "🔲 ПРОМОКОДЫ - СПОРТИВНОЕ ПИТАНИЕ"


class PromocodesBrands(models.Model):
    """Промокоды"""
    brands = models.ManyToManyField(Brands, verbose_name='Бренды')
    type_active = models.CharField(max_length=100, verbose_name='Активен по', choices=(('date', 'ДАТЕ/ВРЕМЕНИ'), ('count', 'КОЛИЧЕСТВУ АКТИВАЦИЙ')))

    date_active = models.DateTimeField(verbose_name='Дата/Время активности', null=True, blank=True, help_text='Установите, если выбрали<br></b>Активен по ДАТЕ/ВРЕМЕНИ</b>')
    count_active = models.IntegerField(verbose_name='Количество активаций', null=True, blank=True, validators=[MinValueValidator(1)],
                                       help_text='Установите, если выбрали<br></b>Активен по КОЛИЧЕСТВУ АКТИВАЦИЙ</b>')

    promocode = models.CharField(max_length=12, verbose_name='Промокод', validators=[promo_validator])
    discount = models.IntegerField(verbose_name='Скидка (%)', validators=[MinValueValidator(0), MaxValueValidator(100)])
    status = models.IntegerField(verbose_name='Статус', choices=((0, 'Не активный'), (1, 'Актинвый')), default=1)

    def __str__(self):
        return self.promocode

    class Meta:
        verbose_name = "промокод"
        verbose_name_plural = "🔲 ПРОМОКОДЫ - БРЕНДЫ"


class PromocodesActivate(models.Model):
    """Активированные промокоды"""
    user_id = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    promocode = models.CharField(max_length=12, verbose_name='Промокод')
    date_time = models.CharField(max_length=100, verbose_name='Дата/Время')

    def __str__(self):
        return self.promocode

    class Meta:
        verbose_name = "промокод"
        verbose_name_plural = "🔲 АКТИВИРОВАНЫЕ ПРОМОКОДЫ"
### ПРОМОКОДЫ ###


### АДМИН БОТА ###
class BotAdmin(models.Model):
    """Администраторы бота"""
    user_id = models.CharField(verbose_name='user_id - админа', max_length=100)

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = "админа"
        verbose_name_plural = "🔒 АДМИН БОТА"
### АДМИН БОТА ###