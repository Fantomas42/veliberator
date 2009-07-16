"""Xml functions for helping in convertion of data"""

def xml_station_status_wrapper(xmlnode):
    """Convert Station status xml
    to a usable dict"""
    
    return {'total': int(xmlnode.getElementsByTagName('total')[0].childNodes[0].data),
            'available': int(xmlnode.getElementsByTagName('available')[0].childNodes[0].data),
            'free': int(xmlnode.getElementsByTagName('free')[0].childNodes[0].data),
            'ticket': int(xmlnode.getElementsByTagName('ticket')[0].childNodes[0].data) == 1}
 

def xml_station_information_wrapper(xmlnode):
    """Convert Station information xml
    to a usable dict"""

    address_parts = xmlnode.getAttribute('fullAddress').split('-')
    
    address = address_parts[0].strip()
    try:
        postal_code = address_parts[1].strip().split(' ')[0]
        city = ' '.join(address_parts[1].strip().split(' ')[1:])
    except IndexError:
        city = ''
        postal_code = ''
        
    return {'id': int(xmlnode.getAttribute('number')),
            'address': address,
            'postal_code': postal_code,
            'city': city,
            'lat': xmlnode.getAttribute('lat'),
            'lng': xmlnode.getAttribute('lng'),
            'opened': xmlnode.getAttribute('open') == '1',
            'bonus': xmlnode.getAttribute('bonus') == '1',}
