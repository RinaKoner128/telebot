import pymssql
import psycopg2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from resources.conf_adm import adress, adress_adm
import resources.select as select
import random

month_list = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

"""
Метод Создания нового пользователя бота
"""
def set_users(id_users):
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram" ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("select distinct count(*) from telegram.users_t where id = (%s)" % id_users)
            try:
                for row in cursor:
                    if row[0] == 0:
                        cursor.execute("select * from telegram.users_t")
                        cursor.execute("INSERT INTO telegram.users_t(id, name)VALUES (%s, null)" % id_users)
            except psycopg2.ProgrammingError:
                print('Пользователь уже есть')
            conn.commit()


"""
Метод получения списка пользователей бота
"""
def get_users():
    users = []
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram") as conn:
        with conn.cursor() as cursor:
            cursor.execute("select distinct id from telegram.users_t")
            for row in cursor:
                users.append(row[0])
            return users


"""
Метод добавления к id пользователя имени
"""
def up_users(id_users, names):
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram" ) as conn:
        with conn.cursor() as cursor:
            try:
                sql_update_query = """Update telegram.users_t set name = %s where id = %s"""
                cursor.execute(sql_update_query, (names, id_users))
                conn.commit()
            except psycopg2.ProgrammingError:
                print('Пользователь уже есть')


"""
Метод получения количества СМЭВ запросов в очереди
"""
def get_smev_wait_send():
    with pymssql.connect(host = adress['host'], database = adress['database'], user = adress['user'], password = adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cursor.execute(select.smev_wait_send)
            for row in cursor:
                return row[0]


"""
Метод получения сводки МФЦ/ПГУ за вчера
"""
def get_yest():
    rep = {'pgu_yest': '0', 'mfc_yest': '0', 'all_yest': '0', 'net_yest': '0', 'elk_yest': '0'}
    with pymssql.connect(host = adress['host'], database = adress['database'], user = adress['user'], password = adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cursor.execute(select.report_epgu_yest)
            for row in cursor:
                rep['pgu_yest'] = row[0]
            cursor.execute(select.report_mfc_yest)
            for row in cursor:
                rep['mfc_yest'] = row[0]
            cursor.execute(select.report_all_yest)
            for row in cursor:
                rep['all_yest'] = row[0]
            cursor.execute(select.report_net_yest)
            for row in cursor:
                rep['net_yest'] = row[0]
            cursor.execute(select.report_elk)
            for row in cursor:
                rep['elk_yest'] = row[0]
            return rep


"""
Метод получения сводки МФЦ/ПГУ за сегодня
"""
def get_to():
    rep = {'pgu_to': '0', 'mfc_to': '0', 'all_to': '0', 'net_to': '0'}
    with pymssql.connect(host = adress['host'], database = adress['database'], user = adress['user'], password = adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cursor.execute(select.report_epgu_to)
            for row in cursor:
                rep['pgu_to'] = row[0]
            cursor.execute(select.report_mfc_to)
            for row in cursor:
                rep['mfc_to'] = row[0]
            cursor.execute(select.report_all_to)
            for row in cursor:
                rep['all_to'] = row[0]
            cursor.execute(select.report_net_to)
            for row in cursor:
                rep['net_to'] = row[0]
            return rep





"""
Метод получения сводки ГИС ФРИ и ЕГР ЗАГС
"""
def get_gis_zags():
    rep = {'gis_yest': '0', 'gis_to': '0', 'gis_week': '0', 'zags_yest': '0', 'zags_to': '0', 'zags_week': '0'}
    with pymssql.connect(host = adress['host'], database = adress['database'], user = adress['user'], password = adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cursor.execute(select.report_gis_yest)
            for row in cursor:
                rep['gis_yest'] = row[0]
            cursor.execute(select.report_zags_yest)
            for row in cursor:
                rep['zags_yest'] = row[0]
            cursor.execute(select.report_gis_to)
            for row in cursor:
                rep['gis_to'] = row[0]
            cursor.execute(select.report_zags_to)
            for row in cursor:
                rep['zags_to'] = row[0]
            cursor.execute(select.report_gis_week)
            for row in cursor:
                rep['gis_week'] = row[0]
            cursor.execute(select.report_zags_week)
            for row in cursor:
                rep['zags_week'] = row[0]
            return rep





"""
Метод получения Данных по ГИС Фри. Возможно будет в купе с МФЦ/ПГУ
"""
def get_gis():
    rep = {'1': '0', '7': '0'}
    with pymssql.connect(host = adress['host'], database = adress['database'], user = adress['user'], password = adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cursor.execute(select.gis_1)
            for row in cursor:
                rep['1'] = row[0]
            cursor.execute(select.gis_7)
            for row in cursor:
                rep['7'] = row[0]


"""
Метод получения количества СМЭВ запросов готовых к загрузке
"""
def get_smev_request_sending():
    with pymssql.connect(host=adress['host'], database=adress['database'], user=adress['user'],password=adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cursor.execute(select.smev_request_sending)
            for row in cursor:
                return row[0]


"""
Метод создания сводки.
СМЭВ запросы в очереди, сгруппированные по регламентам
"""
def get_smev_report():
    with pymssql.connect(host=adress['host'], database=adress['database'], user=adress['user'], password=adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cols = ["№", "Реестр", "кол-во"]
            a = np.empty(shape=[0, 3])
            cursor.execute(select.smev_report)
            for row in cursor:
                a = np.append(a, [[row[0],row[1],row[2]]], axis=0)
            df = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0]+1)))
            pd.set_option('max_colwidth', 37)
        return df




"""
Метод создания сводки.
СМЭВ запросы По 1013
"""

def get_smev_1013():
    with pymssql.connect(host=adress['host'], database=adress['database'], user=adress['user'], password=adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cols = ["Район", "кол-во"]
            a = np.empty(shape=[0, 2])
            cursor.execute(select.smev_1013)
            for row in cursor:
                a = np.append(a, [[row[0],row[1]]], axis=0)
            df = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0]+1)))
            pd.set_option('max_colwidth', 37)
        return df


