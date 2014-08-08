#encoding=utf8
import os
from xml.etree.ElementTree import tostring
import datetime
from decimal import Decimal
import uuid
from unittest import TestCase

from cdek.exceptions import CDEKConfigurationError
from cdek.api import CDEKAPI
from cdek.objects import CDEKItem, CDEKAddress, CDEKPackage, CDEKOrder, ApiResponse


class BaseTestCase(TestCase):
    def setUp(self):
        self.api_client = CDEKAPI(account=os.getenv(u'CDEK_ACCOUNT'), password=os.getenv(u'CDEK_PASSWORD'))


class TestSerialization(BaseTestCase):
    def test_item_serialization(self):
        item = self.api_client.factory_item(
            ware_key=uuid.uuid1().get_hex()[:10],
            cost_ex=Decimal(250.0),
            cost=Decimal(250.0 * 30),
            payment=Decimal(250.0),
            payment_ex=Decimal(300.0),
            weight=500,
            weight_brutto=600,
            amount=4,
            comment_ex=u'English comment',
            comment=u'Комментарий на русском',
            link=u'http://shop.ru/item/42'
        )
        self.assertIsInstance(item, CDEKItem)
        tostring(item.to_xml_element(u'Item'), encoding='UTF-8').replace("'", "\"")

    def test_address_serialization(self):
        address = self.api_client.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97',
            pvz_code=None
        )
        self.assertIsInstance(address, CDEKAddress)
        tostring(address.to_xml_element(u'Address'), encoding='UTF-8').replace("'", "\"")

    def test_package_serialization(self):
        items = [
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(450.0),
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                payment_ex=Decimal(500.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(250.0),
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                payment_ex=Decimal(300.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]

        package = self.api_client.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )
        self.assertIsInstance(package, CDEKPackage)
        tostring(package.to_xml_element(u'Package'), encoding='UTF-8').replace("'", "\"")

    def test_order_serialization(self):
        items = [
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(450.0),
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                payment_ex=Decimal(500.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(250.0),
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                payment_ex=Decimal(300.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]
        packages = [self.api_client.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )]

        address = self.api_client.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97'
        )
        order = self.api_client.factory_order(
            number=uuid.uuid1().hex[:10],
            date_invoice=datetime.datetime.now(),
            recipient_name=u'Петров Виктор Владимирович',
            recipient_email=u'mail@mail.ru',
            phone=u'+79876543210',
            tariff_type_code=1,
            seller_name=u'ООО "Магазин"',
            seller_address=u'Москва, ул. 40 лет Октября, 12-22',
            shipper_name=u'СДЭК',
            shipper_address=u'Москва, ул. 90 лет Октября, 12-22',
            address=address,
            packages=packages,
            send_city_post_code=u'123456',
            rec_city_post_code=u'654321'
        )
        self.assertIsInstance(order, CDEKOrder)
        tostring(order.to_xml_element(tag_name=u'Order'), encoding='UTF-8').replace("'", "\"")

    def test_order_factory_without_sender_code(self):
        items = [
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(450.0),
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                payment_ex=Decimal(500.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(250.0),
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                payment_ex=Decimal(300.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]
        packages = [self.api_client.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )]

        address = self.api_client.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97'
        )
        try:
            self.api_client.factory_order(
                number=uuid.uuid1().hex[:10],
                date_invoice=datetime.datetime.now(),
                recipient_name=u'Петров Виктор Владимирович',
                recipient_email=u'mail@mail.ru',
                phone=u'+79876543210',
                tariff_type_code=1,
                seller_name=u'ООО "Магазин"',
                seller_address=u'Москва, ул. 40 лет Октября, 12-22',
                shipper_name=u'СДЭК',
                shipper_address=u'Москва, ул. 90 лет Октября, 12-22',
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
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(450.0),
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                payment_ex=Decimal(500.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(250.0),
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                payment_ex=Decimal(300.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]
        packages = [self.api_client.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )]

        address = self.api_client.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97'
        )
        order = self.api_client.factory_order(
            number=uuid.uuid1().hex[:10],
            date_invoice=datetime.datetime.now(),
            recipient_name=u'Петров Виктор Владимирович',
            recipient_email=u'mail@mail.ru',
            phone=u'+79876543210',
            tariff_type_code=1,
            seller_name=u'ООО "Магазин"',
            seller_address=u'Москва, ул. 40 лет Октября, 12-22',
            shipper_name=u'СДЭК',
            shipper_address=u'Москва, ул. 90 лет Октября, 12-22',
            address=address,
            packages=packages,
            send_city_post_code=u'123456',
            rec_city_post_code=u'654321'
        )
        delivery_request = self.api_client.factory_delivery_request(
            orders=[order],
            foreign_delivery=True,
            number=uuid.uuid1().hex[:10],
            date=datetime.datetime.now(),
            currency=CDEKAPI.CURRENCIES.RUB
        )
        tostring(delivery_request.to_xml_element(u'DeliveryRequest'))


class TestApi(BaseTestCase):
    def test_delivery_request(self):
        items = [
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(450.0),
                cost=Decimal(450.0 * 30),
                payment=Decimal(450.0),
                payment_ex=Decimal(500.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/44'
            ),
            self.api_client.factory_item(
                ware_key=uuid.uuid1().get_hex()[:10],
                cost_ex=Decimal(250.0),
                cost=Decimal(250.0 * 30),
                payment=Decimal(250.0),
                payment_ex=Decimal(300.0),
                weight=500,
                weight_brutto=600,
                amount=4,
                comment_ex=u'English comment',
                comment=u'Комментарий на русском',
                link=u'http://shop.ru/item/42'
            )
        ]
        packages = [self.api_client.factory_package(
            number=uuid.uuid1().hex[:10],
            weight=3000,
            items=items
        )]

        address = self.api_client.factory_address(
            street=u'Ленина',
            house=u'34',
            flat=u'97'
        )
        order = self.api_client.factory_order(
            number=uuid.uuid1().hex[:10],
            date_invoice=datetime.datetime.now(),
            recipient_name=u'Петров Виктор Владимирович',
            recipient_email=u'mail@mail.ru',
            phone=u'+79876543210',
            tariff_type_code=1,
            seller_name=u'ООО "Магазин"',
            seller_address=u'Москва, ул. 40 лет Октября, 12-22',
            shipper_name=u'СДЭК',
            shipper_address=u'Москва, ул. 90 лет Октября, 12-22',
            address=address,
            packages=packages,
            send_city_post_code=u'111402',
            rec_city_post_code=u'119332',
            passport_number=u'7575',
            passport_series=u'012345'
        )
        delivery_request = self.api_client.factory_delivery_request(
            orders=[order],
            foreign_delivery=True,
            number=uuid.uuid1().hex[:10],
            date=datetime.datetime.now(),
            currency=CDEKAPI.CURRENCIES.RUB
        )
        response = self.api_client.make_delivery_request(delivery_request)
        self.assertIsInstance(response, ApiResponse)