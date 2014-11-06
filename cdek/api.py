# coding=utf-8
import urlparse
import requests
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import ElementTree

from cdek.base import ResponseError, ResponseOrder, Response, ResponseStatus


class CDEKAPI(object):
    _api_host = None
    _account = None
    _password = None

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
        api_response = Response(status=Response.STATUS_OK, request_element=xml_element)
        orders = {}
        for api_order in xml_response.findall('Order'):
            order_number = api_order.get(u'Number')
            if api_order.get('ErrorCode'):
                order = orders.get(order_number)
                if not order:
                    order = ResponseOrder(number=order_number)
                    orders[order_number] = order
                error = ResponseError(code=api_order.get(u'ErrorCode'), message=api_order.get(u'Msg'), )
                order.add_error(error)
                api_response.status = api_response.STATUS_FAIL
            elif api_order.get(u'DispatchNumber'):
                order = ResponseOrder(number=order_number, dispatch_number=api_order.get(u'DispatchNumber'))
                orders[order_number] = order
        api_response.data = orders.values()
        return api_response

    def make_status_report_request(self, status_report, method_url=u'status_report_h.php'):
        """
        Производит запрос на получение статуса отправления
        :param basestring method_url:
        :param CDEKDeliveryRequest delivery_request:
        """
        xml_element = status_report.to_xml_element(tag_name=u'StatusReport')
        xml_response = self._make_api_request(xml_element, method_url)
        api_response = Response(status=Response.STATUS_OK, request_element=xml_element)
        orders = {}
        for api_order in xml_response.findall('Order'):
            order_number = api_order.get(u'Number')
            if api_order.get('ErrorCode'):
                order = orders.get(order_number)
                if not order:
                    order = ResponseOrder(number=order_number)
                    orders[order_number] = order
                error = ResponseError(code=api_order.get(u'ErrorCode'), message=api_order.get(u'Msg'), )
                order.add_error(error)
                api_response.status = api_response.STATUS_FAIL
            elif api_order.find(u'Status') is not None:
                api_order_status = api_order.find(u'Status')
                order = ResponseOrder(
                    number=order_number,
                    dispatch_number=api_order.get(u'DispatchNumber'),
                    status=ResponseStatus(
                        city_code=api_order_status.get(u'CityCode'),
                        city_name=api_order_status.get(u'CityName'),
                        code=int(api_order_status.get(u'Code')),
                        date=api_order_status.get(u'Date'),
                        description=api_order_status.get(u'Description')
                    )
                )
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