"""
Метод создания сводки.
СМЭВ запросы в очереди(ждущие в отправку), сгруппированные по регламентам
"""
def get_smev_report_full():
    with pymssql.connect(host=adress['host'], database=adress['database'], user=adress['user'], password=adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cols = ["№", "Реестр", "кол-во"]
            a = np.empty(shape=[0, 3])
            cursor.execute(select.smev_report_full)
            for row in cursor:
                a = np.append(a, [[row[0],row[1],row[2]]], axis=0)
            df = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0]+1)))
            pd.set_option('max_colwidth', 37)
        return df


"""
Метод возвращающий количество запросов/заявок с ошибками.
"""
def get_err_count():
    rep = {'smev': '0', 'pgu': '0'}
    with pymssql.connect(host = adress['host'], database = adress['database'], user = adress['user'], password = adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cursor.execute(select.err_count_smev)
            for row in cursor:
                rep['smev'] = row[0]
            cursor.execute(select.err_count_pgu)
            for row in cursor:
                rep['pgu'] = row[0]
            return rep


"""
Метод возвращающий значения для команды "Прочее".
"""
def get_fil_count():
    rep = {'uszn': '0', 'nbo_pgu': '0', 'dist_pgu': '0'}
    with pymssql.connect(host = adress['host'], database = adress['database'], user = adress['user'], password = adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cursor.execute(select.uszn)
            for row in cursor:
                rep['uszn'] = row[0]
            cursor.execute(select.nob_pgu)
            for row in cursor:
                rep['nbo_pgu'] = row[0]
            cursor.execute(select.distr_pgu)
            for row in cursor:
                rep['dist_pgu'] = row[0]
            return rep


"""
Метод создания файла со сбоями.
ВСЕ Запросы СМЭВ_3 и Заявки ПГУ, которые получили статус "Сбой"
"""
def get_smev_err():
    with pymssql.connect(host=adress['host'], database=adress['database'], user=adress['user'], password=adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cols = ["Сообщение", "Дата обращения", "Тип запроса", "Услуга", "Ответ", "Тип запроса"]
            a = np.empty(shape=[0, 6])
            cursor.execute(select.smev_err)
            for row in cursor:
                a = np.append(a, [[row[0],row[1],row[2],row[3],row[4],row[5]]], axis=0)
            df_smev = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0]+1)))
            cols = ["Сообщение", "Дата обращения", "Тип запроса", "Услуга", "Описание обработки", "Тип запроса"]
            a = np.empty(shape=[0, 6])
            cursor.execute(select.smev_err_proc)
            for row in cursor:
                a = np.append(a, [[row[0],row[1],row[2],row[3],row[4],row[5]]], axis=0)
            df_proc = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0]+1)))
            cols = ["Номер заявки", "Сообщение", "Дата обращения", "Тип запроса", "Услуга", "Ответ", "Тип запроса"]
            a = np.empty(shape=[0, 7])
            cursor.execute(select.smev_err_req)
            for row in cursor:
                a = np.append(a, [[row[0], row[1], row[2], row[3], row[4], row[5], row[6]]], axis=0)
            conn.close()
            df_req = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0] + 1)))
        with pd.ExcelWriter('Сбои.xlsx', engine='xlsxwriter') as wb:
            df_req.to_excel(wb, sheet_name='Заявки', index=False)
            sheet = wb.sheets['Заявки']
            sheet.autofilter(0, 0, 0, 6)
            cell_format = wb.book.add_format()
            cell_format.set_font_name('Times New Romance')
            cell_format.set_font_size(10)
            cell_format.set_text_wrap()
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            sheet.set_column('A:D', 25, cell_format)
            sheet.set_column('E:E', 46, cell_format)
            sheet.set_column('F:F', 111, cell_format)
            sheet.set_column('G:G', 25, cell_format)
            df_smev.to_excel(wb, sheet_name='Запросы', index=False)
            sheet = wb.sheets['Запросы']
            sheet.autofilter(0, 0, 0, 5)
            cell_format = wb.book.add_format()
            cell_format.set_font_name('Times New Romance')
            cell_format.set_font_size(10)
            cell_format.set_text_wrap()
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            sheet.set_column('A:C', 25, cell_format)
            sheet.set_column('D:D', 46, cell_format)
            sheet.set_column('E:E', 111, cell_format)
            sheet.set_column('F:F', 25, cell_format)
            df_proc.to_excel(wb, sheet_name='Обработка', index=False)
            sheet = wb.sheets['Обработка']
            sheet.autofilter(0, 0, 0, 5)
            cell_format = wb.book.add_format()
            cell_format.set_font_name('Times New Romance')
            cell_format.set_font_size(10)
            cell_format.set_text_wrap()
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            sheet.set_column('A:C', 25, cell_format)
            sheet.set_column('D:D', 46, cell_format)
            sheet.set_column('E:E', 111, cell_format)
            sheet.set_column('F:F', 25, cell_format)


