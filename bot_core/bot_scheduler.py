import schedule, sqlite3, time
import datetime as d

db_path = 'web_panel/db.sqlite3'

def dict_factory(cursor, row):
    """Преобразование результата sql lite в словарь"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def promo_status():
    """Отключение промокодов"""
    con = sqlite3.connect(db_path)
    con.row_factory = dict_factory
    cur = con.cursor()

    for table in ['admin_panel_promocodeshealth', 'admin_panel_promocodessport', 'admin_panel_promocodesbrands']:
        sql = "SELECT id as id, date_active as date_active FROM  {table} WHERE status = ? AND type_active = ?".format(table=table)
        cur.execute(sql, (1, 'date'))
        result = cur.fetchall()

        if result:
            for promocode in result:
                now_time = d.datetime.now()

                promo_date = promocode['date_active'].split(' ')[0].split('-')
                promo_time = promocode['date_active'].split(' ')[1].split(':')

                promo_datetime = d.datetime(year=int(promo_date[0]), month=int(promo_date[1]), day=int(promo_date[2]),
                                            hour=int(promo_time[0]), minute=int(promo_time[1]))

                if now_time >= promo_datetime:
                    sql_update = "UPDATE admin_panel_promocodeshealth SET status = ? WHERE id = ?"
                    cur.execute(sql_update, (0, promocode['id']))
                    con.commit()

    cur.close()
    con.close()


def schedule_start():
    schedule.every(600).seconds.do()


    while True:
        schedule.run_pending()
        time.sleep(1)