# def inputToDB(con, lot):
#     cur = con.cursor()
#     cur.execute(
#         "INSERT INTO etender_uzex_test(lot_number, type, category_id, source_url, started_at, ended_at, status, country_id, region_id, area_id, price, currency_id, purchase_name, customer_name, customer_details, customer_contact, delivery_address, delivery_term, deposit, deposit_payment, advance_payment, payment_method, payment_period, special_conditions, attached_file, description)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#         (lot.lotID, lot.type, lot.categoryID, lot.linkToLot, lot.startedAt, lot.endedAt, lot.status,
#          lot.customerAddressCountryID, lot.customerAddressRegionID, lot.customerAddressAreaID,
#          lot.startingPrice, lot.currencyID, lot.purchaseName, lot.customerName, lot.customerDetails,
#          lot.customerContact, lot.deliveryAddress, lot.deliveryTerm, lot.deposit, lot.depositPayment,
#          lot.advancePayment, lot.paymentMethod, lot.paymentPeriod, lot.specialConditions, lot.attachedFile,
#          lot.description))
#     print("  {} was inserted successfully".format(lot.lotID))
#     con.commit()

# def findExpiredLots(con):
#     cur = con.cursor()
#     # setting timezone for current session to avoid mistakes
#     cur.execute("SET TIMEZONE=5")
#     cur.execute("UPDATE etender_uzex_test SET status = 'expired' WHERE ended_at < now()")
#     con.commit()


def getForEverything(con, listOfLots):  # название временное
    print("Processing data...")
    for lot in listOfLots:
        getForThisLot(con, lot)
        # printLotIDs(lot)
    print("Data was processed successfully\n"
          "Adding to Database...")


def getForThisLot(con, currentLot):
    currentLot.categoryID = getCategoryId(con, currentLot.category)
    currentLot.customerAddressAreaID = getAreaId(con, currentLot.customerAddressArea)


def transliterate(name):
    # Слоаврь с заменами
    dictionary = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
                  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
                  'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
                  'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
                  'ю': 'u', 'я': 'ja', ' ': '-'}
    # Циклически заменяем все буквы в строке
    for key in dictionary:
        name = name.lower().replace(key, dictionary[key])
    return name


def insertInToBiddingCategories(con, name):
    cur = con.cursor()
    cur.execute("SELECT id, slug FROM bidding_categories")
    rows = cur.fetchall()
    for row in rows:
        if row[1] == transliterate(name):
            return row[0]
    cur.execute(
        "INSERT INTO bidding_categories(id, parent_id, depth, path, slug, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, now(), now())",
        (rows[-1][0] + 1,
         41,
         2,
         '/41/{}/'.format(rows[-1][0] + 1),
         transliterate(name)))
    con.commit()
    return rows[-1][0] + 1


def getCategoryId(con, required):
    if required.lower().replace(' ', '') == '':
        required = 'undefined'
    cur = con.cursor()
    cur.execute("SELECT category_id, name, id FROM bidding_categories_translations")
    rows = cur.fetchall()
    for row in rows:
        if row[1].lower().replace(' ', '') == required.lower().replace(' ', ''):
            print("getCategoryId done successfully")
            return row[0]
    print("Category was not found:", required)
    categoryId = insertInToBiddingCategories(con, required)
    cur.execute("INSERT INTO bidding_categories_translations(id, category_id, name, locale) VALUES (%s, %s, %s, %s)",
                (rows[-1][2] + 1,
                 categoryId,
                 required,
                 'rus'))
    cur.execute("INSERT INTO bidding_categories_translations(id, category_id, name, locale) VALUES (%s, %s, %s, %s)",
                (rows[-1][2] + 2,
                 categoryId,
                 required,
                 'uzb'))
    con.commit()
    # print("Category was added to Database successfully")
    rows.clear()
    # return -1
    return categoryId


def getAreaId(con, required):
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
            print("getAreaId done successfully")
            return row[1]
    print("Area was not found:", required)
    # cur.execute("INSERT INTO geo_areas_translations(id, area_id, name, locale) VALUES (%s, %s, %s, %s)",
    #             (rows[-1][0] + 1,
    #              rows[-1][1] + 1,
    #              required,
    #              'rus'))
    # cur.execute("INSERT INTO geo_areas_translations(id, area_id, name, locale) VALUES (%s, %s, %s, %s)",
    #             (rows[-1][0] + 2,
    #              rows[-1][1] + 1,
    #              required,
    #              'uzb'))
    # con.commit()
    # print("Area was added to Database successfully")
    rows.clear()
    return -1
    # return rows[-1][1] + 1


def inTable(con, lotNumber):
    cur = con.cursor()
    cur.execute("SELECT lot_number FROM etender_uzex_test")
    rows = cur.fetchall()
    for row in rows:
        if int(lotNumber) == row[0]:
            return True
    return False