"""
Метод создания невылеченного файла со сбоями.
Запросы СМЭВ_3 и Заявки ПГУ, которые получили статус "Сбой" без исправления.
"""
def get_smev_err_heal():
    with pymssql.connect(host=adress['host'], database=adress['database'], user=adress['user'], password=adress['password'], charset='cp1251') as conn:
        with conn.cursor() as cursor:
            cols = ["Сообщение", "Дата обращения", "Тип запроса", "Услуга", "Ответ", "Тип запроса"]
            a = np.empty(shape=[0, 6])
            cursor.execute(select.smev_err_heal)
            for row in cursor:
                a = np.append(a, [[row[0],row[1],row[2],row[3],row[4],row[5]]], axis=0)
            df_smev = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0]+1)))

            cols = ["Номер заявки", "Сообщение", "Дата обращения", "Тип запроса", "Услуга", "Ответ", "Тип запроса"]
            a = np.empty(shape=[0, 7])
            cursor.execute(select.smev_err_req_heal)
            for row in cursor:
                a = np.append(a, [[row[0], row[1], row[2], row[3], row[4], row[5], row[6]]], axis=0)
            df_req = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0] + 1)))

            cols = ["Номер заявки", "Сообщение", "Дата обращения", "ИС отправителя"]
            a = np.empty(shape=[0, 4])
            cursor.execute(select.smev_err_asp)
            for row in cursor:
                a = np.append(a, [[row[0], row[1], row[2], row[3]]], axis=0)
            conn.close()
            df_net_asp = pd.DataFrame(a, columns=cols, index=range(1, (a.shape[0] + 1)))

        with pd.ExcelWriter('Сбои.xlsx', engine='xlsxwriter') as wb:
            df_req.to_excel(wb, sheet_name='Заявки', index=False)
            sheet = wb.sheets['Заявки']
            sheet.autofilter(0, 0, 0, 6)
            cell_format = wb.book.add_format()
            cell_format.set_font_name('Times New Romance')
            cell_format.set_font_size(10)
            cell_format.set_text_wrap()
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            sheet.set_column('A:D', 25, cell_format)
            sheet.set_column('E:E', 46, cell_format)
            sheet.set_column('F:F', 111, cell_format)
            sheet.set_column('G:G', 25, cell_format)

            df_smev.to_excel(wb, sheet_name='Запросы', index=False)
            sheet = wb.sheets['Запросы']
            sheet.autofilter(0, 0, 0, 5)
            cell_format = wb.book.add_format()
            cell_format.set_font_name('Times New Romance')
            cell_format.set_font_size(10)
            cell_format.set_text_wrap()
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            sheet.set_column('A:C', 25, cell_format)
            sheet.set_column('D:D', 46, cell_format)
            sheet.set_column('E:E', 111, cell_format)
            sheet.set_column('F:F', 25, cell_format)

            df_net_asp.to_excel(wb, sheet_name='Не ушедшие с ТИ', index=False)
            sheet = wb.sheets['Не ушедшие с ТИ']
            sheet.autofilter(0, 0, 0, 3)
            cell_format = wb.book.add_format()
            cell_format.set_font_name('Times New Romance')
            cell_format.set_font_size(10)
            cell_format.set_text_wrap()
            cell_format.set_align('center')
            cell_format.set_align('vcenter')
            sheet.set_column('A:D', 25, cell_format)

