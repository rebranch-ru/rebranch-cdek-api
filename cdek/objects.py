#encoding=utf8
from xml.etree.ElementTree import Element, SubElement, tostring


class XMLableObject(object):
    serializeable_attributes = ()

    def _to_pascal_case(self, attribute_name):
        attribute_name = u''.join([x.capitalize() for x in attribute_name.split(u'_')])
        return attribute_name

    def to_xml_element(self, tag_name, parent=None):
        element = Element(tag_name) if parent is None else SubElement(parent=parent, tag=tag_name)
        for attribute_name in self.serializeable_attributes:
            attribute = getattr(self, attribute_name)
            if attribute is None:
                pass
            elif not isinstance(attribute, (XMLableObject, tuple, list)):
                attribute = attribute if isinstance(attribute, unicode) else str(attribute).decode(u'utf8')
                element.set(self._to_pascal_case(attribute_name), attribute)
            elif isinstance(attribute, (tuple, list)):
                for subattribute in attribute:
                    subattribute.to_xml_element(parent=element, tag_name=self._to_pascal_case(attribute_name))
            elif isinstance(attribute, XMLableObject):
                attribute.to_xml_element(parent=element, tag_name=self._to_pascal_case(attribute_name))
        return element


class CDEKPassport(XMLableObject):
    serializeable_attributes = (u'series', u'number')

    def __init__(self, series, number):
        self.series = series
        self.number = number


class CDEKAddress(XMLableObject):
    serializeable_attributes = (
        u'street',
        u'house',
        u'flat',
        u'pvz_code'
    )

    def __init__(self, street, house, flat, pvz_code=None):
        self.street = street
        self.house = house
        self.flat = flat
        self.pvz_code = pvz_code


class CDEKItem(XMLableObject):
    serializeable_attributes = (
        u'ware_key',
        u'cost_ex',
        u'cost',
        u'payment_ex',
        u'payment',
        u'weight',
        u'weight_brutto',
        u'amount',
        u'comment_ex',
        u'link',
        u'comment'
    )

    def __init__(self, ware_key, cost_ex, cost, payment_ex, payment, weight, weight_brutto, amount, comment_ex, link,
                 comment=None):
        self.ware_key = ware_key
        self.cost_ex = cost_ex
        self.cost = cost
        self.payment_ex = payment_ex
        self.payment = payment
        self.weight = weight
        self.weight_brutto = weight_brutto
        self.amount = amount
        self.comment_ex = comment_ex
        self.link = link
        self.comment = comment


class CDEKPackage(XMLableObject):
    serializeable_attributes = (
        'number',
        'bar_code',
        'weight',
        'item',
        'size_a',
        'size_b',
        'size_c'
    )

    def __init__(self, number, bar_code, weight, items, size_a=None, size_b=None, size_c=None):
        self.number = number
        self.bar_code = bar_code
        self.weight = weight
        self.size_a = size_a
        self.size_b = size_b
        self.size_c = size_c
        self.item = items


class CDEKOrder(XMLableObject):
    serializeable_attributes = (
        u'number',
        u'date_invoice',
        u'recipient_name',
        u'recipient_email',
        u'phone',
        u'tariff_type_code',
        u'seller_name',
        u'seller_address',
        u'shipper_name',
        u'shipper_address',
        u'address',
        u'package',
        u'send_city_code',
        u'rec_city_code',
        u'send_city_post_code',
        u'rec_city_post_code',
        u'passport',
        u'comment'
    )

    def __init__(self, number, date_invoice, recipient_name, recipient_email, phone, tariff_type_code,
                 seller_name, seller_address, shipper_name, shipper_address, address, packages, send_city_code=None,
                 rec_city_code=None, send_city_post_code=None, rec_city_post_code=None, passport_series=None,
                 passport_number=None, comment=None):
        self.number = number
        self.date_invoice = date_invoice
        self.send_city_code = send_city_code
        self.rec_city_code = rec_city_code
        self.send_city_post_code = send_city_post_code
        self.rec_city_post_code = rec_city_post_code
        self.tariff_type_code = tariff_type_code
        self.seller_name = seller_name
        self.seller_address = seller_address
        self.shipper_name = shipper_name
        self.shipper_address = shipper_address
        self.address = address
        self.comment = comment
        self.passport = CDEKPassport(series=passport_series, number=passport_number)
        self.recipient_email = recipient_email
        self.phone = phone
        self.recipient_name = recipient_name
        self.package = packages


class CDEKDeliveryRequest(XMLableObject):
    serializeable_attributes = (
        u'order',
        u'foreign_delivery',
        u'number',
        u'date',
        u'currency',
        u'account',
        u'secure',
        u'order_count'
    )

    def __init__(self, orders, foreign_delivery, number, date, currency, account, secure, order_count):
        self.order = orders
        self.foreign_delivery = foreign_delivery
        self.number = number
        self.date = date
        self.currency = currency
        self.account = account
        self.secure = secure
        self.order_count = order_count


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