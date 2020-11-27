def transliterate(name):
    # Слоаврь с заменами
    dictionary = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
                  'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                  'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '',
                  'э': 'e', 'ю': 'u', 'я': 'ja', ' ': '-'}
    # Циклически заменяем все буквы в строке
    for key in dictionary:
        name = name.lower().replace(key, dictionary[key])
    return name


def in_table(con, lotNumber):
    # Проверяем на наличие лота в таблице
    cur = con.cursor()
    cur.execute("SELECT number FROM bidding_lots")
    rows = cur.fetchall()
    for row in rows:
        if int(lotNumber) == row[0]:
            rows.clear()
            return True
    return False


def find_expired_lots(con):
    # находим просроченные лоты и изменяем их статус
    cur = con.cursor()
    # setting timezone for current session to avoid mistakes
    cur.execute("SET TIMEZONE=5")
    cur.execute("UPDATE bidding_lots SET status = 'expired' WHERE ended_at < now()")
    con.commit()


def add_category(con, name):
    # добавить новую категорию в таблицу и вернуть новый id
    cur = con.cursor()
    cur.execute("SELECT id, slug FROM bidding_categories")
    rows = cur.fetchall()
    for row in rows:
        if row[1] == transliterate(name):
            return row[0]
    category_id = rows[-1][0] + 1
    cur.execute(
        "INSERT INTO bidding_categories(id, parent_id, depth, path, slug, created_at, updated_at) VALUES (%s, %s, %s, "
        "%s, %s, now(), now())", (category_id, 41, 2, '/41/{}/'.format(rows[-1][0] + 1), transliterate(name)))
    con.commit()
    rows.clear()
    return category_id


def get_category_id(con, required):
    # вернуть id категории лота (если нет, то создать)
    if required.lower().replace(' ', '') == '':
        required = 'undefined'
    cur = con.cursor()
    cur.execute("SELECT category_id, name, id FROM bidding_categories_translations")
    rows = cur.fetchall()
    for row in rows:
        if row[1].lower().replace(' ', '') == required.lower().replace(' ', ''):
            return row[0]
    print("Category was not found:", required)
    category_id = add_category(con, required)
    cur.execute("INSERT INTO bidding_categories_translations(id, category_id, name, locale) VALUES (%s, %s, %s, %s)",
                (rows[-1][2] + 1, category_id, required, 'rus'))
    cur.execute("INSERT INTO bidding_categories_translations(id, category_id, name, locale) VALUES (%s, %s, %s, %s)",
                (rows[-1][2] + 2, category_id, required, 'uzb'))
    con.commit()
    rows.clear()
    return category_id


def get_source_id(con, required):
    # вернуть id источника (если нет, то добавить заранее вручную)
    cur = con.cursor()
    cur.execute("SELECT id, url FROM bidding_sources")
    rows = cur.fetchall()
    for row in rows:
        if row[1] in required:
            return row[0]
    print("Source was not found:", required)


def get_subject_id(con, required):
    cur = con.cursor()
    cur.execute("SELECT id name FROM bidding_subjects")
    rows = cur.fetchall()
    for row in rows:
        if row[1].lower.replace(' ', '') == required.lower().replace(' ', ''):
            return row[0]
    print("subject was not found:", required)
    # надо дописать действия при отсутсвии информации

# def get_currency_id(con, required):


# def get_country_id(con, required):


# def get_region_id(con, required):



def get_area_id(con, required):
    cur = con.cursor()
    cur.execute("SELECT id, area_id, name FROM geo_areas_translations")
    rows = cur.fetchall()
    scrap = required
    scrap = scrap.lower()
    scrap = scrap.replace(' ', '')
    scrap = scrap.replace('район', '')
    scrap = scrap.replace('р-он', '')
    scrap = scrap.replace('г.', '')
    scrap = scrap.replace('p', 'р')
    for row in rows:
        if scrap in row[2].lower().replace(' ', ''):
            return row[1]
    print("Area was not found:", required)
    rows.clear()
    return -1


def get_for_this_lot(con, currentLot):
    currentLot.categoryID = get_category_id(con, currentLot.category)
    currentLot.customerAddressAreaID = get_area_id(con, currentLot.customerAddressArea)


def get_for_everything(con, listOfLots):  # название временное
    print("Processing data...")
    for lot in listOfLots:
        get_for_this_lot(con, lot)
    print("Data was processed successfully\n"
          "Adding to Database...")


def save_lot(con, lot):
    cur = con.cursor()
    cur.execute(
        "INSERT INTO xarid_uzauto_test(lot_number, type, category_id, source_url, started_at, ended_at, status, "
        "country_id, area_id, purchase_name, customer_name, delivery_term, attached_file, payment_term, "
        "customer_company_name, customer_phone, customer_email, special_conditions) "
        "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
            lot.lotID, lot.type, lot.categoryID, lot.linkToLot, lot.startDate, lot.endDate, lot.status,
            lot.customerAddressCountryID, lot.customerAddressAreaID, lot.purchaseName, lot.customerName,
            lot.deliveryTerm, lot.attachedFile, lot.paymentTerm, lot.customerCompanyName, lot.customerPhone,
            lot.customerEmail, lot.specialConditions))
    print("{} was inserted successfully".format(lot.lotID))
    con.commit()
