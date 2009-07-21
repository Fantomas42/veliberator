"""Models for database"""
from datetime import datetime

from elixir import *

from veliberator.settings import DATABASE_URI, DATABASE_ECHO

class StationInformation(Entity):
    """Station information entity model"""
    id = Field(Integer, primary_key=True)

    address = Field(String(100))
    postal_code = Field(String(100))
    city = Field(String(100))
    
    lat = Field(String(30))
    lng = Field(String(30))

    opened = Field(Boolean)
    bonus = Field(Boolean)

    creation_date = Field(DateTime, default=datetime.now)
    update = Field(DateTime, default=datetime.now)

    using_options(order_by='id',
                  tablename='veliberator_station_information')

    def __repr__(self):
        return '<StationInformation "%s" (%s)>' % (self.id, self.address)

    @property
    def full_address(self):
        return '%s, %s %s' % (self.address,
                              self.postal_code,
                              self.city)


def db_connection(sqluri=DATABASE_URI, echo=DATABASE_ECHO):
    metadata.bind = sqluri
    metadata.bind.echo = echo
    setup_all()
    create_all()
