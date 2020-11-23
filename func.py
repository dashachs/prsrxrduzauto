from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import object_of_lot


def openAndParsePage(browser, link, listOfTenders):
    browser.get(link)
    tempForLinkText = link
    # getting number of pages
    numberOfTenders = int(browser.find_element_by_xpath("//div[@class='filter__option filter--text pull-left']/div[1]/select/option").text.replace(' ','').replace('Активныеконкурсы:', ''))
    numberOfPages = numberOfTenders // 15
    if numberOfTenders % 15 > 0:
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
    # getting info from table
    listForLotIDs = browser.find_elements_by_xpath("//div[@class='table-responsive']/table/tbody/tr/td[1]/a")
    listForStartDates = browser.find_elements_by_xpath("//div[@class='table-responsive']/table/tbody/tr/td[2]")
    listForPurchaseNames = browser.find_elements_by_xpath("//div[@class='table-responsive']/table/tbody/tr/td[3]")
    listForCategories = browser.find_elements_by_xpath("//div[@class='table-responsive']/table/tbody/tr/td[4]")
    listForEndDates = browser.find_elements_by_xpath("//div[@class='table-responsive']/table/tbody/tr/td[5]")
    listForCustomerNames = browser.find_elements_by_xpath("//div[@class='table-responsive']/table/tbody/tr/td[6]")
    listForCustomerCompanyNames = browser.find_elements_by_xpath("//div[@class='table-responsive']/table/tbody/tr/td[7]")

    for i in range(len(listForCustomerCompanyNames)):
        listForLotIDs[i] = listForLotIDs[i].text
        if listForCustomerNames[i] == "":
            listForCustomerNames[i] = '-'
        listForStartDates[i] = listForStartDates[i].text
        listForEndDates[i] = listForEndDates[i].text
        listForPurchaseNames[i] = listForPurchaseNames[i].text
        if listForPurchaseNames[i] == "":
            listForPurchaseNames[i] = '-'
        listForCategories[i] = listForCategories[i].text
        if listForCategories[i] == "":
            listForCategories[i] = '-'
        listForCustomerNames[i] = listForCustomerNames[i].text
        if listForCustomerNames[i] == "":
            listForCustomerNames[i] = '-'
        listForCustomerCompanyNames[i] = listForCustomerCompanyNames[i].text
        if listForCustomerCompanyNames[i] == "":
            listForCustomerCompanyNames[i] = '-'

    # putting info in list
    for i in range(len(listForLotIDs)):
        size = len(listOfTenders)
        listOfTenders.append(object_of_lot.lot())
        listOfTenders[size].lotID = int(listForLotIDs[i])
        listOfTenders[size].link = (tempForLinkText + "/") + listForLotIDs[i]
        listOfTenders[size].purchaseName = listForPurchaseNames[i]
        listOfTenders[size].startDate = listForStartDates[i][0:10]
        listOfTenders[size].endDate = listForEndDates[i][0:10]
        listOfTenders[size].category = listForCategories[i]
        listOfTenders[size].customerName = listForCustomerNames[i]
        listOfTenders[size].customerCompanyName = listForCustomerCompanyNames[i]
        # parse current

    # clear lists
    listForLotIDs.clear()
    listForStartDates.clear()
    listForPurchaseNames.clear()
    listForCategories.clear()
    listForEndDates.clear()
    listForCustomerNames.clear()
    listForCustomerCompanyNames.clear()


def parseTenderLot(browser, currentTender):
    print("#", currentTender.lotID)
    browser.get(currentTender.link)
    try:
        currentTender.customerAddressArea = browser.find_element_by_xpath("//ul[@class='infos']/li[2]/p[@class='info']").text
    except NoSuchElementException:
        currentTender.customerAddressArea = "-"

    try:
        currentTender.deliveryTerm = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/span/span[text()='II. Условия поставки']/following::p[1]").text
    except NoSuchElementException:
        currentTender.deliveryTerm = "-"
        print("-deliveryTerm")

    currentTender.paymentTerm = "Add"

    try:
        tempForProne = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/span/p[contains(text(),'Тел')]").text.split(":")
        currentTender.customerPhone = tempForProne[-1].replace(' ', '')
        tempForProne.clear()
    except NoSuchElementException:
        currentTender.customerPhone = '-'

    try:
        tempForEmail = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/span/p[contains(text(),'mail')]").text.split(":")
        currentTender.customerEmail = tempForEmail[-1].replace(' ', '')
        tempForEmail.clear()
    except NoSuchElementException:
        currentTender.customerEmail = '-'

    currentTender.description = "Add"
    try:
        currentTender.specialConditions = browser.find_element_by_xpath(
            "//*[@id='product-details']/div[@class='tab-content-wrapper']/p").text
    except NoSuchElementException:
        currentTender.specialConditions = "-"
        print("-specialConditions")

    currentTender.type = "Конкурс"

    content = browser.page_source
    if "Вложение" in content:
        currentTender.attachedFile = currentTender.link + "/download"
    else:
        currentTender.attachedFile = "-"


def printLots(listOfTenders):
    tempCountForPrint = 1
    for tender in listOfTenders:
        print("#", tempCountForPrint,
              "\n  lotID", tender.lotID,
              "\n  type\n   ", tender.type,
              "\n  category\n   ", tender.category,
              "\n  link\n   ", tender.link,
              "\n  startDate\n   ", tender.startDate,
              "\n  endDate\n   ", tender.endDate,
              "\n  status\n   ", tender.status,
              "\n  customerAddressArea\n   ", tender.customerAddressArea,
              "\n  purchaseName\n   ", tender.purchaseName,
              "\n  customerName\n   ", tender.customerName,
              "\n  attachedFile\n   ", tender.attachedFile,
              "\n  paymentTerm\n   ", tender.paymentTerm,
              "\n  customerCompanyName\n   ", tender.customerCompanyName,
              "\n  customerPhone\n   ", tender.customerPhone,
              "\n  customerEmail\n   ", tender.customerEmail,
              "\n  specialConditions\n   ", tender.specialConditions,
              "\n  deliveryTerm\n   ", tender.deliveryTerm,
              "\n ============================\n")
        tempCountForPrint += 1
