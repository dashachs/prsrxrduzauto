from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from psycopg2 import OperationalError
import psycopg2
import time

import dbUser
import func


def executeParserOrders():
    print("Parsing...")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # create lot's object
    listOfLots = []

    # start chrome browser
    browser = webdriver.Chrome('chromedriver.exe', options=options)

    # open tenders page and parse tenders
    link = 'https://xarid.uzautomotors.com/public/order'
    func.openAndParsePage(browser, link, listOfLots)

    # # reopening browser bc this bitch won't load
    # browser.quit()
    # browser = webdriver.Chrome('chromedriver.exe', options=options)
    #
    # # open contests page
    # link = 'http://etender.uzex.uz/lots/1/0'
    # func.openAndLoadPage(browser, link)
    #
    # # parse contests
    # func.parseFromPage(browser, listOfLots)
    #
    print("Parsed successfully")
    # close browser
    browser.quit()

    # # database input
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

    dbUser.getForEverything(con, listOfLots)

    # adding to DB
    for lot in listOfLots:
        if not dbUser.inTable(con, lot.lotID):
            dbUser.inputToDB(con, lot)

    # find expired lots
    dbUser.findExpiredLots(con)

    print("Database is up-to-date")

    # close DB
    con.close()

    # clear list of lots
    listOfLots.clear()


while True:
    # try:
    executeParserOrders()
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
