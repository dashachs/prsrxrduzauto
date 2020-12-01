from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from psycopg2 import OperationalError
import psycopg2
import time

import db
import func


def execute_parser_orders():
    print("Parsing...")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # create lot's object
    list_of_lots = []

    # start chrome browser
    browser = webdriver.Chrome('chromedriver.exe', options=options)

    # open tenders page and parse tenders
    link = 'https://xarid.uzautomotors.com/public/order'
    func.open_and_parse_page(browser, link, list_of_lots)

    print("Parsed successfully")
    # close browser
    browser.quit()

    # database input
    while True:
        try:
            con = psycopg2.connect(
                database="postgres",
                user="anwar",
                password="etender.uz",
                host="database-rds.cbs8omqsohea.eu-west-3.rds.amazonaws.com",
                port="5432"
            )
        except OperationalError:
            print("Failed to connect to the server. connection...")
        else:
            print("Database was opened successfully")
            break

    db.get_for_everything(con, list_of_lots)

    # adding to DB
    for lot in list_of_lots:
        if not db.in_table(con, lot.number, lot.source_url):
            db.save_lot(con, lot)

    # find expired lots
    db.find_expired_lots(con)





    print("Database is up-to-date")

    # close DB
    con.close()

    # clear list of lots
    list_of_lots.clear()


while True:
    # try:
    execute_parser_orders()
    # except TimeoutException:
    #     print("TIMEOUT_EXCEPTION")
    # except WebDriverException:
    #     print("WEB_DRIVER_EXCEPTION")
    # except:
    #     print("ERROR")
    # finally:
        # setting repeating time
    timerTime = 90
    print("\n~~~~~~~~~~~~~~~~~~~~~\n"
          "Parser will start again in", timerTime, "seconds"
          "\n~~~~~~~~~~~~~~~~~~~~~\n")
    time.sleep(timerTime)
