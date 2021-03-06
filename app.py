# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import _thread
import a
import os


os.system('wget https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz')
os.system('tar -zxvf geckodriver-v0.11.1-linux64.tar.gz')
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


def start(update, context):
    update.message.reply_text(
        'سلام! چون میدونم گشادی من جات کارنامه رو چک میکنم'
        ''
        '\n'
        'یوزر و پسوردت وارد یه لیست میشه. به نوبت هر دفعه یه نفر از این لیست چک میشه پس به اندازه ی تعداد افراد تو لیست طول میکشه تا دوباره کارنامه ت چک بشه.',
        reply_markup=markup
    )
    print(update.message.chat_id)
    return CHOOSING


def user_pass(update, context):
    user_data = context.user_data
    user_data['choice'] = 'username'
    update.message.reply_text('خب {} خودتو بده:'.format('نام کاربری'))
    return USERPASS


def received_userpass(update, context):
    user_data = context.user_data
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


def add_to_list(update, context):
    user_data = context.user_data
    bot = context.bot
    
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


def restart(update, context):
    user_data = context.user_data
    user_data.clear()

    with open('list.txt', 'r') as f:
        ls = f.readlines()
    with open('list.txt', 'w') as f:
        for l in ls:
            if l.split('=')[0] != str(update.message.chat_id):
                f.write(l)
    os.system('rm '+str(update.message.chat_id))

    update.message.reply_text('اطلاعاتت پاک شد از لیست هم اومدی بیرون.', reply_markup=markup)


def unknown(update, context):
    update.message.reply_text('ورودی یا دستور نامعتبر!', reply_markup=markup)
    return CHOOSING


def main():
    updater = Updater('995772295:AAFjjCH_i2ap2Mh0ibWQyjZQNxYAKZM-M8k', use_context=True)
    # updater = Updater('')
    _thread.start_new_thread(a.main, (updater.bot,))
    dp = updater.dispatcher
    restart_command_handler = CommandHandler('stop', restart, pass_user_data=True)
    dp.add_handler(restart_command_handler)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(Filters.text, start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^username\, password$'),
                                    user_pass),
                       MessageHandler(Filters.regex('^start$'),
                                    add_to_list),
                       MessageHandler(Filters.regex('^stop'),
                                    restart),
                       CommandHandler('start',
                                      start),
                       CommandHandler('restart',
                                      restart,
                                      pass_user_data=True),
                       MessageHandler(Filters.all,
                                      unknown)],

            USERPASS: [MessageHandler(Filters.text,
                                      received_userpass)],
        },

        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
