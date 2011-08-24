"""Xml functions for helping in convertion of data"""


def xml_station_status_wrapper(xmlnode):
    """Convert Station status xml
    to a usable dict"""
    def node_value(name):
        return xmlnode.getElementsByTagName(name)[0].childNodes[0].data

    return {'total': int(node_value('total')),
            'available': int(node_value('available')),
            'free': int(node_value('free')),
            'ticket': int(node_value('ticket')) == 1}


def xml_station_information_wrapper(xmlnode):
    """Convert Station information xml
    to a usable dict"""
    city = ''
    postal_code = ''
    address = xmlnode.getAttribute('address')[:-1].strip()
    address_parts = xmlnode.getAttribute('fullAddress').split()

    for p in address_parts:
        if len(p) == 5 and p.isdigit():
            postal_code = p
            city = ' '.join(address_parts[address_parts.index(p) + 1:])
            break

    return {'id': int(xmlnode.getAttribute('number')),
            'address': address,
            'postal_code': postal_code,
            'city': city,
            'lat': xmlnode.getAttribute('lat'),
            'lng': xmlnode.getAttribute('lng'),
            'opened': xmlnode.getAttribute('open') == '1',
            'bonus': xmlnode.getAttribute('bonus') == '1'}
