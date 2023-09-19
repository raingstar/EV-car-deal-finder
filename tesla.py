# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time

import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


subject = "Model Y for sale gucci price"
test_body = "This is the body of the text message"
sender = "keyunie@gmail.com"
recipients = "keyunie@gmail.com"
password = "xdiogcewclvcrtlx"


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = body
    msg['To'] = recipients
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

TESLA_URL = 'https://www.tesla.com/inventory/new/my?TRIM=LRAWD&arrangeby=plh&zip=94025&range=200'
tesla_parttern = 'div.results-container.results-container--grid.results-container--has-results'


def watch_tesla():
    TESLA_URL = 'https://www.tesla.com/inventory/new/my?TRIM=LRAWD&arrangeby=plh&zip=94025&range=200'
    tesla_parttern = 'div.results-container.results-container--grid.results-container--has-results'

    # test using Chrome Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(90)

    # Load the URL and get the page source
    driver.get(TESLA_URL)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, tesla_parttern))
    )

    try:
        html = driver.page_source
    except:
        print("An exception occurred")

    if html:
        soup = BeautifulSoup(html, 'lxml')
        cars = [];
        for car_html in soup.select_one(tesla_parttern).findChildren('article'):
            car = {}
            car['price'] = int(car_html.select_one('section.result-header').select_one('div.result-pricing').select_one(
                'div.result-price').select_one('div.result-loan-payment').text.replace(',', '')[1:6])
            car['colour'] = car_html.select('section.result-features.features-grid')[0].select('ul')[1].select('li')[
                0].text
            car['type'] = car_html.select_one('section.result-header').select_one('div.result-basic-info').select_one(
                'h3').text
            car['trim'] = \
            car_html.select_one('section.result-header').select_one('div.result-basic-info').select('div')[0].text
            #             print(car)
            if car['price'] < 47000:
                cars.append(car)
                print("FOUND A CAR for " + str(car['price']) + "$")
        time.sleep(3)  # seconds

    if len(cars):
        body = ",".join([json.dumps(f_car) for f_car in cars])
        send_email(subject, body, sender, recipients, password)
        print("Send email to notify")
    else:
        print("Could not find a deal for model Y")

    driver.quit()

    return cars

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(watch_tesla())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
