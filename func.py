from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import lot
import time


def toCutString(text, length=255):
    for i in range(length-5, 0, -1):
        if text[i] == '.' or text[i] == ';':
            text = text[0:i+1]+'..'
            return text


def openAndParsePage(browser, link, listOfTenders):
    browser.get(link)
    tempForLinkText = link
    # getting number of pages
    numberOfTenders = int(browser.find_element_by_xpath("//*[@id='results']/div/div[@class='row']/div[@class='col-md-6']/h4/strong/span[@class='badge badge-secondary']").text.replace(' ',''))
    numberOfTendersOnPage = len(browser.find_elements_by_xpath("/html/body/main/div[3]/div/div[@class='col-lg-12']/div"))
    numberOfPages = numberOfTenders // numberOfTendersOnPage
    if numberOfTenders % numberOfTendersOnPage > 0:
        numberOfPages += 1
    # parsing from each page
    for i in range(numberOfPages):
        parseTendersFromPage(browser, listOfTenders, tempForLinkText)
        if i + 1 != numberOfPages:
            try:
                link = browser.find_element_by_xpath("//ul[@class='pagination']/li[last()]/a[@class='page-link']").get_attribute('href')
                # print(link)
                browser.get(link)
            except NoSuchElementException:
                print("\n===  NoSuchElementException  ===")
            finally:
                continue
    # for tender in listOfTenders:
    #     parseTenderLot(browser, tender)
    printLots(listOfTenders)


def parseTendersFromPage(browser, listOfTenders, tempForLinkText):
    # making all elements visible
    invisible_divs = browser.find_elements_by_xpath("//div[@class='strip_list wow fadeIn']")
    for div in invisible_divs:
        script = "arguments[0].style.visibility = 'visible';"
        browser.execute_script(script, div)

    # getting info from page
    list_for_lot_numbers = browser.find_elements_by_xpath("//div[@class='row']/div[@class='col-lg-6 strip_list_center']/ul/li[@class='strip_list_ow']/a")
    list_for_started_at = browser.find_elements_by_xpath("//div[@class='row']/div[@class='col-lg-6 strip_list_center']/ul/li[contains(text(), 'Дата подачи') and @class='strip_list_ow']")
    list_for_ended_at = browser.find_elements_by_xpath("//*[@id='my-soon-counter']")
    list_for_names = browser.find_elements_by_xpath("//div[@class='col-lg-12']/div/p/a")
    list_for_categories = browser.find_elements_by_xpath("//div[@class='col-lg-12']/div/small/a")

    # formating text
    for i in range(len(list_for_lot_numbers)):
        list_for_lot_numbers[i] = list_for_lot_numbers[i].text.replace(' ', '').replace('ID:', '')
        list_for_started_at[i] = list_for_started_at[i].text.replace('Дата подачи : ', '')
        list_for_ended_at[i] = list_for_ended_at[i].get_attribute('data-due')
        list_for_names[i] = list_for_names[i].text
        if list_for_names[i] == "":
            list_for_names[i] = None
        list_for_categories[i] = list_for_categories[i].text.replace('#', '')
        if list_for_categories[i] == "":
            list_for_categories[i] = None

    # putting info in list
    for i in range(len(list_for_lot_numbers)):
        size = len(listOfTenders)
        listOfTenders.append(lot.Lot())
        listOfTenders[size].number = list_for_lot_numbers[i]
        listOfTenders[size].source_url = (tempForLinkText + "/") + list_for_lot_numbers[i]
        listOfTenders[size].name = list_for_names[i]
        listOfTenders[size].started_at = list_for_started_at[i][0:19]
        listOfTenders[size].ended_at = list_for_ended_at[i][0:19]
        listOfTenders[size].category = list_for_categories[i]
        listOfTenders[size].type = 'tender'

    # clear lists
    list_for_lot_numbers.clear()
    list_for_started_at.clear()
    list_for_names.clear()
    list_for_categories.clear()
    list_for_ended_at.clear()


def parseTenderLot(browser, currentTender):
    browser.get(currentTender.linkToLot)
    try:
        currentTender.customerAddressArea = browser.find_element_by_xpath("//ul[@class='infos']/li[2]/p[@class='info']").text
    except NoSuchElementException:
        currentTender.customerAddressArea = "-"

    try:
        currentTender.deliveryTerm = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/span/span[text()='II. Условия поставки']/following::p[1]").text
        if len(currentTender.deliveryTerm) >= 255:
            currentTender.deliveryTerm = toCutString(currentTender.deliveryTerm)
    except NoSuchElementException:
        currentTender.deliveryTerm = None

    try:
        currentTender.paymentTerm = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/span/b[text()='III. Условия оплаты']/following::*[2]").text
        if len(currentTender.paymentTerm) >= 255:
            currentTender.paymentTerm = toCutString(currentTender.paymentTerm)
    except NoSuchElementException:
        currentTender.paymentTerm = None

    try:
        tempForProne = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/span/p[contains(text(),'Тел')]").text.split(":")
        currentTender.customerPhone = tempForProne[-1].replace(' ', '')
        tempForProne.clear()
    except NoSuchElementException:
        currentTender.customerPhone = None

    try:
        tempForEmail = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/span/p[contains(text(),'mail')]").text.split(":")
        currentTender.customerEmail = tempForEmail[-1].replace(' ', '')
        tempForEmail.clear()
    except NoSuchElementException:
        currentTender.customerEmail = None

    try:
        currentTender.specialConditions = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/p").text
        if len(currentTender.specialConditions) >= 255:
            currentTender.specialConditions = toCutString(currentTender.specialConditions)
    except NoSuchElementException:
        currentTender.specialConditions = None

    currentTender.type = "tender"

    content = browser.page_source
    if "Вложение" in content:
        currentTender.attachedFile = currentTender.linkToLot + "/download"
    else:
        currentTender.attachedFile = None


def printLots(listOfTenders):
    tempCountForPrint = 1
    for tender in listOfTenders:
        print("#", tempCountForPrint,
              "\n  number\n   ", tender.number,
              "\n  type\n   ", tender.type,
              "\n  category\n   ", tender.category,
              "\n  source_url\n   ", tender.source_url,
              "\n  started_at\n   ", tender.started_at,
              "\n  ended_at\n   ", tender.ended_at,
              # "\n  status\n   ", tender.status,
              # "\n  customerAddressArea\n   ", tender.customerAddressArea,
              "\n  name\n   ", tender.name,
              # "\n  customerName\n   ", tender.customerName,
              # "\n  attachedFile\n   ", tender.attachedFile,
              # "\n  paymentTerm\n   ", tender.paymentTerm,
              # "\n  customerCompanyName\n   ", tender.customerCompanyName,
              # "\n  customerPhone\n   ", tender.customerPhone,
              # "\n  customerEmail\n   ", tender.customerEmail,
              # "\n  specialConditions\n   ", tender.specialConditions,
              # "\n  deliveryTerm\n   ", tender.deliveryTerm,
              "\n ============================\n")
        tempCountForPrint += 1
