import sqlite3

db_path = 'web_panel/db.sqlite3'

def dict_factory(cursor, row):
    """Преобразование результата sql lite в словарь"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# SELECT
def select_user_admin(data):
    """Выбор всех админов"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT user_id as user_id FROM admin_panel_botadmin WHERE user_id = ?", (data['user_id'],))
    result = cur.fetchone()
    cur.close()
    con.close()

    if result is None:
        return None
    return result

def select_users():
    """Выюор всех пользователей"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT user_id as user_id FROM admin_panel_users")
    result = cur.fetchall()
    cur.close()
    con.close()

    if result == []:
        return None

    return result


def select_user(data):
    """Выбор пользователя по user_id"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT id as id, user_id as user_id, user_name as user_name, first_name as first_name, language as language, contact as contact FROM admin_panel_users WHERE user_id = ?",
                (data['user_id'],))
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_all_actions():
    """Выбор всех акций"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_panel_actions WHERE status = 1")
    result = cur.fetchall()
    cur.close()
    con.close()

    return result


def select_action(data):
    """Выбор определенной акции"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT * FROM (SELECT id as id, title_{language} as title, photo_path as photo_path FROM admin_panel_actions WHERE status = 1) LIMIT {limit} OFFSET {offset}".format(language=data['language'], limit=data['limit'], offset=data['offset'])
    cur.execute(sql, )
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result[0]
    else:
        return None

def select_all_news():
    """Выюор всех новостей"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_panel_news WHERE status = 1")
    result = cur.fetchall()
    cur.close()
    con.close()

    return result


def select_one_news(data):
    """Выбор определенной новости"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT * FROM (SELECT id as id, title_{language} as title, photo_path as photo_path FROM admin_panel_news WHERE status = 1) LIMIT {limit} OFFSET {offset}".format(language=data['language'], limit=data['limit'], offset=data['offset'])
    cur.execute(sql, )
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result[0]
    else:
        return None

def select_categories_healthy(data):
    """Выбор всех категорий здорового питания"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT id as id, title_{language} as button_name FROM admin_panel_categoryhealthy ORDER BY position DESC".format(language=data['language'])
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None

def select_products_healthy(data):
    """Выбор продуктов здорового питания"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT h.id as id, h.title_{language} as button_name FROM admin_panel_productshealthy as h INNER JOIN admin_panel_brands as b ON h.brand_id = b.id WHERE h.category_id = ? AND h.status = 1 ORDER BY b.position DESC".format(language=data['language'])
    cur.execute(sql, (data['id'],))
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_healthy_product(data):
    """Выбор продукта здоровое питание"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT title_{language} as title, description_{language} as description, price as price, photo_path as photo_path, category_id as category_id FROM admin_panel_productshealthy WHERE id = ? AND status = 1".format(language=data['language'])
    cur.execute(sql,
                (data['product_id'],))
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_categories_sport(data):
    """Выбор всех категорий спортивного питания"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT id as id, title_{language} as button_name FROM admin_panel_categorysport ORDER BY position DESC".format(language=data['language'])
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_products_sport(data):
    """Выбор продуктов спортивного питания"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT s.id as id, s.title_{language} as button_name FROM admin_panel_productssport as s INNER JOIN admin_panel_brands as b ON s.brand_id = b.id WHERE s.category_id = ? AND s.status = 1 ORDER BY b.position DESC".format(language=data['language'])
    cur.execute(sql, (data['id'],))
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_sport_product(data):
    """Выбор продукта спортивного питание"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT title_{language} as title, description_{language} as description, price as price, photo_path as photo_path, category_id as category_id FROM admin_panel_productssport WHERE id = ? AND status = 1".format(language=data['language'])
    cur.execute(sql,
                (data['product_id'],))
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_healthy_category(data):
    """Выбор категории здорового питания"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT title_{language} as title FROM admin_panel_categoryhealthy WHERE id = ?".format(language=data['language'])
    cur.execute(sql, (data['id'],))
    result = cur.fetchone()
    cur.close()
    con.close()

    return result


def select_sport_category(data):
    """Выбор категории спортивного питания"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    sql = "SELECT title_{language} as title FROM admin_panel_categorysport WHERE id = ?".format(language=data['language'])
    cur.execute(sql, (data['id'],))
    result = cur.fetchone()
    cur.close()
    con.close()

    return result


def select_partnership(data):
    """Выбор партнера"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT brand_id as brand_id FROM admin_panel_partnership WHERE user_id_id = ?", (data['user_id_id'],))
    result = cur.fetchone()
    cur.close()
    con.close()

    return result


def select_update_count_order():
    """Выбор номера заказа"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT count as count FROM admin_panel_countorder")
    result = cur.fetchone()['count'] + 1

    cur.execute("UPDATE admin_panel_countorder SET count = ?", (result,))
    con.commit()

    cur.close()
    con.close()

    return result


def select_order_data(data):
    """Выбор данных заказа"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT count as count_order, user_id as user_id, order_text as order_text, full_price as full_price, first_name as first_name, contact as contact, type_payment as type_payment FROM admin_panel_orders WHERE message_id_chat = ?", (data,))
    result = cur.fetchone()
    cur.close()
    con.close()

    return result


def select_promocode_by_user(data):
    """Выбрать промокод по пользователю"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT promocode as promocode  FROM admin_panel_promocodesactivate WHERE user_id_id = ? AND promocode = ?",
                (data['user_id_id'], data['promocode']))
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        return True
    else:
        return False


