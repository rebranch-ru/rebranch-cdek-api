# coding=utf-8
import hashlib

from cdek.objects import CDEKAddress, CDEKOrder, CDEKItem, CDEKPackage, CDEKDeliveryRequest, CDEKPassport, CDEKCall, \
    CDEKSendAddress, CDEKCallCourier, CDEKAddService
from cdek.exceptions import CDEKConfigurationError


class CDEKObjectsFactoryAbastract(object):
    def __init__(self, account, password):
        """
        :param basestring account:
        :param basestring password:
        :param basestring api_host:
        """
        self._account = account
        self._password = password


class CDEKRequestDeliveryObjectsFactory(CDEKObjectsFactoryAbastract):
    def factory_address(self, street, house, flat, pvz_code=None):
        """
        Инстанциирует CDEKAddress
        :rtype: CDEKAddress
        :param :
        :param basestring street: Улица
        :param basestring house: Дом, корпус, строение
        :param basestring flat: Квартира/Офис
        :param pvz_code: Код ПВЗ (см. «Список пунктов выдачи заказов (ПВЗ)»). Атрибут необходим только для заказов с
        режим доставки «до склада»
        :return:
        """
        address = CDEKAddress(street=street, house=house, flat=flat, pvz_code=pvz_code)
        return address

    def factory_item(self, ware_key, cost, payment, weight, weight_brutto, amount, link, comment=None):
        """
        Инстанциирует CDEKItem
        :rtype : CDEKItem
        :param basestring ware_key: Идентификатор/артикул товара (Уникален в пределах упаковки Package).
        :param float|Decimal cost_ex: Объявленная стоимость товара (за единицу товара в указанной валюте, значение >=0).
        :param float|Decimal cost: Объявленная стоимость товара (за единицу товара в рублях, значение >=0) в рублях.
        С данного значения рассчитывается страховка.
        :param float|Decimal payment_ex: Оплата за товар при получении (за единицу товара в указанной валюте, значение
         >=0) — наложенный платеж, в случае предоплаты значение = 0.
        :param float|Decimal payment: Оплата за товар при получении (за единицу товара в рублях, значение >=0) —
        наложенный платеж, в случае предоплаты значение = 0.
        :param int weight: Вес нетто (за единицу товара, в граммах)
        :param int weight_brutto: Вес брутто (за единицу товара, в граммах)
        :param int amount: Количество единиц товара (в штуках)
        :param basestring comment_ex: Наименование товара  на английском (может также содержать описание товара:
        размер, цвет)
        :param basestring link: Ссылка на сайт интернет-магазина с описанием товара
        :param basestring  comment: Наименование товара на русском (может также содержать описание товара: размер, цвет)
        :return:
        """
        item = CDEKItem(ware_key=ware_key, cost=cost, payment=payment, weight=weight, weight_brutto=weight_brutto,
                        amount=amount, link=link, comment=comment)
        return item

    def factory_package(self, number, weight, items, bar_code=None, size_a=None, size_b=None, size_c=None):
        """
        Инстанциирует CDEKPackage
        :rtype : CDEKPackage
        :param basestring number: Номер упаковки (можно использовать порядковый номер упаковки заказа), уникален в пределах заказа
        :param basestring bar_code: Штрих-код упаковки, если есть
        :param int weight: Общий вес (в граммах)
        :param list items: Список вложений(товаров)
        :param int size_a: Габариты упаковки. Длина (в сантиметрах)
        :param int size_b: Габариты упаковки. Ширина (в сантиметрах)
        :param int size_c: Габариты упаковки. Высота (в сантиметрах)
        :return:
        """
        assert isinstance(items, list)
        # Если bar_code не установлен то установить значение number
        if bar_code is None:
            bar_code = number
        package = CDEKPackage(number=number, bar_code=bar_code, weight=weight, item=items, size_a=size_a,
                              size_b=size_b, size_c=size_c)
        return package

    def factory_order(self, number, date_invoice, recipient_name, recipient_email, phone, tariff_type_code,
                      seller_name, address, packages, send_city_code=None, rec_city_code=None, send_city_post_code=None,
                      rec_city_post_code=None, passport_series=None, passport_number=None, comment=None,
                      call_courier=None, add_service=None, delivery_recipient_cost=None):
        """
        Инстанциирует CDEKOrder
        :rtype : CDEKOrder
        :param basestring number: Номер отправления клиента (должен быть уникален в пределах акта приема-передачи)
        :param datetime.datetime date_invoice: Дата инвойса
        :param basestring recipient_name: Получатель (ФИО)
        :param basestring recipient_email:  RecipientEmail
        :param basestring phone: Телефон получателя
        :param int tariff_type_code: Код типа тарифа (см. Приложение, таблица 1)
        :param basestring seller_name: Истинный продавец. Используется при печати инвойсов для отображения настоящего продавца
        товара, либо торгового названия
        :param CDEKAddress address: Адрес доставки. В зависимости от режима доставки необходимо указывать либо атрибуты
        (Street, House, Flat), либо PvzCode
        :param list packages: Список упаковок
        :param int send_city_code: Код города отправителя из базы СДЭК
        :param int rec_city_code: Код города получателя из базы СДЭК
        :param basestring send_city_post_code: Почтовый индекс города отправителя
        :param basestring rec_city_post_code: Почтовый индекс города получателя
        :param basestring passport_series: Серия паспорта
        :param basestring passport_number: Номер паспорта
        :param comment: Комментарий по заказу
        :return:
        """
        assert isinstance(packages, list)
        assert isinstance(address, CDEKAddress)
        if call_courier is not None:
            assert isinstance(call_courier, CDEKCallCourier)

        if rec_city_code is None and rec_city_post_code is None:
            raise CDEKConfigurationError(u'rec_city_code либо rec_city_post_code должен быть указан')

        if send_city_code is None and send_city_post_code is None:
            raise CDEKConfigurationError(u'send_city_code либо send_city_post_code должен быть указан')

        date_invoice = date_invoice.isoformat()
        passport = CDEKPassport(series=passport_series, number=passport_number)
        order = CDEKOrder(number=number, date_invoice=date_invoice, recipient_name=recipient_name,
                          recipient_email=recipient_email, phone=phone, tariff_type_code=tariff_type_code,
                          seller_name=seller_name, address=address, package=packages, send_city_code=send_city_code,
                          rec_city_code=rec_city_code, send_city_post_code=send_city_post_code,
                          rec_city_post_code=rec_city_post_code, comment=comment, passport=passport,
                          call_courier=call_courier, add_service=add_service,
                          delivery_recipient_cost=delivery_recipient_cost)
        return order

    def factory_delivery_request(self, orders, number, date):
        """
        Инстанциирует CDEKDeliveryRequest
        :rtype : CDEKDeliveryRequest
        :param list orders:
        :param bool foreign_delivery: Признак международной доставки
        :param basestring number: Номер акта приема-передачи/ТТН
        :param datetime.datetime date: Дата документа (дата заказа)
        :return:
        """
        date = date.isoformat()
        assert isinstance(orders, list)
        md5_object = hashlib.md5()
        md5_object.update(u'{}&{}'.format(date, self._password))
        secure = md5_object.hexdigest()
        delivery_request = CDEKDeliveryRequest(order=orders, number=number, date=date, account=self._account,
                                               secure=secure, order_count=len(orders))
        return delivery_request

    def factory_call(self, date, time_beg, time_end, send_city_code, lunch_beg=None, lunch_end=None):
        """
        Инстанциирует CDEKCall
        :rtype : CDEKCall
        :param datetime.date date: Дата ожидания курьера
        :param datetime.time time_beg: Время начала ожидания курьера
        :param datetime.time time_end: Время окончания ожидания курьера
        :param int send_city_code: Код города отправителя из базы СДЭК
        :param datetime.time lunch_beg: Время начала обеда, если входит во временной диапазон [TimeBeg; TimeEnd]
        :param datetime.time lunch_end: Время окончания обеда, если входит во временной диапазон [TimeBeg; TimeEnd]
        :return:
        """
        call = CDEKCall(date=date.isoformat(), time_beg=time_beg.isoformat(), time_end=time_end.isoformat(),
                        send_city_code=send_city_code, lunch_beg=lunch_beg.isoformat(), lunch_end=lunch_end.isoformat())
        return call

    def factory_send_address(self, street, house, flat, send_phone, sender_name, comment=None):
        """
        Инстанциирует CDEKSendAddress
        :rtype : CDEKSendAddress
        :param basestring street:Улица
        :param basestring house:Дом, корпус, строение
        :param basestring flat:Квартира/Офис
        :param basestring send_phone:Контактный телефон отправителя
        :param basestring sender_name:Отправитель (ФИО)
        :param basestring comment:Комментарий
        :return:
        """
        address = CDEKSendAddress(street=street, house=house, flat=flat, send_phone=send_phone, sender_name=sender_name,
                                  comment=comment)
        return address

    def factory_call_courier(self, call, send_address):
        """
        Инстанциирует CDEKCallCourier
        :rtype : CDEKCallCourier
        :param CDEKCall call:
        :param CDEKSendAddress send_address:
        :return:
        """
        assert isinstance(call, CDEKCall)
        assert isinstance(send_address, CDEKSendAddress)
        call_courier = CDEKCallCourier(call=call, send_address=send_address)
        return call_courier

    def factory_add_service(self, service_codes):
        """
        Инстанциирует CDEKAddService
        :param list|tuple|set service_codes: Тип дополнительной услуги
        :return:
        """
        assert isinstance(service_codes, (list, tuple, set))
        add_service = CDEKAddService(service_code=service_codes)
        return add_service