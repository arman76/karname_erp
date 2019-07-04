# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import _thread
import a
import os
#import zipfile

os.system('wget https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz')
os.system('tar -zxvf geckodriver-v0.11.1-linux64.tar.gz')
os.system('wget https://github.com/rafpyprog/Mobilenium/archive/master.zip')
os.system('unzip Mobilenium-master.zip')

os.system('wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2')
os.system('tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2')
cwd = os.getcwd()
path = cwd + '/phantomjs-2.1.1-linux-x86_64/bin'
os.environ["PATH"] += os.pathsep + path
os.environ["PATH"] += os.pathsep + cwd


CHOOSING, TYPING_REPLY, TYPING_CHOICE, USERPASS, START_TIME, FINISH_TIME, COMMENTS, LESSON, PROFESSOR, CHOOSING_DARS, DATE = range(
    11)

reply_keyboard = [['username, password'],
                  ['start'],
                  ['stop']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(bot, update):
    update.message.reply_text(
        'سلام! کار من اینه که با استفاده از یوزرنیم و پسورد erp وارد سامانه بشم'
        ' و کارنامه ت رو مدام چک کنم هر وقت اتفاقی بیوفته خبرت کنم!'
        '\n'
        'یوزر و پسوردت وارد یه لیست میشه. به نوبت هر دفعه یه نفر از این لیست چک میشه پس به اندازه ی تعداد افراد تو لیست طول میکشه تا دوباره کارنامه ت چک بشه.',
        reply_markup=markup
    )
    print(update.message.chat_id)
    return CHOOSING


def user_pass(bot, update, user_data):
    user_data['choice'] = 'username'
    update.message.reply_text('خب {} خودتو بده:'.format('نام کاربری'))
    return USERPASS


def received_userpass(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    if category == 'username':
        update.message.reply_text('خب {} خودتو بده:'.format('کلمه عبور'))
        user_data['choice'] = 'password'
        return USERPASS
    del user_data['choice']
    if 'start_app' in user_data:
        with open('list.txt', 'r') as f:
            ls = f.readlines()
        with open('list.txt', 'w') as f:
            for l in ls:
                if l.split('=')[0] != str(update.message.chat_id):
                    f.write(l)
        with open('list.txt', 'a') as f:
            f.write(str(update.message.chat_id) + '=' + user_data['username'] + ':' + user_data['password']+'\n')

        update.message.reply_text('خب الان وارد لیست شدی! هر موقع اتفاقی افتاد کارنامه رو برات میفرستم!', reply_markup=markup)

        del user_data['start_app']
        return CHOOSING
    update.message.reply_text('خب اطلاعات گرفته شد! الان میتونی start رو بزنی!',
                              reply_markup=markup)
    return CHOOSING


def add_to_list(bot, update, user_data):
    if 'username' not in user_data:
        user_data['start_app'] = 1
        update.message.reply_text('اول باید نام کاربری و کلمه عبور رو بفرستی!')
        bot.send_message(chat_id=update.message.chat_id, text='خب {} خودتو بده:'.format('نام کاربری'))
        user_data['choice'] = 'username'
        return USERPASS
    
    with open('list.txt', 'r') as f:
        ls = f.readlines()
    with open('list.txt', 'w') as f:
        for l in ls:
            if l.split('=')[0] != str(update.message.chat_id):
                f.write(l)
    with open('list.txt', 'a') as f:
        f.write(str(update.message.chat_id) + '=' + user_data['username'] + ':' + user_data['password']+'\n')

    bot.send_message(chat_id=update.message.chat.id,
                     text='خب الان تو لیستی! هر موقع کارنامه ت تغییری کرد میفرستم برات!', reply_markup=markup)
    return CHOOSING


def restart(bot, update, user_data):
    user_data.clear()

    with open('list.txt', 'r') as f:
        ls = f.readlines()
    with open('list.txt', 'w') as f:
        for l in ls:
            if l.split('=')[0] != str(update.message.chat_id):
                f.write(l)
    os.system('rm '+str(update.message.chat_id))

    update.message.reply_text('اطلاعاتت پاک شد از لیست هم اومدی بیرون.', reply_markup=markup)


def unknown(bot, update):
    update.message.reply_text('ورودی یا دستور نامعتبر!', reply_markup=markup)
    return CHOOSING


def main():
    updater = Updater('427411167:AAEwT1ByVafesnS-kn1ITebZ8zy2SAoUGEk')
    _thread.start_new_thread(a.main, (updater.bot,))
    dp = updater.dispatcher
    restart_command_handler = CommandHandler('stop', restart, pass_user_data=True)
    dp.add_handler(restart_command_handler)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(Filters.text, start)],

        states={
            CHOOSING: [RegexHandler('^username\, password$',
                                    user_pass,
                                    pass_user_data=True),
                       RegexHandler('^start$',
                                    add_to_list,
                                    pass_user_data=True),
                       RegexHandler('^stop',
                                    restart,
                                    pass_user_data=True),
                       CommandHandler('start',
                                      start),
                       CommandHandler('restart',
                                      restart,
                                      pass_user_data=True),
                       MessageHandler(Filters.all,
                                      unknown)],

            USERPASS: [MessageHandler(Filters.text,
                                      received_userpass,
                                      pass_user_data=True)],
        },

        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