def select_promocode_healhty(data):
    """Выбрать промокод"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_panel_promocodeshealth as promoh INNER JOIN admin_panel_promocodeshealth_products as healthp ON promoh.id = healthp.promocodeshealth_id INNER JOIN admin_panel_productshealthy as producth ON healthp.productshealthy_id = producth.id WHERE promoh.status = ? AND promoh.promocode = ?",
                (data['status'], data['promocode']))
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_promocodesport(data):
    """Выбрать промокод"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_panel_promocodessport as promos INNER JOIN admin_panel_promocodessport_products as sportp ON promos.id = sportp.promocodessport_id INNER JOIN admin_panel_productssport as products ON sportp.productssport_id = products.id WHERE promos.status = ? AND promos.promocode = ?",
                (data['status'], data['promocode']))
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_promocode_brand(data):
    """Выбрать промокод"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM admin_panel_promocodesbrands as promob INNER JOIN admin_panel_promocodesbrands_brands as brandd ON promob.id = brandd.promocodesbrands_id INNER JOIN admin_panel_brands as brands ON brandd.brands_id = brands.id WHERE promob.status = ? AND promob.promocode = ?",
                (data['status'], data['promocode']))
    result = cur.fetchall()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_discount_health(data):
    """Выбор скидки"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT promoh.discount as discount FROM admin_panel_promocodeshealth as promoh INNER JOIN admin_panel_promocodeshealth_products as healthp ON promoh.id = healthp.promocodeshealth_id INNER JOIN admin_panel_productshealthy as producth ON healthp.productshealthy_id = producth.id WHERE promoh.status = ? AND promoh.promocode = ? AND producth.id = ?",
                (data['status'], data['promocode'], data['id']))
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_discount_sport(data):
    """Выбор скидки"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT promos.discount as discount FROM admin_panel_promocodessport as promos INNER JOIN admin_panel_promocodessport_products as sportp ON promos.id = sportp.promocodessport_id INNER JOIN admin_panel_productssport as products ON sportp.productssport_id = products.id WHERE promos.status = ? AND promos.promocode = ? AND promos.id = ?",
                (data['status'], data['promocode'], data['id']))
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_discount_brand(data):
    """Выбор скидки"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT promob.discount as discount FROM admin_panel_promocodesbrands as promob INNER JOIN admin_panel_promocodesbrands_brands as brandb ON promob.id = brandb.promocodesbrands_id INNER JOIN admin_panel_brands as b ON brandb.brands_id = b.id WHERE promob.status = ? AND promob.promocode = ? AND promob.id = ?",
                (data['status'], data['promocode'], data['id']))
    result = cur.fetchone()
    cur.close()
    con.close()

    if result:
        return result
    else:
        return None


def select_promo(data):
    """Выбор существования промокода"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()

    for table in ['admin_panel_promocodeshealth', 'admin_panel_promocodessport', 'admin_panel_promocodesbrands']:
        sql = "SELECT * FROM {table} WHERE promocode = ?".format(table=table)
        cur.execute(sql, (data['promocode'],))
        result = cur.fetchone()

        if result:
            cur.close()
            con.close()
            return False

    cur.close()
    con.close()

    return True
# SELECT


# INSERT
def insert_user(data):
    """Добавление пользователя"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO admin_panel_users (user_id, user_name, first_name, language, contact) VALUES (?, ?, ?, ?, ?)",
                (data['user_id'], data['user_name'], data['first_name'], data['language'], data['contact']))
    con.commit()
    cur.close()
    con.close()


def insert_partnership(data):
    """Добавить партнерку"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO admin_panel_partnership (user_id_id, full_name, contact, brand_name, comment, document) VALUES (?, ?, ?, ?, ?, ?)",
                (data['user_id_id'], data['full_name'], data['contact'], data['brand_name'], data['comment'], data['document']))
    con.commit()
    cur.close()
    con.close()


def insert_new_order(data):
    """Добавление заказа"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("INSERT INTO admin_panel_orders (count, user_id, first_name, contact, order_text, full_price, date, status, message_id_chat, type_payment, type_delivery) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (data['count'], data['user_id'], data['first_name'], data['contact'], data['order_text'], data['full_price'],  data['date'], data['status'], data['message_id_chat'], data['type_payment'], data['type_delivery']))
    con.commit()

    cur.close()
    con.close()


def insert_promo_user(data):
    """Добавить активацию промокода к пользователю"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for promocode in data['list_of_promocodes']:
        cur.execute("INSERT INTO admin_panel_promocodesactivate (user_id_id, date_time, promocode) VALUES (?, ?, ?)",
                    (data['user_id_id'], data['date_time'], promocode))
        con.commit()

    cur.close()
    con.close()
# INSERT


# UPDATE
def update_language(data):
    """Обновить язык"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("UPDATE admin_panel_users SET language = ? WHERE user_id = ?",
                (data['language'], data['user_id']))

    con.commit()
    cur.close()
    con.close()


def update_order_status(data):
    """Обновить заказ"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("UPDATE admin_panel_orders SET status = ? WHERE message_id_chat = ?",
                (data['status'], data['message_id_chat']))
    con.commit()
    cur.close()
    con.close()


def update_decrement_promo(data):
    """Изменить количество активаций промокодов"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()

    for table in ['admin_panel_promocodeshealth', 'admin_panel_promocodessport', 'admin_panel_promocodesbrands']:
        for promocode in data['list_of_promocodes']:
            sql = "SELECT count_active as count_active, type_active as type_active FROM {table} WHERE promocode = ?".format(table=table)
            cur.execute(sql, (promocode,))
            result = cur.fetchone()
            if result:
                if result['type_active'] == 'count':
                    new_count_active = result['count_active'] - 1
                    if new_count_active == 0:
                        status = 0
                    else:
                        status = 1

                    sql_update = "UPDATE {table} SET status = ?, count_active = ? WHERE promocode = ?".format(table=table)
                    cur.execute(sql_update, (status, new_count_active, promocode))
                    con.commit()

    cur.close()
    con.close()
# UPDATE