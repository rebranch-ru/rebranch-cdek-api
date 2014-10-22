# encoding=utf8
from cdek.base import XMLableObject, XMLAttribute


class PassportRequestObject(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'series', True),
        XMLAttribute(u'number', True)
    )


class AddressRequestObject(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'street', True),
        XMLAttribute(u'house', True),
        XMLAttribute(u'flat', True),
        XMLAttribute(u'pvz_code', False)
    )


class ItemRequestObject(XMLableObject):
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


class PackageRequestObject(XMLableObject):
    xml_attributes = (
        XMLAttribute('number', True),
        XMLAttribute('bar_code', True),
        XMLAttribute('weight', True),
        XMLAttribute('item', True),
        XMLAttribute('size_a', False),
        XMLAttribute('size_b', False),
        XMLAttribute('size_c', False)
    )


class OrderRequestObject(XMLableObject):
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


class DeliveryRequestObject(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'order', True),
        XMLAttribute(u'number', True),
        XMLAttribute(u'date', True),
        XMLAttribute(u'account', True),
        XMLAttribute(u'secure', True),
        XMLAttribute(u'order_count', True),
    )


class CallCourierRequestObject(XMLableObject):
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


class SendAddressRequestObject(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'street', True),
        XMLAttribute(u'house', True),
        XMLAttribute(u'flat', True),
        XMLAttribute(u'send_phone', True),
        XMLAttribute(u'sender_name', True),
        XMLAttribute(u'comment', False),
    )


class AddServiceRequestObject(XMLableObject):
    class SERVICE_CODES(object):
        FITTING_AT_HOME = 30  # Курьер доставляет покупателю несколько единиц товара (одежда, обувь и пр.) для примерки.
        # Время ожидания курьера в этом случае составляет 30 минут.
        PARTLY_DELIVERY = 36  # Во время доставки товара покупатель может отказаться от одной или нескольких позиций, и
        # выкупить только часть заказа
        ITEMS_INSPECTION = 37  # Проверка покупателем содержимого заказа до его оплаты (вскрытие посылки).
        DELIVERY_IN_HOLIDAYS = 3  # Осуществление доставки заказа в выходные и нерабочие дни.
        WITHDRAWAL_IN_SENDER_CITY = 16  # Дополнительная услуга забора груза в городе отправителя, при условии что тариф
        # доставки с режимом «от склада»
        DELIVERY_IN_RECIPIENT_CITY = 17  # Дополнительная услуга доставки груза в городе получателя, при условии что
        # тариф доставки с режимом «до склада» (только для тарифов «Магистральный», «Магистральный супер-экспресс»)
        INSURANCE = 2  # Обеспечение страховой защиты посылки. Размер дополнительного сбора страхования вычисляется от
        # размера объявленной стоимости отправления. Важно: Услуга начисляется автоматически для всех заказов ИМ, не
        # разрешена для самостоятельной передачи в тэге AddService.

    xml_attributes = (
        XMLAttribute(u'service_code', True),
    )