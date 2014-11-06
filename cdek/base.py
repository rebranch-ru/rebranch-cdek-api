# encoding=utf8
from xml.etree.ElementTree import Element, SubElement


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


class ResponseError(object):
    code = None
    message = None

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __repr__(self):
        return '<ApiResponseError: {}>'.format(self.code)


class ResponseOrder(object):
    number = None
    dispatch_number = None
    errors = None
    status = None

    def __init__(self, number, dispatch_number=None, errors=None, status=None):
        self.number = number
        self.dispatch_number = dispatch_number
        self.errors = errors or []
        self.status = status


    def __repr__(self):
        return '<ApiOrder: {}>'.format(self.number)

    def add_error(self, error):
        self.errors.append(error)


class ResponseStatus(object):
    city_code = None
    city_name = None
    code = None
    date = None
    description = None

    STATUS_CODE_REGISTERED = 1
    # Заказ зарегистрирован в базе данных СДЭК

    STATUS_CODE_DELETED = 2
    # Заказ отменен ИМ после регистрации в системе до прихода груза на склад СДЭК в городе-отправителе

    STATUS_CODE_ACCEPTED_TO_SENDER_STORAGE = 3
    # Оформлен приход на склад СДЭК в городе-отправителе.

    STATUS_CODE_ISSUED_TO_SEND_FROM_SENDER_STORAGE = 6
    # Оформлен расход со склада СДЭК в городе-отправителе. Груз подготовлен к отправке (консолидирован с другими
    # посылками)

    STATUS_CODE_RETURNED_TO_SENDER_STORAGE = 16
    # Повторно оформлен приход в городе-отправителе (не удалось передать перевозчику по какой-либо причине)

    STATUS_CODE_ISSUED_TO_SHIPPER_IN_SENDER_STORAGE = 7
    # Зарегистрирована отправка в городе-отправителе. Консолидированный груз передан на доставку (в аэропорт/загружен
    # машину)

    STATUS_CODE_SENT_TO_TRANSIT_CITY = 21
    # Зарегистрирована отправка в город-транзит. Проставлены дата и время отправления у перевозчика

    STATUS_CODE_RECEIVED_IN_TRANSIT_CITY = 22
    # Зарегистрирована встреча в городе-транзите

    STATUS_CODE_ACCEPTED_TO_TRANSIT_STORAGE = 13
    # Оформлен приход в городе-транзите

    STATUS_CODE_RETURNED_TO_TRANSIT_STORAGE = 17
    # Повторно оформлен приход в городе-транзите (груз возвращен на склад)

    STATUS_CODE_ISSUED_TO_SEND_FROM_TRANSIT_STORAGE = 19
    # Оформлен расход в городе-транзите

    STATUS_CODE_ISSUED_TO_SHIPPER_IN_TRANSIT_STORAGE = 20
    # Зарегистрирована отправка у перевозчика в городе-транзите

    STATUS_CODE_SENT_TO_RECEIVER_CITY = 8
    # Зарегистрирована отправка в город-получатель, груз в пути.

    STATUS_CODE_RECEIVED_IN_RECEIVER_CITY = 9
    # Зарегистрирована встреча груза в городе-получателе

    STATUS_CODE_ACCEPTED_TO_RECEIVER_STORAGE = 10
    # Оформлен приход на склад города-получателя., ожидает доставки до двери

    STATUS_CODE_ACCEPTED_TO_RECEIVER_STORAGE_POSTE_RESTANTE = 12
    # Оформлен приход на склад города-получателя. Доставка до склада, посылка ожидает забора клиентом - покупателем ИМ

    STATUS_CODE_ISSUED_TO_DELIVER = 11
    # Добавлен в курьерскую карту, выдан курьеру на доставку

    STATUS_CODE_RETURNED_TO_RECEIVER_STORAGE = 18
    # Оформлен повторный приход на склад в городе-получателе. Доставка не удалась по какой-либо причине, ожидается
    # очередная попытка доставки

    STATUS_CODE_DELIVERED = 4
    # Успешно доставлен и вручен адресату

    STATUS_CODE_RETURNED = 5
    # Покупатель отказался от покупки, возврат в ИМ

    def __init__(self, city_code, city_name, code, date, description):
        self.city_code = city_code
        self.city_name = city_name
        self.code = code
        self.date = date
        self.description = description


class Response(object):
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