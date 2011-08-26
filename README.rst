Veliberator
===========

**Veliberator** is a Python module who provides an API for getting the
informations related to the stations of the Velib' bike renting network.


.. contents::

API Usage
---------

To retrieve the informations of a station you only have to have the ID of
the station and a database synchronized with all the available stations.

Then in your Python interpreter you can play with the API:
::
    >>> from veliberator.stations import Station
    >>> station = Station(42008)
    >>> station.informations.address
    u'128 AVENUE DANIEL CASANOVA'

The informations attributes contains many data such as:

* ``address``
* ``postal_code``
* ``city``
* ``lat`` *(the latitude of the GPS coordonates)*
* ``lng`` *(the longitude of the GPS coordonates)*
* ``opened`` *(True if the station is open)*
* ``bonus`` *(True if the station is a bonus station)*

You could retrieve the live status of the station easily:
::

    >>> station.status.available
    24
    >>> station.status.free
    1
    >>> station.status.total
    25
    >>> station.status.closed
    0

More useful, you can retrieve the closest stations sorted by distance:
::

    >>> station.stations_around
    [<StationInformation "42006" (23 RUE PIERRE BROSSOLETTE)>, <StationInformation "42010" (1 RUE ROBESPIERRE)>, ...]

The **veliberator** script
--------------------------

Write an API for developers is a nice idea, but write an useful script
who uses the API for the end-user is a much nicer idea.

So the package provide a script named ``veliberator``.

For exemple if I need to know the status of the Velib' station with the ID:
*42008*, I simply need to run this command:
::

  $ veliberator 42008

This command will display the status of the station and find other stations
around if no parking place are available.

The ``veliberator`` script can also find the Velib' stations around an
address, by simply launching the script.

Note that at the first run of the script a database will be created for
registering all the available stations.

For update or create the database you can run this command:
::

  $ veliberator --synchronize

Run this command for more informations:
::

  $ veliberator -h

Settings
--------

The veliberator module has a configuration file needed for running, this
file contains all the options of the module.

So you can change the options of the module and the script simply by editing
the ``.veliberator.cfg`` file located in your home directory.
