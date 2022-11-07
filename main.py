import os
import datetime
import pymssql
import telebot
from collections import deque
import time
from threading import Thread
from notifiers import get_notifier
from resources.conf_adm import tockenn
import resources.TI_base_smev as bs


# import subprocess

"""
Настроить фоновый режим
Отладить библиотеки к запуску из терминала
"""
bot = telebot.TeleBot(tockenn)
telg = get_notifier('telegram')

history = deque([bs.get_smev_request_sending()], maxlen=2880)
times = deque([f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}'],
              maxlen=2880)
layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                           'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                           "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                           'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
li = [1850516818]

def dat_hist(n):
    maxm = 35000
    check = 0
    while True:
        check += 1
        if check == 12:
            bs.set_graf(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), bs.get_smev_request_sending())

            # Оповещение о малом количестве МФЦ заявок
            if datetime.datetime.now().strftime("%H:%M") == "09:30" and datetime.datetime.now().weekday() != 0:
                if bs.get_rep_pgu_mfc()["mfc_yest"] < 50 and bs.get_rep_pgu_mfc()["mfc_to"] < 150:
                    for i in bs.get_users():
                        telg.notify(token=tockenn, chat_id=i,
                                    message=f'Заявок с МФЦ за вчерашний день мало, очень:\n{str(bs.get_rep_pgu_mfc()["mfc_yest"])}\n'
                                            f'За сегодня заявок: {str(bs.get_rep_pgu_mfc()["mfc_to"])}')

            if datetime.datetime.now().strftime("%H:%M") == "16:45" and datetime.datetime.now().weekday() != 0:
                if bs.get_rep_pgu_mfc()["mfc_yest"] < 50 and bs.get_rep_pgu_mfc()["mfc_to"] < 150:
                    for i in bs.get_users():
                        telg.notify(token=tockenn, chat_id=i,
                                    message=f'За последние 2 дня заявок с МФЦ очень мало:\n'
                                            f'За вчерашний день: {str(bs.get_rep_pgu_mfc()["mfc_yest"])}\n'
                                            f'За сегодня заявок: {str(bs.get_rep_pgu_mfc()["mfc_to"])}')
            check = 0

#Оповещение о переполнености очереди
        history.append(bs.get_smev_request_sending())
        times.append(
            f'{datetime.datetime.now().hour}:{datetime.datetime.now().minute}')
        if history[len(history) - 2] > maxm > history[len(history) - 3] and (history[len(history) - 2] < history[len(history) - 1] or history[len(history) - 1] > maxm):
            if datetime.datetime.now().strftime("%H:%M") < "22:00":
                for i in bs.get_users():
                    # process = subprocess.Popen("script.bat") #Запуск скрипта типа bat
                    telg.notify(token=tockenn, chat_id=i, message=f'Превышение допустимой длины очереди. \nЗапросы в очереди: {str(bs.get_smev_request_sending())}')

        time.sleep(n)


