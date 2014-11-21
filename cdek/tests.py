# encoding=utf8
import os
from xml.etree.ElementTree import tostring
import datetime
from decimal import Decimal
import uuid
from unittest import TestCase

from cdek.exceptions import CDEKConfigurationError
from cdek.api import CDEKAPI
from cdek.factory import CDEKRequestDeliveryObjectsFactory, CDEKStatusReportObjectsFactory
from cdek.objects.request import ItemRequestObject, AddressRequestObject, PackageRequestObject, OrderRequestObject
from cdek.base import Response, ResponseOrder


class BaseTestCase(TestCase):
    def setUp(self):
        self.request_delivery_factory = CDEKRequestDeliveryObjectsFactory(account=os.getenv(u'CDEK_ACCOUNT'),
                                                                          password=os.getenv(u'CDEK_PASSWORD'))
        self.status_report_factory = CDEKStatusReportObjectsFactory(account=os.getenv(u'CDEK_ACCOUNT'),
                                                                    password=os.getenv(u'CDEK_PASSWORD'))
        self.api_client = CDEKAPI(account=os.getenv(u'CDEK_ACCOUNT'), password=os.getenv(u'CDEK_PASSWORD'))


class TestSerialization(BaseTestCase):
    def test_item_serialization(self):
        item = self.request_delivery_factory.factory_item(
            ware_key=uuid.uuid1().get_hex()[:10],
            cost=Decimal(250.0 * 30),
            payment=Decimal(250.0),
            weight=500,
            weight_brutto=600,
            amount=4,
            comment=u'Комментарий на русском',
            link=u'http://shop.ru/item/42'
        )
        self.assertIsInstance(item, ItemRequestObject)
        tostring(item.to_xml_element(u'Item'), encoding='UTF-8').replace("'", "\"")

    def test_address_serialization(self):
        address = self.request_delivery_factory.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97',
            pvz_code=None
        )
        self.assertIsInstance(address, AddressRequestObject)
        tostring(address.to_xml_element(u'Address'), encoding='UTF-8').replace("'", "\"")

    def test_package_serialization(self):
        items = [
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]

        package = self.request_delivery_factory.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )
        self.assertIsInstance(package, PackageRequestObject)
        tostring(package.to_xml_element(u'Package'), encoding='UTF-8').replace("'", "\"")

    def test_order_serialization(self):
        items = [
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]
        packages = [self.request_delivery_factory.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )]

        address = self.request_delivery_factory.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97'
        )
        order = self.request_delivery_factory.factory_order(
            number=uuid.uuid1().hex[:10],
            date_invoice=datetime.datetime.now(),
            recipient_name=u'Петров Виктор Владимирович',
            recipient_email=u'mail@mail.ru',
            phone=u'+79876543210',
            tariff_type_code=1,
            seller_name=u'ООО "Магазин"',
            address=address,
            packages=packages,
            send_city_post_code=u'123456',
            rec_city_post_code=u'654321'
        )
        self.assertIsInstance(order, OrderRequestObject)
        tostring(order.to_xml_element(tag_name=u'Order'), encoding='UTF-8').replace("'", "\"")

    def test_order_factory_without_sender_code(self):
        items = [
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]
        packages = [self.request_delivery_factory.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )]

        address = self.request_delivery_factory.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97'
        )
        try:
            self.request_delivery_factory.factory_order(
                number=uuid.uuid1().hex[:10],
                date_invoice=datetime.datetime.now(),
                recipient_name=u'Петров Виктор Владимирович',
                recipient_email=u'mail@mail.ru',
                phone=u'+79876543210',
                tariff_type_code=1,
                seller_name=u'ООО "Магазин"',
                address=address,
                packages=packages,
                rec_city_post_code=u'654321'
            )
        except Exception as e:
            self.assertIsInstance(e, CDEKConfigurationError)
        else:
            self.assertTrue(False, u'This is not supposed to happen')

    def test_delivery_reqesut_serialization(self):
        items = [
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]
        packages = [self.request_delivery_factory.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )]

        address = self.request_delivery_factory.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97'
        )
        order = self.request_delivery_factory.factory_order(
            number=uuid.uuid1().hex[:10],
            date_invoice=datetime.datetime.now(),
            recipient_name=u'Петров Виктор Владимирович',
            recipient_email=u'mail@mail.ru',
            phone=u'+79876543210',
            tariff_type_code=1,
            seller_name=u'ООО "Магазин"',
            address=address,
            packages=packages,
            send_city_post_code=u'123456',
            rec_city_post_code=u'654321'
        )
        delivery_request = self.request_delivery_factory.factory_delivery_request(
            orders=[order],
            number=uuid.uuid1().hex[:10],
            date=datetime.datetime.now()
        )
        tostring(delivery_request.to_xml_element(u'DeliveryRequest'))


class TestApi(BaseTestCase):
    def test_delivery_request(self):
        items = [
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.request_delivery_factory.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]
        packages = [self.request_delivery_factory.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )]

        address = self.request_delivery_factory.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97'
        )
        order = self.request_delivery_factory.factory_order(
            number=uuid.uuid1().hex[:10],
            date_invoice=datetime.datetime.now(),
            recipient_name=u'Петров Виктор Владимирович',
            recipient_email=u'mail@mail.ru',
            phone=u'+79876543210',
            tariff_type_code=1,
            seller_name=u'ООО "Магазин"',
            address=address,
            packages=packages,
            send_city_post_code=u'111402',
            rec_city_post_code=u'119332',
            passport_number=u'7575',
            passport_series=u'012345'
        )
        delivery_request = self.request_delivery_factory.factory_delivery_request(
            orders=[order],
            number=uuid.uuid1().hex[:10],
            date=datetime.datetime.now()
        )
        response = self.api_client.make_delivery_request(delivery_request)
        self.assertIsInstance(response, Response)
        self.assertEqual(len(response.data), 1)
        self.assertIsInstance(response.data[0], ResponseOrder)

        def test_status_report(self):
            order = self.status_report_factory.factory_order(dispatch_number=u'1012369182')
            status_report = self.status_report_factory.factory_status_report(order=order, date=datetime.datetime.now())
            self.api_client.make_status_report_request(status_report)
            from nose.tools import set_trace

            set_trace()