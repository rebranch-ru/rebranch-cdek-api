#encoding=utf8
from xml.etree.ElementTree import Element, SubElement, tostring


class XMLAttribute(object):
    name = None
    required = None

    def __init__(self, name, required):
        self.name = name
        self.required = required


class XMLableObject(object):
    xml_attributes = ()

    @property
    def attributes(self):
        return [x.name for x in self.xml_attributes]

    def _to_pascal_case(self, attribute_name):
        attribute_name = u''.join([x.capitalize() for x in attribute_name.split(u'_')])
        return attribute_name

    def to_xml_element(self, tag_name, parent=None):
        element = Element(tag_name) if parent is None else SubElement(parent=parent, tag=tag_name)
        for attribute_name in self.attributes:
            attribute = getattr(self, attribute_name)
            if attribute is None:
                pass
            elif not isinstance(attribute, (XMLableObject, tuple, list)):
                attribute = attribute if isinstance(attribute, unicode) else str(attribute).decode(u'utf8')
                element.set(self._to_pascal_case(attribute_name), attribute)
            elif isinstance(attribute, (tuple, list)):
                for subattribute in attribute:
                    if isinstance(subattribute, XMLableObject):
                        subattribute.to_xml_element(parent=element, tag_name=self._to_pascal_case(attribute_name))
                    else:
                        subattribute = unicode(subattribute)
                        element.set(self._to_pascal_case(attribute_name), subattribute)
            elif isinstance(attribute, XMLableObject):
                attribute.to_xml_element(parent=element, tag_name=self._to_pascal_case(attribute_name))
        return element

    def __init__(self, **kwargs):
        for xml_attribute in self.xml_attributes:
            if xml_attribute.required and not xml_attribute.name in kwargs.keys():
                raise TypeError(u'"{}" keyword argument required!'.format(xml_attribute.name))
            elif xml_attribute.name in kwargs.keys():
                setattr(self, xml_attribute.name, kwargs[xml_attribute.name])
        for key in kwargs.keys():
            if not key in self.attributes:
                raise AssertionError(u'Wrong keyword argument "{}"!'.format(key))


class CDEKPassport(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'series', True),
        XMLAttribute(u'number', True)
    )


class CDEKAddress(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'street', True),
        XMLAttribute(u'house', True),
        XMLAttribute(u'flat', True),
        XMLAttribute(u'pvz_code', False)
    )


class CDEKItem(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'ware_key', True),
        XMLAttribute(u'cost', True),
        XMLAttribute(u'payment', True),
        XMLAttribute(u'weight', True),
        XMLAttribute(u'weight_brutto', True),
        XMLAttribute(u'amount', True),
        XMLAttribute(u'link', True),
        XMLAttribute(u'comment', False)
    )


class CDEKPackage(XMLableObject):
    xml_attributes = (
        XMLAttribute('number', True),
        XMLAttribute('bar_code', True),
        XMLAttribute('weight', True),
        XMLAttribute('item', True),
        XMLAttribute('size_a', False),
        XMLAttribute('size_b', False),
        XMLAttribute('size_c', False)
    )


class CDEKOrder(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'number', True),
        XMLAttribute(u'date_invoice', True),
        XMLAttribute(u'recipient_name', True),
        XMLAttribute(u'recipient_email', True),
        XMLAttribute(u'phone', True),
        XMLAttribute(u'tariff_type_code', True),
        XMLAttribute(u'seller_name', True),
        XMLAttribute(u'address', True),
        XMLAttribute(u'package', True),
        XMLAttribute(u'send_city_code', False),
        XMLAttribute(u'rec_city_code', False),
        XMLAttribute(u'passport', True),
        XMLAttribute(u'send_city_post_code', False),
        XMLAttribute(u'rec_city_post_code', False),
        XMLAttribute(u'call_courier', False),
        XMLAttribute(u'comment', False),
        XMLAttribute(u'add_service', False),
        XMLAttribute(u'delivery_recipient_cost', False)
    )


class CDEKDeliveryRequest(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'order', True),
        XMLAttribute(u'number', True),
        XMLAttribute(u'date', True),
        XMLAttribute(u'account', True),
        XMLAttribute(u'secure', True),
        XMLAttribute(u'order_count', True),
    )


class CallCourier(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'call', True),
        XMLAttribute(u'send_address', True),
    )


class CDEKCall(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'date', True),
        XMLAttribute(u'time_beg', True),
        XMLAttribute(u'time_end', True),
        XMLAttribute(u'send_city_code', True),
        XMLAttribute(u'lunch_beg', False),
        XMLAttribute(u'lunch_end', False),
    )


class CDEKSendAddress(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'street', True),
        XMLAttribute(u'house', True),
        XMLAttribute(u'flat', True),
        XMLAttribute(u'send_phone', True),
        XMLAttribute(u'sender_name', True),
        XMLAttribute(u'comment', False),
    )


class CDEKCallCourier(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'call', True),
        XMLAttribute(u'send_address', True),
    )


class CDEKAddService(XMLableObject):
    class SERVICE_CODES(object):
        FITTING_AT_HOME = 30  #Курьер доставляет покупателю несколько единиц товара (одежда, обувь и пр.) для примерки.
        # Время ожидания курьера в этом случае составляет 30 минут.
        PARTLY_DELIVERY = 36  #Во время доставки товара покупатель может отказаться от одной или нескольких позиций, и
        # выкупить только часть заказа
        ITEMS_INSPECTION = 37  #Проверка покупателем содержимого заказа до его оплаты (вскрытие посылки).
        DELIVERY_IN_HOLIDAYS = 3  #Осуществление доставки заказа в выходные и нерабочие дни.
        WITHDRAWAL_IN_SENDER_CITY = 16  #Дополнительная услуга забора груза в городе отправителя, при условии что тариф
        # доставки с режимом «от склада»
        DELIVERY_IN_RECIPIENT_CITY = 17  #Дополнительная услуга доставки груза в городе получателя, при условии что
        # тариф доставки с режимом «до склада» (только для тарифов «Магистральный», «Магистральный супер-экспресс»)
        INSURANCE = 2  #Обеспечение страховой защиты посылки. Размер дополнительного сбора страхования вычисляется от
        # размера объявленной стоимости отправления. Важно: Услуга начисляется автоматически для всех заказов ИМ, не
        # разрешена для самостоятельной передачи в тэге AddService.

    xml_attributes = (
        XMLAttribute(u'service_code', True),
    )


class ApiResponseError(object):
    code = None
    message = None

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __repr__(self):
        return '<ApiResponseError: {}>'.format(self.code)


class ApiResponseOrder(object):
    number = None
    dispatch_number = None
    errors = None

    def __init__(self, number, dispatch_number=None, errors=None):
        self.number = number
        self.dispatch_number = dispatch_number
        self.errors = errors or []

    def __repr__(self):
        return '<ApiOrder: {}>'.format(self.number)

    def add_error(self, error):
        self.errors.append(error)


class ApiResponse(object):
    status = None
    request_element = None

    STATUS_OK = u'ok'
    STATUS_FAIL = u'fail'

    def __init__(self, status, request_element, data=None):
        self.status = status
        self.data = data
        self.request_element = request_element

    def __repr__(self):
        return u'<ApiResponse: {}>'.format(self.status)