def main_st():
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_smev_ti = ["СМЭВ", "Сводка", "Ошибки"]
        buttons_pgu_mfc = ["Заявки за вчера", "Заявки за сегодня", "Прочее"]
        buttons_graf = ["График 📉","ГИС ФРИ/ЕГР ЗАГС"]
        but_help = 'Инфо ❓'
        keyboard.add(*buttons_smev_ti)
        keyboard.add(*buttons_pgu_mfc)
        keyboard.add(*buttons_graf)
        keyboard.add(but_help)

        @bot.message_handler(commands=["start"])
        def big_start(m):
            bs.set_users(m.from_user.id)
            bot.send_message(m.chat.id,
                            'Добрый день. Я тестовый бот для анализа нагруженности ТИ. Выберите Вид сведений, которые хотите получить.', reply_markup=keyboard)

        # @bot.message_handler(commands=["new"])
        # def update(message):
        #     for user in li:
        #         bot.send_message(user, 'Обновление', reply_markup=keyboard)


        @bot.message_handler(content_types=['text'])
        def start(message):
            message.text = str(message.text).translate(layout)
            if message.text.lower() == 'смэв' or message.text.lower() == 'смев':
                if bs.get_smev_wait_send() == 0:
                    bot.send_message(message.from_user.id, 'Очередь пуста. Уточните на сервере.')
                else:
                    bot.send_message(message.from_user.id,
                                    f'СМЭВ на ТИ\nЗапросы, ожидающие отправки: {str(bs.get_smev_wait_send())}.\nВсего запросов в отправке: {str(bs.get_smev_request_sending())}')

            elif message.text.lower() == 'заявки пгу.мфц.фри' or message.text.lower() == 'пгу' or message.text.lower() == 'мфц' or message.text.lower() == 'гис' or message.text.lower() == 'фри' or message.text.lower() == 'заявки':
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                today = datetime.date.today()
                bot.send_message(message.from_user.id,
                                    f'За {(yesterday.strftime(f"%d {bs.month_list[yesterday.month - 1]} %Y"))}:\n'
                                    f'ПГУ: {str(bs.get_yest()["pgu_yest"])}\n'
                                    f'МФЦ: {str(bs.get_yest()["mfc_yest"])}\n'
                                    f'{"_"*30}\n'
                                    f'Всего на ТИ загружено: {str(bs.get_yest()["all_yest"])},\n'
                                    f'из них в АСП не загрузилось: {str(bs.get_yest()["net_yest"])}')
                bot.send_message(message.from_user.id,
                                    f'За {(today.strftime(f"%d {bs.month_list[today.month - 1]} %Y"))}:\n'
                                    f'ПГУ: {str(bs.get_to()["pgu_to"])}\n'
                                    f'МФЦ: {str(bs.get_to()["mfc_to"])}\n'
                                    f'{"_"*30}\n'
                                    f'Всего на ТИ загружено: {str(bs.get_to()["all_to"])},\n'
                                    f'из них в АСП не загрузилось: {str(bs.get_to()["net_to"])}')

            elif message.text.lower() == 'заявки за вчера' or message.text.lower() == 'заявки пгу.мфц.фри за вчера':
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                bot.send_message(message.from_user.id,
                                    f'За {(yesterday.strftime(f"%d {bs.month_list[yesterday.month - 1]} %Y"))}:\n'
                                    f'ПГУ: {str(bs.get_yest()["pgu_yest"])}\n'
                                    f'МФЦ: {str(bs.get_yest()["mfc_yest"])}\n'
                                    f'{"_"*30}\n'
                                    f'Всего на ТИ загружено: {str(bs.get_yest()["all_yest"])},\n'
                                    f'из них в АСП не загрузилось: {str(bs.get_yest()["net_yest"])}')

            elif message.text.lower() == 'заявки за сегодня' or message.text.lower() == 'заявки пгу.мфц.фри за сегодня':
                today = datetime.date.today()
                bot.send_message(message.from_user.id,
                                    f'За {(today.strftime(f"%d {bs.month_list[today.month - 1]} %Y"))}:\n'
                                    f'ПГУ: {str(bs.get_to()["pgu_to"])}\n'
                                    f'МФЦ: {str(bs.get_to()["mfc_to"])}\n'
                                    f'{"_"*30}\n'
                                    f'Всего на ТИ загружено: {str(bs.get_to()["all_to"])},\n'
                                    f'из них в АСП не загрузилось: {str(bs.get_to()["net_to"])}')



            elif message.text.lower() == 'гис фри.егр загс' or message.text.lower() == 'егр загс' or message.text.lower() == 'гис фри' or message.text.lower() == 'гис' or message.text.lower() == 'фри' or message.text.lower() == 'егр' or message.text.lower() == 'загс' :
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                today = datetime.date.today()
                bot.send_message(message.from_user.id,
                                    f'За {(yesterday.strftime(f"%d {bs.month_list[yesterday.month - 1]} %Y"))}:\n'
                                    f'ГИС ФРИ: {str(bs.get_gis_zags()["gis_yest"])}\n'
                                    f'ЕГР ЗАГС: {str(bs.get_gis_zags()["zags_yest"])}\n'
                                    f'{"_"*30}\n'
                                    f'За {(today.strftime(f"%d {bs.month_list[today.month - 1]} %Y"))}:\n'
                                    f'ГИС ФРИ: {str(bs.get_gis_zags()["gis_to"])}\n'
                                    f'ЕГР ЗАГС: {str(bs.get_gis_zags()["zags_to"])}\n'
                                    f'{"_"*30}\n'
                                    f'За последние 7 дней:\n'
                                    f'ГИС ФРИ: {str(bs.get_gis_zags()["gis_week"])}\n'
                                    f'ЕГР ЗАГС: {str(bs.get_gis_zags()["zags_week"])}\n'
                                 )





            elif message.text.lower() == 'сводка':
                bot.send_message(message.from_user.id, f'Запросы, ждущие отправки:\n\n{str(bs.get_smev_report_full())}')
                if str(bs.get_smev_report()).count('DataFrame'):
                    bot.send_message(message.from_user.id, 'Очередь пуста.')
                else:
                    bot.send_message(message.from_user.id, f'Из них запросы, находящиеся в отправке:\n\n{str(bs.get_smev_report())}')

            elif message.text.lower() == 'ошибки':
                # bot.send_message(message.from_user.id, f'Операция может занять несколько секунд. Пожалуйста, ожидайте результата.')
                try:
                    # bot.send_message(message.from_user.id, f'Вы може')
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    key_ful = telebot.types.InlineKeyboardButton(text='Все ошибки', callback_data='all')
                    key_slice = telebot.types.InlineKeyboardButton(text='Ошибки без "лечения"', callback_data='slice')
                    keyboard.add(key_ful)
                    keyboard.add(key_slice)
                    bot.send_message(message.from_user.id, text='Загрузить файл списка ошибок?', reply_markup=keyboard)
                except Exception as e:
                    bot.send_message(message.from_user.id, f'Ошибка сервра. Попробуйте через пару минут.({e})')

            elif message.text.lower() == 'прочее':
                bot.send_message(message.from_user.id,
                                f'За последние 3 дня Необработанных заявок:  {str(bs.get_fil_count()["nbo_pgu"])}.\n'
                                f'За последние 3 дня Нераспределенных по районам заявок:  {str(bs.get_fil_count()["dist_pgu"])}.\n'
                                f'За последние 7 дней "УСЗН" заявок:    {str(bs.get_fil_count()["uszn"])}.')

            elif message.text.lower() == 'график' or message.text == 'График 📉':
                bs.draw_graf()
                bot.send_photo(message.chat.id, photo=open('graf.png', 'rb'))
                os.remove('graf.png')

            elif message.text == 'Инфо ❓' or message.text.lower() == 'инфо' or message.text.lower() == 'и':
                bot.send_message(message.from_user.id, bs.info())

            elif message.text.lower() == 'привет' or message.text.lower() == 'здравствуй' or message.text.lower() == 'здравствуйте':
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJfil-7g5saK6caYV8CsqELuWLynDH2AALiBgACOtEHAAFgVDNflxcX6h4E')
                bot.send_message(message.from_user.id, "Здравствуйте. Как я могу к Вам обращаться?")
                bot.register_next_step_handler(message, get_name)

            else:
                if bs.answer(message.text.lower()) is not None:
                    bot.send_message(message.from_user.id, f'{str(bs.answer(message.text.lower()))}')
                else:
                    bot.send_message(message.from_user.id,
                                    f'Я еще совсем маленький и только учусь. \n'
                                    f'Я запомню Ваш вопрос и обязательно отвечу на него позже. А пока, предлагаю почитать что-нибудь, для поднятия настроения ☺\n\n'
                                    f'{str(bs.other())}')
                    bs.set_question(message.text)

        def get_name(message):
            global name
            name = message.text
            bs.up_users(message.from_user.id, name)
            bot.send_message(message.from_user.id, f'Приятно познакомится, {name}. Я Вас запомнил 😈')
    except Exception as e:
        print(f'Ошибка - {e}')

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        if call.data == "all":
            try:
                bot.send_message(call.message.chat.id, 'Файл формируется. Пожалуйста, подождите несколько секунд.')
                bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEGQwtjX45RB3O9j-troQS5R_i2S2kbVQAClgoAAmXXSEqeC5Vjb_xP4CoE')
                bs.get_smev_err()
                file = open('Сбои.xlsx', 'rb')
                bot.send_animation(call.message.chat.id, file)
                file.close()
                os.remove('Сбои.xlsx')
            except Exception as e:
                bot.send_message(call.message.chat.id, f'Ошибка сервера. Попробуйте через пару минут.({e})')
        if call.data == "slice":
            try:
                bot.send_message(call.message.chat.id, 'Файл формируется. Пожалуйста, подождите несколько секунд.')
                bot.send_sticker(call.message.chat.id, 'CAACAgIAAxkBAAEGQw1jX45XoJeLQIcxLoIDyW2FTPgZ_wACIwADKA9qFCdRJeeMIKQGKgQ')
                bs.get_smev_err_heal()
                file = open('Сбои.xlsx', 'rb')
                bot.send_document(call.message.chat.id, file)
                file.close()
                os.remove('Сбои.xlsx')
            except pymssql._pymssql.OperationalError as e:
                bot.send_message(call.message.chat.id,
                                 'Запрос пал жертвой репрессий в угоду БД. Помянем...')
                bot.send_sticker(call.message.chat.id,
                                 'CAACAgIAAxkBAAEF8Z9jM-XK_HHjbju6ND0Dw8fX_1HoRgACcxMAAtjY4QAB-R-zLyXpPuEqBA')
                print(e)
            except Exception as e:
                bot.send_message(call.message.chat.id, f'Ошибка сервера. Попробуйте через пару минут.({e})')



    if __name__ == '__main__':
        while True:
            try:
                bot.polling(none_stop=True, interval=0)
            except Exception as e:
                time.sleep(3)
                print(f'{datetime.datetime.now()} Возникла ошибка {e}')



t1 = Thread(target=dat_hist, args=(5,))
t2 = Thread(target=main_st)

t1.start()
t2.start()
t1.join()
t2.join()
