import copy

from selenium.common.exceptions import WebDriverException, NoSuchElementException
import lot


def to_cut_string(text, length=255):
    for i in range(length - 5, 0, -1):
        if text[i] == '.' or text[i] == ';':
            text = text[0:i + 1] + '..'
            return text


def crop_name(name):
    text1 = "онкурс на "
    text2 = "онкурс по "
    text3 = "ендер на"
    text4 = "ендер по"
    if text1 in name:
        temp_for_name = name.split(text1)
        name = temp_for_name[1]
    elif text2 in name:
        temp_for_name = name.split(text2)
        name = temp_for_name[1]
    elif text3 in name:
        temp_for_name = name.split(text3)
        name = temp_for_name[1]
    elif text4 in name:
        temp_for_name = name.split(text4)
        name = temp_for_name[1]
    name = name.capitalize()
    return name


def open_and_parse_page(browser, link, list_of_tenders):
    browser.get(link)
    temp_for_link_text = link
    # getting number of pages
    number_of_tenders = int(browser.find_element_by_xpath(
        "//*[@id='results']/div/div[@class='row']/div[@class='col-md-6']/h4/strong/span[@class='badge badge-secondary']").text.replace(
        ' ', ''))
    number_of_tenders_on_page = len(
        browser.find_elements_by_xpath("/html/body/main/div[3]/div/div[@class='col-lg-12']/div"))
    number_of_pages = number_of_tenders // number_of_tenders_on_page
    if number_of_tenders % number_of_tenders_on_page > 0:
        number_of_pages += 1
    # parsing from each page
    for i in range(number_of_pages):
        parse_tenders_from_page(browser, list_of_tenders, temp_for_link_text)
        if i + 1 != number_of_pages:
            try:
                link = browser.find_element_by_xpath(
                    "//ul[@class='pagination']/li[last()]/a[@class='page-link']").get_attribute('href')
                browser.get(link)
            except NoSuchElementException:
                pass

    link1 = "https://xarid.uzautomotors.com/public/corp"
    browser.get(link1)
    subject_name = browser.find_element_by_xpath("//div[@class='box_list wow fadeIn animated']/div/h5").text
    subject_phone = browser.find_element_by_xpath("//div[@class='box_list wow fadeIn animated']/div/p/a").text
    subject_address = browser.find_element_by_xpath(
        "//div[@class='box_list wow fadeIn animated']/div/p[2]").text.replace('Местонахождение', '').replace(': ', '').replace(':', '')
    subject_email = browser.find_element_by_xpath("//div[@class='box_list wow fadeIn animated']/div/a").text

    for tender in list_of_tenders:
        tender.phone = subject_phone
        tender.subject_address = subject_address
        tender.email = subject_email
        tender.subject = subject_name
        if not tender.is_sublot:
            parse_tender_lot(browser, tender, list_of_tenders)


def parse_tenders_from_page(browser, list_of_tenders, tempForLinkText):
    # making all elements visible
    invisible_divs = browser.find_elements_by_xpath("//div[@class='strip_list wow fadeIn']")
    for div in invisible_divs:
        script = "arguments[0].style.visibility = 'visible';"
        browser.execute_script(script, div)

    # getting info from page
    list_for_lot_numbers = browser.find_elements_by_xpath(
        "//div[@class='row']/div[@class='col-lg-6 strip_list_center']/ul/li[@class='strip_list_ow']/a")
    list_for_started_at = browser.find_elements_by_xpath(
        "//div[@class='row']/div[@class='col-lg-6 strip_list_center']/ul/li[contains(text(), 'Дата подачи') and @class='strip_list_ow']")
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
        size = len(list_of_tenders)
        list_of_tenders.append(lot.Lot())
        list_of_tenders[size].number = list_for_lot_numbers[i]
        list_of_tenders[size].source_url = (tempForLinkText + "/") + list_for_lot_numbers[i]
        list_of_tenders[size].name = list_for_names[i]
        list_of_tenders[size].started_at = list_for_started_at[i][0:19]
        list_of_tenders[size].ended_at = list_for_ended_at[i][0:19]
        list_of_tenders[size].category = list_for_categories[i]
        list_of_tenders[size].type = 'tender'

    # clear lists
    list_for_lot_numbers.clear()
    list_for_started_at.clear()
    list_for_names.clear()
    list_for_categories.clear()
    list_for_ended_at.clear()