"""
Блок выстраивания графика.
"""

"""
Метод отправки данных из портала  таблицу
"""
def set_graf(times, velue):
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram" ) as conn:
        with conn.cursor() as cursor:
            cursor = conn.cursor()
            insert_query = """ INSERT INTO telegram.graf(date_dow, value) VALUES (%s, %s)"""
            item_tuple = (times, velue)
            cursor.execute(insert_query, item_tuple)
            conn.commit()


"""
Метод получения данных из таблицы
"""
def get_graf():
    x=[]
    y=[]
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram" ) as conn:
        with conn.cursor() as cursor:
            cursor = conn.cursor()
            cursor.execute("""SELECT date_dow, value FROM telegram.graf WHERE "date_dow" >= now () - INTERVAL '8 hour' order by date_dow""")
            for row in cursor:
                x.append(row[0].strftime("%H:%M"))
                y.append(row[1])
            return [x, y]


"""
Метод отрисовки графика.
"""
def draw_graf():
    x = get_graf()[0]
    y = get_graf()[1]
    new_x = []
    spam = []
    fig, ax = plt.subplots(figsize=(24, 8), dpi=240)
    plt.tight_layout(pad=5.0)
    ax.fill_between(x, y, y2=0, label='uempmed', alpha=0.5, color='tab:blue', linewidth=2)
    ax.set_title('График СМЭВ в отправке')
    ax.set_xlabel('Время запроса очереди', labelpad=15, fontsize=14)
    ax.set_ylabel('Запросы в отправке', labelpad=15, fontsize=14)
    for i in x:
        spam1 = re.search(':00$', i)
        spam2 = re.search(':30$', i)
        if spam1 != None or spam2 != None:
            new_x.append(i)
            spam.append(x.index(i))
    for i in spam:
        ax.text(x[i], y[i] + 0.5, f'{y[i]}', color='tab:blue', fontsize=12)
    ax.text(x[y.index(max(y))], max(y) + 0.5, f'{max(y)}', color='tab:blue', fontsize=12)
    plt.xticks(new_x)
    ax.grid(which='major', color='#EEEEEE', linewidth=1.8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.savefig('graf.png')

"""
Блок отвечающий на "Оживление" бота
Реализация приблеженного к реальному ответа бота.
"""

"""
Метод предоставления ответа, который "знает" бот.
Извлечение ответа на вопрос пользователя из базы данных
"""
def answer(question):
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'],
                          password=adress_adm['password'], options="-c search_path=telegram") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""select answer from telegram.question_answer where question = (%s);""",  [question])
            for row in cursor:
                return row[0]

"""
Метод записи новых вопросов.
"""
def set_question(question):
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram" ) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(""" INSERT INTO telegram.info(question) VALUES (%s);""", [question])
            except psycopg2.ProgrammingError as e:
                print(f'Вопрос не записан {e}')
            conn.commit()

"""
Метод выдает пользователю шутку, в случае, если в базе нет ответа на вопрос.
"""
def other():
    spam_list = []
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram") as conn:
        with conn.cursor() as cursor:
            cursor.execute("select distinct id from telegram.other")
            for row in cursor:
                spam_list.append(row[0])
    spam = random.choice(spam_list)
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram") as conn:
        with conn.cursor() as cursor:
            cursor.execute("select body from telegram.other where id = (%s)" % spam)
            for row in cursor:
                return row[0]

def info():
    with psycopg2.connect(host=adress_adm['host'], database=adress_adm['database'], user=adress_adm['user'], password=adress_adm['password'], options="-c search_path=telegram") as conn:
        with conn.cursor() as cursor:
            cursor.execute("select info from telegram.inform")
            for row in cursor:
                return row[0]



