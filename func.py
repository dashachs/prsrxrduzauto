from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import object_of_lot


def openAndParsePage(browser, link, listOfLots):
    browser.get(link)
    # getting number of pages
    numberOfTenders = int(browser.find_element_by_xpath("//div[@class='filter__option filter--text pull-left']/div[1]/select/option").text.replace(' ','').replace('Активныеконкурсы:', ''))
    numberOfPages = numberOfTenders // 15
    if numberOfTenders % 15 > 0:
        numberOfPages += 1
    # parsing from each page
    for i in range(numberOfPages):
        parseTendersFromPage(browser, listOfLots)
        if i + 1 != numberOfPages:
            link = browser.find_element_by_xpath("//ul[@class='pagination']/li[last()]/a").get_attribute('href')
            print(link)
            browser.get(link)


def parseTendersFromPage(browser, listOfLots):
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
        size = len(listOfLots)
        print("#", size)
        listOfLots.append(object_of_lot.lot())
        listOfLots[size].lotID = listForLotIDs[i]
        listOfLots[size].purchaseName = listForPurchaseNames[i]
        listOfLots[size].startDate = listForStartDates[i]
        listOfLots[size].endDate = listForEndDates[i]
        listOfLots[size].category = listForCategories[i]
        listOfLots[size].customerName = listForCustomerNames[i]
        listOfLots[size].customerCompanyName = listForCustomerCompanyNames[i]

    printLots(listOfLots)

    # # parse lots
    # for i in range(len(lotNames)):
    #     size = len(listOfLots)
    #     link = "http://etender.uzex.uz/lot/" + lotIDs[i]
    #
    #     # adding new lot to list of lots (adding ID and purchase name)
    #     listOfLots.append(object_of_lot.lot())
    #     listOfLots[size].lotID = lotIDs[i]
    #     listOfLots[size].purchaseName = lotNames[i]
    #     listOfLots[size].customerAddress = lotAddresses[i]
    #     parseLot(browser, link, listOfLots[size])

    # clear lists
    listForLotIDs.clear()
    listForStartDates.clear()
    listForPurchaseNames.clear()
    listForCategories.clear()
    listForEndDates.clear()
    listForCustomerNames.clear()
    listForCustomerCompanyNames.clear()


# def parseFromPage(browser, listOfLots):
#     # search lot's ID and purchase names
#     lotIDs = []
#     lotNames = []
#     lotAddresses = []
#     listForIDs = browser.find_elements_by_xpath("//div[@class ='lot-item__num-cat']/div/span")
#     listForNames = browser.find_elements_by_xpath("//div[@class='lot-item__title']")
#     listOfAddresses = browser.find_elements_by_xpath("//div[@class='lot-item__address']")
#     for i, j, k in zip(listForIDs, listForNames, listOfAddresses):
#         lotIDs.append(i.text)
#         lotNames.append(j.text)
#         lotAddresses.append(k.text)
#
#     # clear lists
#     listForIDs.clear()
#     listForNames.clear()
#     listOfAddresses.clear()
#
#     # parse lots
#     for i in range(len(lotNames)):
#         size = len(listOfLots)
#         link = "http://etender.uzex.uz/lot/" + lotIDs[i]
#
#         # adding new lot to list of lots (adding ID and purchase name)
#         listOfLots.append(object_of_lot.lot())
#         listOfLots[size].lotID = lotIDs[i]
#         listOfLots[size].purchaseName = lotNames[i]
#         listOfLots[size].customerAddress = lotAddresses[i]
#         parseLot(browser, link, listOfLots[size])
#
#     # clear lists
#     lotIDs.clear()
#     lotNames.clear()
#     lotAddresses.clear()


def printLots(listOfLots):
    for lot in listOfLots:
        print("  lotID", lot.lotID,
              "\n  purchaseName\n   ", lot.purchaseName,
              "\n  startDate\n   ", lot.startDate,
              "\n  endDate\n   ", lot.endDate,
              "\n  category\n   ", lot.category,
              "\n  customerName\n   ", lot.customerName,
              "\n  customerCompanyName\n   ", lot.customerCompanyName,
              "\n ============================\n")


# def parseLot(browser, link, currentLot):
#     browser.get(link)
#     # waiting for page to load
#
#
#
# def fillInLot(browser, link, currentLot):
#
#
# def reformatDate(date):
#     dateAndTime = date.split(' ')
#     dayMonthYear = dateAndTime[0].split('-')
#     date = (((((dayMonthYear[2] + '-') + dayMonthYear[1]) + '-') + dayMonthYear[0]) + ' ') + dateAndTime[1]
#     dateAndTime.clear()
#     dayMonthYear.clear()
#     return date

