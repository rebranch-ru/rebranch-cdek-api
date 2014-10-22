#encoding=utf8
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