def create_sublot(row_number, row, current_tender, list_of_tenders):
    number = len(list_of_tenders)
    list_of_tenders.append(lot.Lot())
    list_of_tenders[number] = copy.deepcopy(current_tender)
    list_of_tenders[number].is_sublot = True
    list_of_tenders[number].description_short = row
    list_of_tenders[number].number = current_tender.number + "_" + str(row_number)


def get_sublots_from_table(temp_rows, current_tender, list_of_tenders):
    count = 0
    current_tender.name = crop_name(current_tender.name)
    # checking again
    if "№" in temp_rows[0].text[0:2]:
        del temp_rows[0]
    # checking for empty lines and deleting them
    for i in range(len(temp_rows)):
        if len(temp_rows[i].text.replace('\n', '').replace(' ', '')) < 3:
            del temp_rows[i]
            i -= 1
    # creating sublots
    for row in temp_rows:
        # formatting text and deleting number
        row = row.text.replace('\n', ' ').replace(str(count + 1) + " ", '')
        if count == 0:
            current_tender.description_short = row
        else:
            create_sublot(count, row, current_tender, list_of_tenders)
        count += 1


def get_description(browser, current_tender, list_of_tenders):
    try:
        # checking if there's table
        table = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Предмет')]/following::div[1]/div[@class='col-lg-12']/table/tbody")
        # there is a table
        # checking if this table has sublots and not just info
        try:
            first_col = browser.find_element_by_xpath(
                "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Предмет')]/following::div[1]/div[@class='col-lg-12']/table/tbody/tr[1]/td[1]").text
            if "№" not in first_col and "1" not in first_col:  # if there's no sublots
                # no sublots, just info
                current_tender.description_short = browser.find_element_by_xpath(
                    "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Предмет')]/following::div[1]/div[@class='col-lg-12']/table/tbody/tr[1]/td[2]").text
            else:
                # table of sublots
                temp_rows = browser.find_elements_by_xpath(
                    "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Предмет')]/following::div[1]/div[@class='col-lg-12']/table/tbody/tr")
                # deleting description row and then getting sublots
                if "№" in temp_rows[0].text:
                    del temp_rows[0]
                get_sublots_from_table(temp_rows, current_tender, list_of_tenders)
        except NoSuchElementException:
            current_tender.description_short = current_tender.name
    except NoSuchElementException:
        # that's not a table
        try:
            browser.find_element_by_xpath(
                "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Предмет')]/following::div[1]/div[@class='col-lg-12']/p[contains(text(),'№')]")
            # just text but imitating table
            current_tender.description_short = current_tender.name
        except NoSuchElementException:
            # no table at all, just text
            try:
                current_tender.description_short = browser.find_element_by_xpath(
                    "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Предмет')]/following::div[1]/div[@class='col-lg-12']/*[text()]").text
            except NoSuchElementException:
                try:
                    current_tender.description_short = browser.find_element_by_xpath(
                        "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Предмет')]/following::div[1]/div[@class='col-lg-12']/*/*[text()]").text
                except NoSuchElementException:
                    # not even text
                    current_tender.description_short = None
    # if empty description
    if len(current_tender.description_short.replace('\n', '').replace(' ', '')) < 3:
        current_tender.description_short = None


