class lot:
    def __init__(self, lotID=None, type=None, category=None, categoryID=None, linkToLot=None, startDate=None,
                 endDate=None, status='relevant', purchaseName=None, customerName=None, customerCompanyName=None,
                 customerContact=None, customerPhone=None, customerEMail=None, customerAddress=None,
                 customerAddressCountryID=220, customerAddressRegion=None, customerAddressRegionID=None,
                 customerAddressArea=None, customerAddressAreaID=None, deliveryAddress=None, deliveryTerm=None,
                 deposit=None, depositPayment=None, advancePayment=None, paymentMethod=None, paymentPeriod=None,
                 specialConditions=None, attachedFile=None, description=None, startingPrice=None, currency=None,
                 currencyID=None):
        self.lotID = lotID  # - номер
        self.type = type  # - конкурс/тендер
        self.category = category  # - Категория
        self.categoryID = categoryID  # - ID категории
        self.linkToLot = linkToLot  # - ссылка https://xarid.uzautomotors.com/public/order/ + номер
        self.startDate = startDate  # - Дата подачи
        self.endedDate = endDate  # - Срок
        self.status = status  # status — (relevant/expired)
        self.purchaseName = purchaseName  # - Наименование конкурса
        self.customerName = customerName  # -Наименование заказчика +
        self.customerCompanyName = customerCompanyName  # -Реквизиты заказчика
        self.customerContact = customerContact  # -Контакты заказчика (ответственного лица, контактное лицо)
        self.customerPhone = customerPhone
        self.customerEMail = customerEMail
        self.customerAddress = customerAddress  # -Адрес заказчика
        self.customerAddressCountryID = customerAddressCountryID  # -ID адрес заказчика (country ID)
        self.customerAddressRegion = customerAddressRegion  # -Адрес заказчика (region)
        self.customerAddressRegionID = customerAddressRegionID  # -ID адрес заказчика (region ID)
        self.customerAddressArea = customerAddressArea   # -Адрес заказчика (area)  #+
        self.customerAddressAreaID = customerAddressAreaID  # -ID адрес заказчика (area ID)
        self.deliveryAddress = deliveryAddress  # -Адрес поставки +
        self.deliveryTerm = deliveryTerm  # -Условия поставки
        self.deposit = deposit  # -задаток
        self.depositPayment = depositPayment  # - Размер задатка
        self.advancePayment = advancePayment  # -Размер авансового платежа
        self.paymentMethod = paymentMethod  # -Порядок оплаты
        self.paymentPeriod = paymentPeriod  # -Срок расчета (полной оплаты)
        self.specialConditions = specialConditions  # -Особые условия (условия участия)
        self.attachedFile = attachedFile  # -Прикреплённый файл(ссылка на скачивание)
        self.description = description  # -Описание закупки(товар/услуга)
        # self.startingPrice = startingPrice  # - стартовая цена
        # self.currency = currency  # -валюта
        # self.currencyID = currencyID  # -ID валюты

# номер
# ссылка https://xarid.uzautomotors.com/public/order/ + номер
# Дата подачи startedAt
# Наименование конкурса purchaseName
# Раздел category
# Срок endedAt
# Покупатель customerName
# Компания customerCompanyName
#
