# -*- coding: utf-8 -*-
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup

reply_keyboard = [['username, password'],
                  ['start'],
                  ['stop']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def main(bot, chat_id, user_data):
    driver = webdriver.PhantomJS()
    try:
        driver.get("http://erp.guilan.ac.ir/Dashboard.aspx")
        if 'erp.guilan.ac.ir/GoToDashboard.aspx' in driver.current_url:
            driver.find_element_by_class_name('refreshDash').click()

        wait = WebDriverWait(driver, 10)
        elem = wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'ورود به س')))
        elem.click()
        elem = wait.until(ec.presence_of_element_located((By.ID, 'iframe_040101')))

        driver.get(elem.get_property('src'))
        elem = driver.find_element_by_name('SSMUsername_txt')
        elem.send_keys(user_data['username'])

        elem = driver.find_element_by_name('SSMPassword_txt')
        elem.send_keys(user_data['password'] + Keys.ENTER)
        elem = wait.until(ec.presence_of_element_located((By.ID, 'userInfoTitle')))
        elem.click()
        elem = wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'امور آموزش')))
        elem.click()

        elem = wait.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'کارنامه ترم')))
        elem.click()
        elem = wait.until(ec.presence_of_element_located((By.ID, 'iframe_020205')))
        driver.get(elem.get_property('src'))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        ts = soup.find_all('table', class_='grd')
        del soup
        t = ts[-1]

        del ts
        text: str = t.get_text()
        del t
        text = text.replace('\n\n\n', '|')
        text = text.replace('\n\n\n', '|')
        text = text.replace('\n\n\n', '|')
        text = text.replace('\n\n', '\n')
        t2 = ''
        for t in text.split('\n'):
            try:
                int(t.split('|')[0])
                t2 += '|'.join(t.split('|')[1:-4]) + '\n'
            except ValueError:
                pass

        try:
            with open(str(chat_id), 'r') as f:
                if f.read() != t2:
                    bot.send_message(chat_id=chat_id, text=t2, reply_markup=markup)
        except FileNotFoundError:
            bot.send_message(chat_id=chat_id, text='اولین بار:\n'+t2, reply_markup=markup)
        with open(str(chat_id), 'w') as f:
            f.write(t2)
        del t2
        del text

    except selenium.common.exceptions.TimeoutException:
        print('selenium.common.exceptions.TimeoutException')
        
        try:
          with open(str(chat_id), 'r') as f:
            print('اررررررررررررررررررروووووووووووووووووووووررررررررررر')
        except FileNotFoundError:
          bot.send_message(chat_id=chat_id, text='ارور. شاید یوزر پس اشتباه باشه.', reply_markup=markup)
        
        
        
        print(user_data)
        try:
            driver.close()
        except Exception as e:
            print(e.args)
            pass
    except Exception as e:
        print(e.args)
        print(user_data)
        print('اررررررررررررررررررررروووووووووووووووووورررررررررر۲۲۲۲۲۲۲۲۲۲۲۲۲')
        #bot.send_message(chat_id=chat_id, text='ارور. شاید یوزر پس اشتباه باشه.', reply_markup=markup)
        try:
            driver.close()
        except Exception as e:
            print(e.args)
