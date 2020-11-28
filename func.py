from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import lot


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
    for tender in listOfTenders:
        parseTenderLot(browser, tender)
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

    # formatting text
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
    browser.get(currentTender.source_url)

    try:
        currentTender.delivery_term = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'поставки')]/following::div[1]/div[@class='col-lg-12']/*").text
        if len(currentTender.delivery_term) >= 255:
            currentTender.delivery_term = toCutString(currentTender.delivery_term)
    except NoSuchElementException:
        currentTender.delivery_term = None
    currentTender.delivery_conditions = currentTender.delivery_term

    try:
        temp_for_payment_term = browser.find_elements_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'оплаты')]/following::div[1]/div[@class='col-lg-12']/*")
        for temp in temp_for_payment_term:
            if temp.text != "":
                currentTender.payment_term = temp.text
                break
        temp_for_payment_term.clear()
        if len(currentTender.payment_term) >= 255:
            currentTender.payment_term = toCutString(currentTender.payment_term)
    except NoSuchElementException:
        currentTender.payment_term = None

    try:
        currentTender.phone = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Контакты')]/following::div[1]/div[@class='col-lg-12']/*/*[contains(text(),'Тел')]/following::*[1]").text
    except NoSuchElementException:
        currentTender.phone = None

    try:
        currentTender.email2 = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Контакты')]/following::div[1]/div[@class='col-lg-12']/*/*[contains(text(),'mail')]/following::*[1]").text
    except NoSuchElementException:
        currentTender.email2 = None

    try:
        currentTender.purchase_conditions = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/p[@class='text-center']").text
        if len(currentTender.purchase_conditions) >= 255:
            currentTender.purchase_conditions = toCutString(currentTender.purchase_conditions)
    except NoSuchElementException:
        currentTender.purchase_conditions = None

    # получение реквизитов (временные переменные)
    try:
        requisites = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Реквизит')]/following::div[1]/div[@class='col-lg-12']/p").text
    except NoSuchElementException:
        requisites = None
    temp_for_company_name = None
    temp_for_tin = None
    temp_for_bank = None
    temp_for_mfo = None
    temp_for_hisob_raqam = None
    if requisites is not None:
        list_of_requisites = requisites.replace("\n", ":").replace(": ", ":").split(":")
        for i in range(len(list_of_requisites)):
            if i != len(list_of_requisites) - 1:
                if "Реквизитлар" in list_of_requisites[i]:
                    temp_for_company_name = list_of_requisites[i + 1]
                if "ИНН" in list_of_requisites[i]:
                    temp_for_tin = list_of_requisites[i + 1]
                    temp_for_bank = list_of_requisites[i + 2]
                if "МФО" in list_of_requisites[i]:
                    temp_for_mfo = list_of_requisites[i + 1]
                if "Хисоб ракам" in list_of_requisites[i]:
                    temp_for_hisob_raqam = list_of_requisites[i + 1]

        # content = browser.page_source  # или "//*[contains(text(),'Скачать прикрепленный файл')]"
    # if "Скачать прикрепленный файл" in content:
    #     currentTender.attachedFile = currentTender.source_url + "/download"
    # else:
    #     currentTender.attachedFile = None


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
              "\n  payment_term\n   ", tender.payment_term,
              # "\n  customerCompanyName\n   ", tender.customerCompanyName,
              # "\n  customerPhone\n   ", tender.customerPhone,
              # "\n  customerEmail\n   ", tender.customerEmail,
              "\n  purchase_conditions\n   ", tender.purchase_conditions,
              "\n  delivery_term\n   ", tender.delivery_term,
              "\n  email2\n   ", tender.email2,
              "\n  phone\n   ", tender.phone,
              "\n ============================\n")
        tempCountForPrint += 1
