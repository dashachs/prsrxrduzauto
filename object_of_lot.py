class lot:
    def __init__(self, lotID=None, type=None, category=None, categoryID=None, linkToLot=None, startDate=None,
                 endDate=None, status='relevant', purchaseName=None, customerName=None, customerCompanyName=None,
                 customerPhone=None, customerEmail=None, customerAddressCountryID=220, customerAddressArea=None,
                 customerAddressAreaID=None, deliveryTerm=None, specialConditions=None, attachedFile=None):
        self.lotID = lotID  # - номер
        self.type = type  # - конкурс/тендер
        self.category = category  # - Категория
        self.categoryID = categoryID  # - ID категории
        self.linkToLot = linkToLot  # - ссылка https://xarid.uzautomotors.com/public/order/ + номер
        self.startDate = startDate  # - Дата подачи
        self.endDate = endDate  # - Срок
        self.status = status  # status — (relevant/expired)
        self.purchaseName = purchaseName  # - Наименование конкурса
        self.customerName = customerName  # -Наименование заказчика +
        self.customerCompanyName = customerCompanyName  # -Реквизиты заказчика
        self.customerPhone = customerPhone
        self.customerEmail = customerEmail
        self.customerAddressCountryID = customerAddressCountryID  # -ID адрес заказчика (country ID)
        self.customerAddressArea = customerAddressArea  # -Адрес заказчика (area)  #+
        self.customerAddressAreaID = customerAddressAreaID  # -ID адрес заказчика (area ID)
        self.deliveryTerm = deliveryTerm  # -Условия поставки
        self.specialConditions = specialConditions  # -Особые условия (условия участия)
        self.attachedFile = attachedFile  # -Прикреплённый файл(ссылка на скачивание)

# номер
# ссылка https://xarid.uzautomotors.com/public/order/ + номер
# Дата подачи startedAt
# Наименование конкурса purchaseName
# Раздел category
# Срок endedAt
# Покупатель customerName
# Компания customerCompanyName
#
