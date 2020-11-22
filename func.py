from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import object_of_lot


def openAndParsePage(browser, link, listOfTenders):
    browser.get(link)
    # getting number of pages
    numberOfTenders = int(browser.find_element_by_xpath("//div[@class='filter__option filter--text pull-left']/div[1]/select/option").text.replace(' ','').replace('Активныеконкурсы:', ''))
    numberOfPages = numberOfTenders // 15
    if numberOfTenders % 15 > 0:
        numberOfPages += 1
    # parsing from each page
    for i in range(numberOfPages):
        parseTendersFromPage(browser, listOfTenders, link)
        if i + 1 != numberOfPages:
            try:
                link = browser.find_element_by_xpath("//ul[@class='pagination']/li[last()]/a[@class='page-link']").get_attribute('href')
                print(link)
                browser.get(link)
            except NoSuchElementException:
                print("\n===  NoSuchElementException  ===")
            finally:
                continue
    for tender in listOfTenders:
        parseTenderLot(browser, tender)
    printLots(listOfTenders)


def parseTendersFromPage(browser, listOfTenders, link):
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
        listForStartDates[i] = listForStartDates[i].text
        listForPurchaseNames[i] = listForPurchaseNames[i].text
        listForCategories[i] = listForCategories[i].text
        listForEndDates[i] = listForEndDates[i].text
        listForCustomerNames[i] = listForCustomerNames[i].text
        listForCustomerCompanyNames[i] = listForCustomerCompanyNames[i].text
        if listForCustomerCompanyNames[i] == "":
            listForCustomerCompanyNames[i] = '-'

    # putting info in list
    for i in range(len(listForLotIDs)):
        size = len(listOfTenders)
        listOfTenders.append(object_of_lot.lot())
        listOfTenders[size].lotID = int(listForLotIDs[i])
        listOfTenders[size].link = (link + "/") + listForLotIDs[i]
        listOfTenders[size].purchaseName = listForPurchaseNames[i]
        listOfTenders[size].startDate = listForStartDates[i]
        listOfTenders[size].endDate = listForEndDates[i]
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
    browser.get(currentTender.link)
    try:
        currentTender.customerAddressArea = browser.find_element_by_xpath("//ul[@class='infos']/li[2]/p[@class='info']").text
    except NoSuchElementException:
        currentTender.customerAddressArea = "-"
    currentTender.deliveryTerm = "Add"
    currentTender.paymentTerm = "Add"
    currentTender.customerPhone = "Add"
    currentTender.customerEmail = "Add"
    currentTender.description = "Add"
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
              "\n  purchaseName\n   ", tender.purchaseName,
              "\n  startDate\n   ", tender.startDate,
              "\n  endDate\n   ", tender.endDate,
              "\n  category\n   ", tender.category,
              "\n  customerName\n   ", tender.customerName,
              "\n  customerCompanyName\n   ", tender.customerCompanyName,
              "\n  customerAddressArea\n   ", tender.customerAddressArea,
              "\n  attachedFile\n   ", tender.attachedFile,
              "\n ============================\n")
        tempCountForPrint += 1