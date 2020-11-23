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


# def printLotIDs(currentLot):  # temp
#     print("Lot №  ", currentLot.lotID,
#           "\n  categoryID:  ", currentLot.categoryID,
#           "\n  customerAddressRegionID:  ", currentLot.customerAddressRegionID,
#           "\n  customerAddressAreaID:  ", currentLot.customerAddressAreaID,
#           "\n  currencyID:  ", currentLot.currencyID,
#           "\n======================================\n")


def getCategoryId(con, required):
    cur = con.cursor()
    cur.execute("SELECT category_id, name FROM bidding_categories_translations")
    rows = cur.fetchall()
    for row in rows:
        if row[1].lower().replace(' ', '') == required.lower().replace(' ', ''):
            print("getCategoryId done successfully")
            return row[0]
    print("  Category was not found:", required)
    # cur.execute("INSERT INTO bidding_categories_translations(id, category_id, name, locale) VALUES (%s, %s, %s, %s)",
    #             (rows[-1][0] + 1,
    #              rows[-1][1] + 1,
    #              required,
    #              'rus'))
    # cur.execute("INSERT INTO bidding_categories_translations(id, category_id, name, locale) VALUES (%s, %s, %s, %s)",
    #             (rows[-1][0] + 2,
    #              rows[-1][1] + 1,
    #              required,
    #              'uzb'))
    # con.commit()
    # print("Category was added to Database successfully")
    rows.clear()
    return -1
    # return rows[-1][1] + 1

# def getCurrencyId(con, required):
#     cur = con.cursor()
#     cur.execute("SELECT id, slug FROM finance_currencies")
#     rows = cur.fetchall()
#     for row in rows:
#         if row[1].upper().replace(' ', '') == required.upper().replace(' ', ''):
#             # print("getCurrencyId done successfully", required, "ID =", row[0])
#             return row[0]
#     print("  Currency was not found:", required)
    # cur.execute("SET TIMEZONE=5")
    # cur.execute("INSERT INTO finance_currencies(id, slug, created_at, updated_at) VALUES (%s, %s, now(), now())",
    #             (rows[-1][0] + 1,
    #              required))
    # con.commit()
    # print("  Currency was added to Database successfully")
    # # print("Please, add description manually")
    # rows.clear()
    # return -1
    # return rows[-1][0] + 1


# def getRegionId(con, required):
#     cur = con.cursor()
#     cur.execute("SELECT region_id, name FROM geo_regions_translations")
#     rows = cur.fetchall()
#     for row in rows:
#         if row[1].lower().replace(' ', '') == required.replace('город', '').lower().replace(' ', ''):
#             # print("getRegionId done successfully")
#             return row[0]
#     print("  Region was not found:", required)
    # cur.execute("INSERT INTO geo_regions_translations(id, region_id, name, locale) VALUES (%s, %s, %s, %s)",
    #             (rows[-1][0] + 1,
    #              rows[-1][1] + 1,
    #              required,
    #              'rus'))
    # cur.execute("INSERT INTO geo_regions_translations(id, region_id, name, locale) VALUES (%s, %s, %s, %s)",
    #             (rows[-1][0] + 2,
    #              rows[-1][1] + 1,
    #              required,
    #              'uzb'))
    # con.commit()
    # print("  Region  was added to Database successfully")
    # rows.clear()
    # return -1
    # return rows[-1][1] + 1


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