def parse_tender_lot(browser, current_tender, list_of_tenders):
    browser.get(current_tender.source_url)

    try:
        current_tender.delivery_term = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'поставки')]/following::div[1]/div[@class='col-lg-12']/*").text
        if len(current_tender.delivery_term) >= 255:
            current_tender.delivery_term = to_cut_string(current_tender.delivery_term)
    except NoSuchElementException:
        current_tender.delivery_term = None
    current_tender.delivery_conditions = current_tender.delivery_term

    try:
        temp_for_payment_term = browser.find_elements_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'оплаты')]/following::div[1]/div[@class='col-lg-12']/*")
        for temp in temp_for_payment_term:
            if temp.text != "":
                current_tender.payment_term = temp.text
                break
        temp_for_payment_term.clear()
        if len(current_tender.payment_term) >= 255:
            current_tender.payment_term = to_cut_string(current_tender.payment_term)
    except NoSuchElementException:
        current_tender.payment_term = None

    try:
        current_tender.phone2 = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Контакты')]/following::div[1]/div[@class='col-lg-12']/*/*[contains(text(),'Тел')]/following::*[1]").text
    except NoSuchElementException:
        current_tender.phone2 = None

    try:
        current_tender.email2 = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Контакты')]/following::div[1]/div[@class='col-lg-12']/*/*[contains(text(),'mail')]/following::*[1]").text
    except NoSuchElementException:
        current_tender.email2 = None

    try:
        current_tender.purchase_conditions = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/p[@class='text-center']").text
        if len(current_tender.purchase_conditions) >= 255:
            current_tender.purchase_conditions = to_cut_string(current_tender.purchase_conditions)
    except NoSuchElementException:
        current_tender.purchase_conditions = None

    # getting requisites (temporary variables just in case)
    try:
        requisites = browser.find_element_by_xpath(
            "//div[@class='box_general_2']/div[@class='main_title_4']/h3[contains(text(),'Реквизит')]/following::div[1]/div[@class='col-lg-12']/p").text
    except NoSuchElementException:
        requisites = None
    temp_for_company_name = None
    temp_for_bank = None
    temp_for_mfo = None
    if requisites is not None:
        list_of_requisites = requisites.replace("\n", ":").replace(": ", ":").split(":")
        for i in range(len(list_of_requisites)):
            if i != len(list_of_requisites) - 1:
                if "Реквизитлар" in list_of_requisites[i]:
                    temp_for_company_name = list_of_requisites[i + 1]
                if "ИНН" in list_of_requisites[i]:
                    current_tender.itin = list_of_requisites[i + 1]
                    temp_for_bank = list_of_requisites[i + 2]
                if "МФО" in list_of_requisites[i]:
                    temp_for_mfo = list_of_requisites[i + 1]
                if "Хисоб ракам" in list_of_requisites[i]:
                    current_tender.bank_account = list_of_requisites[i + 1].replace(' ', '')

    content = browser.page_source  # or "//*[contains(text(),'Скачать прикрепленный файл')]"
    if "Скачать прикрепленный файл" in content:
        current_tender.attached_file = browser.find_element_by_xpath(
            "//div[@class='row add_bottom_45']/div[@class='col-lg-12']/center/a").get_attribute('href')
    else:
        current_tender.attached_file = None

    get_description(browser, current_tender, list_of_tenders)
    current_tender.name = crop_name(current_tender.name)


# def print_lots(list_of_tenders):
#     temp_count_for_print = 1
#     for tender in list_of_tenders:
#         print("#", temp_count_for_print,
#               "\n  number\n   ", tender.number,
#               "\n  type\n   ", tender.type,
#               "\n  category\n   ", tender.category,
#               "\n  source_url\n   ", tender.source_url,
#               "\n  started_at\n   ", tender.started_at,
#               "\n  ended_at\n   ", tender.ended_at,
#               "\n  description_short\n   ", tender.description_short,
#               # "\n  customerAddressArea\n   ", tender.customerAddressArea,
#               "\n  name\n   ", tender.name,
#               # "\n  customerName\n   ", tender.customerName,
#               "\n  attached_file\n   ", tender.attached_file,
#               "\n  payment_term\n   ", tender.payment_term,
#               # "\n  customerCompanyName\n   ", tender.customerCompanyName,
#               # "\n  customerPhone\n   ", tender.customerPhone,
#               # "\n  customerEmail\n   ", tender.customerEmail,
#               "\n  purchase_conditions\n   ", tender.purchase_conditions,
#               "\n  delivery_term\n   ", tender.delivery_term,
#               "\n  email2\n   ", tender.email2,
#               "\n  phone2\n   ", tender.phone2,
#               "\n  phone\n   ", tender.phone,
#               "\n  subject_address\n   ", tender.subject_address,
#               "\n  email\n   ", tender.email,
#               "\n  subject\n   ", tender.subject,
#               "\n ============================\n")
#         temp_count_for_print += 1
