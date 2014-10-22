from cdek.base import XMLAttribute, XMLableObject


class OrderStatusObject(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'dispatch_number', False),
        XMLAttribute(u'number', False),
        XMLAttribute(u'date', False),
    )


class ChangePeriodStatusObject(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'date_first', True),
        XMLAttribute(u'date_last', True),
    )


class StatusReportObject(XMLableObject):
    xml_attributes = (
        XMLAttribute(u'order', False),
        XMLAttribute(u'change_period', False),
        XMLAttribute(u'date', True),
        XMLAttribute(u'account', True),
        XMLAttribute(u'secure', True),
        XMLAttribute(u'show_history', False),
    )