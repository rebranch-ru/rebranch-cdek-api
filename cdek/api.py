# coding=utf-8
import urlparse
import requests
import hashlib
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import ElementTree

from cdek.objects import CDEKAddress, CDEKOrder, CDEKItem, CDEKPackage, CDEKDeliveryRequest, ApiResponseError, \
    ApiResponseOrder, ApiResponse
from cdek.exceptions import CDEKConfigurationError


class CDEKAPI(object):
    _api_host = None
    _account = None
    _password = None

    class CURRENCIES(object):
        RUB = u'RUB'
        USD = u'USD'
        EUR = u'EUR'
        KZT = u'KZT'
        GBP = u'GBP'
        CNY = u'CNY'
        BYR = u'BYR'
        UAH = u'UAH'

    def __init__(self, account, password, api_host=u'http://gw.edostavka.ru:11443'):
        """
        :param basestring account:
        :param basestring password:
        :param basestring api_host:
        """
        self._account = account
        self._password = password
        self._api_host = api_host

    def make_delivery_request(self, delivery_request, method_url=u'new_orders.php'):
        """
        Производит запрос на регистрацию списка заказов на доставку
        :param basestring method_url:
        :param CDEKDeliveryRequest delivery_request:
        """
        xml_element = delivery_request.to_xml_element(tag_name=u'DeliveryRequest')
        xml_response = self._make_api_request(xml_element, method_url)
        api_response = ApiResponse(status=ApiResponse.STATUS_OK, request_element=xml_element)
        orders = {}
        for api_order in xml_response.findall('Order'):
            order_number = api_order.get(u'Number')
            if api_order.get('ErrorCode'):
                order = orders.get(order_number)
                if not order:
                    order = ApiResponseOrder(number=order_number)
                    orders[order_number] = order
                error = ApiResponseError(code=api_order.get(u'ErrorCode'), message=api_order.get(u'Msg'), )
                order.add_error(error)
                api_response.status = api_response.STATUS_FAIL
            elif api_order.get(u'DispatchNumber'):
                order = ApiResponseOrder(number=order_number, dispatch_number=api_order.get(u'DispatchNumber'))
                orders[order_number] = order
        api_response.data = orders.values()
        return api_response

    def _make_api_request(self, xml_element, method_url):
        xml_document = tostring(xml_element, encoding='UTF-8').replace("'", "\"")
        url = urlparse.urljoin(self._api_host, method_url)
        response = requests.post(
            url=url,
            data={'xml_request': xml_document},
            stream=True
        )
        xml_response = ElementTree()
        xml_response.parse(response.raw)
        return xml_response

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
        address = CDEKAddress(street, house, flat, pvz_code)
        return address

    def factory_item(self, ware_key, cost_ex, cost, payment_ex, payment, weight, weight_brutto, amount, comment_ex,
                     link, comment=None):
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
        item = CDEKItem(ware_key, cost_ex, cost, payment_ex, payment, weight, weight_brutto, amount, comment_ex, link,
                        comment)
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
        package = CDEKPackage(number, bar_code, weight, items, size_a, size_b, size_c)
        return package

    def factory_order(self, number, date_invoice, recipient_name, recipient_email, phone, tariff_type_code,
                      seller_name, seller_address, shipper_name, shipper_address, address, packages,
                      send_city_code=None, rec_city_code=None, send_city_post_code=None, rec_city_post_code=None,
                      passport_series=None, passport_number=None, comment=None):
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
        :param basestring seller_address: Адрес истинного продавца. Используется при печати инвойсов для отображения адреса
        настоящего продавца товара, либо торгового названия
        :param basestring shipper_name:
        :param basestring shipper_address: Адрес грузоотправителя. Используется при печати накладной.
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

        if rec_city_code is None and rec_city_post_code is None:
            raise CDEKConfigurationError(u'rec_city_code либо rec_city_post_code должен быть указан')

        if send_city_code is None and send_city_post_code is None:
            raise CDEKConfigurationError(u'send_city_code либо send_city_post_code должен быть указан')

        date_invoice = date_invoice.isoformat()
        order = CDEKOrder(number, date_invoice, recipient_name, recipient_email, phone,
                          tariff_type_code, seller_name, seller_address, shipper_name, shipper_address, address,
                          packages, send_city_code, rec_city_code, send_city_post_code, rec_city_post_code,
                          passport_series, passport_number, comment)
        return order

    def factory_delivery_request(self, orders, foreign_delivery, number, date, currency):
        """
        Инстанциирует CDEKDeliveryRequest
        :rtype : CDEKDeliveryRequest
        :param list orders:
        :param bool foreign_delivery: Признак международной доставки
        :param basestring number: Номер акта приема-передачи/ТТН
        :param datetime.datetime date: Дата документа (дата заказа)
        :param basestring currency: Идентификатор валюты для указания цен
        :return:
        """
        date = date.isoformat()
        assert isinstance(orders, list)
        md5_object = hashlib.md5()
        md5_object.update(u'{}&{}'.format(date, self._password))
        secure = md5_object.hexdigest()
        delivery_request = CDEKDeliveryRequest(orders, int(foreign_delivery), number, date, currency, self._account,
                                               secure, len(orders))
        return delivery_request