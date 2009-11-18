Veliberator
===========

Veliberator provides a Python API for getting informations
about the stations of the Velib' bike renting network.

.. contents::

Binaries
--------

The packages provides few binaries to tests and to initialize the datas.

* synchronize.py

  Must be used at first to grab the general datas about the stations.

* find_place.py

  A test script for finding free places to park a bike or the stations around.

Note that you must run these commands as root until you have not configured 
your own settings.

Usage
-----

To retrieve the informations of a station you only
have to have the ID of the station, and run synchronize.py
to initiate the data.

The in your python interpreter : ::

    >>> from veliberator.stations import Station
    >>> station = Station(42008)
    >>> station.informations.address
    u'128 AVENUE DANIEL CASANOVA'

The informations attributes contains many data such as :

* address
* postal_code
* city
* lat *(the latitude of GPS coordonates)*
* lng *(the longitude of GPS coordonates)*
* opened *(boolean who told if the station is open)*
* bonus *(boolean who told if the station is a bonus station)*

You could retrieve the live status of the station easily : ::

    >>> station.status.available
    24
    >>> station.status.free
    1
  
And we can retrieve the station ids around our station by distance : ::

    >>> station.stations_around
    [42006, 42010, 42012, 42014, 42016, ...]

Other methods on the Station objects are available, but the source is often more explicit.

Settings
========

You can change the settings of the applications by creating or editing the *.veliberator.cfg* 
file in your home directory, basing on the */etc/veliberator.cfg*.

