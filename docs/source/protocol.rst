Protocol definition
===================

This page explain the protocol used by pioneer N-50A.
The explaination is revert engineering of network player with wireshark.

The communication between your application and the player is a socket opened on port 8102.
If you use a NAS to store your files you must use http to retrieve the cover of songs.
The protocol have two command type, the first is the command without response and the second is command with response.


Network player
--------------


Power
~~~~~

This section exaplain how to manage the power of your player

+-------+---------+
| order | command |
+=======+=========+
| ON    | PO\\r   |
+-------+---------+
| OFF   | PF\\r   |
+-------+---------+


To know the state of your player you can send the command


+--------+---------+
| order  | command |
+========+=========+
| status | ?P\\r   |
+--------+---------+

the response of this command is

+--------+----------+
| status | response |
+========+==========+
| ON     | PWR0     |
+--------+----------+
| OFF    | PWR2     |
+--------+----------+


Input
~~~~~

+-----------------+---------+
| input           | command |
+=================+=========+
| DAC             | 13FN\\r |
+-----------------+---------+
| ipod/usb front  | 17FN\\r |
+-----------------+---------+
| radio           | 38FN\\r |
+-----------------+---------+
| NAS             | 44FN\\r |
+-----------------+---------+
| favorite        | 45FN\\r |
+-----------------+---------+
| spotify         | 57FN\\r |
+-----------------+---------+
| digital input 1 | 59FN\\r |
+-----------------+---------+
| digital input 2 | 60FN\\r |
+-----------------+---------+
| ipod/usb rear   | 61FN\\r |
+-----------------+---------+

To know the input selected by your network player you can use the following command:

+--------+---------+
| order  | command |
+========+=========+
| status | ?F\\r   |
+--------+---------+

the response of this command is

+-----------------+----------+
| input           | response |
+=================+==========+
| DAC             | FN13     |
+-----------------+----------+
| ipod/usb front  | FN17     |
+-----------------+----------+
| radio           | FN38     |
+-----------------+----------+
| NAS             | FN44     |
+-----------------+----------+
| favorite        | FN45     |
+-----------------+----------+
| spotify         | FN57     |
+-----------------+----------+
| digital input 1 | FN59     |
+-----------------+----------+
| digital input 2 | FN60     |
+-----------------+----------+
| ipod/usb rear   | FN61     |
+-----------------+----------+

Music player
~~~~~~~~~~~~

+------------------+----------+
| order            | commande |
+==================+==========+
| play             | 10PB\\r  |
+------------------+----------+
| pause            | 11PB\\r  |
+------------------+----------+
| precedent        | 12PB\\r  |
+------------------+----------+
| suivant          | 13PB\\r  |
+------------------+----------+
| stop             | 20PB\\r  |
+------------------+----------+
| entrer           | 30PB\\r  |
+------------------+----------+
| return           | 31PB\\r  |
+------------------+----------+
| ajoute au favori | 32PB\\r  |
+------------------+----------+
| repeat           | 34PB\\r  |
+------------------+----------+
| shuffle          | 35PB\\r  |
+------------------+----------+


Screen status
~~~~~~~~~~~~~

to know the informations display on screen you can execute the following command:


+--------+---------+
| order  | command |
+========+=========+
| status | ?GAP\\r |
+--------+---------+

this command return the following responses:

+---------------------------+-------------------------+
| type of information       | response                |
+===========================+=========================+
| screen header information | GCPaabcdefghijkkklmm"n" | 
+---------------------------+-------------------------+
| screen information        | GDPaaaaabbbbbccccc      |
+---------------------------+-------------------------+
| screen line information   | GEPaabcc"d"             |
+---------------------------+-------------------------+

Often the response contains several value of this table. 

Example for a screen on song played::

    'GBP08\r\nGCP02110100000110200""\r\nGDP000010000100001\r\nGEP01020"Milk"\r\nGEP02021"Garbage"\r\nGEP03022"Garbage"\r\nGEP04026"mp3"\r\nGEP05028""\r\nGEP06029"320kbps"\r\nGEP07023"0:23"\r\nGEP08034"3:52"\r\n'

Example when screen display a song list::

    'GBP08\r\nGCP01110100000000200"Garbage"\r\nGDP000010000800012\r\nGEP01002"Supervixen"\r\nGEP02102"Queer"\r\nGEP03002"Only Happy When It Rains"\r\nGEP04002"As Heaven Is Wide"\r\nGEP05002"Not My Idea"\r\nGEP06002"A Stroke Of Luck"\r\nGEP07002"Vow"\r\nGEP08002"Stupid Girl"\r\n'

GBP
***

First instructtion returned when the scrren status is required, explain the number of GEP must be parsed.

+-----+----+
| GBP | aa |
+-----+----+

Each field have following description

+-------+------------------------------------+
| field | description                        |
+=======+====================================+
| aa    | number of line displayed on screen |
+-------+------------------------------------+

GCP
***

This response is send to describe the view

+-----+----+---+---+---+---+---+---+---+---+---+-----+---+----+-----+
| GCP | aa | b | c | d | e | f | g | h | i | j | kkk | l | mm | "n" |
+-----+----+---+---+---+---+---+---+---+---+---+-----+---+----+-----+

Example::

    GCP01110100000000200"Garbage"


Each field have following description

+-------+-------------------------+
| field | description             |
+=======+=========================+
| aa    | screen type             |
+-------+-------------------------+
| b     |                         | 
+-------+-------------------------+
| c     | top menu button enabled |
+-------+-------------------------+
| d     |                         |
+-------+-------------------------+
| e     | return button enabled   |
+-------+-------------------------+
| f     |                         |
+-------+-------------------------+
| g     | shuffle enable          |
+-------+-------------------------+
| h     | repeat enabled          |
+-------+-------------------------+
| i     |                         |
+-------+-------------------------+
| j     |                         |
+-------+-------------------------+
| kkk   | view type               | 
+-------+-------------------------+
| l     | play status             |
+-------+-------------------------+
| mm    |                         |
+-------+-------------------------+
| n     | title                   |
+-------+-------------------------+


The screen type can be have several value described in following table:

+------+----------------------+
| code | description          |
+======+======================+
| 00   | error                |
+------+----------------------+
| 01   | list                 |
+------+----------------------+
| 02   | file info            |
+------+----------------------+
| 03   | file info with pause |
+------+----------------------+
| 06   | loading              |
+------+----------------------+

The view can be display several type of informations.

+------+-------------------------------------------+
| code | description                               |
+======+===========================================+
| 000  | the view is a list                        |
+------+-------------------------------------------+
| 002  | the view display the root of music server |
+------+-------------------------------------------+
| 110  | the view display information of file      |
+------+-------------------------------------------+

The play field display the state of current play

+------+-------------+
| code | description |
+======+=============+
| 0    | stopped     |
+------+-------------+
| 1    | pause       |
+------+-------------+
| 2    | play        |
+------+-------------+


GDP
***

+-----+-------+-------+-------+
| GDP | aaaaa | bbbbb | ccccc |
+-----+-------+-------+-------+

Example::

    GDP000010000800012


+-------+-------------------------+
| field | description             |
+=======+=========================+
| aaaaa | first line at screen    |
+-------+-------------------------+
| bbbbb | last line at screen     |
+-------+-------------------------+
| ccccc | total number of lines   |
+-------+-------------------------+

GEP
***

+-----+----+---+----+-----+
| GEP | aa | b | cc | "d" |
+-----+----+---+----+-----+

Example::

    GEP01002"Supervixen"


+-------+----------------+
| field | description    |
+=======+================+
| aa    | number of line |
+-------+----------------+
| b     | selected line  |
+-------+----------------+
| cc    |                |
+-------+----------------+
| "d"   | text of line   |
+-------+----------------+


Image information
~~~~~~~~~~~~~~~~~


+---------------+---------+
| order         | command |
+===============+=========+
| get image url | ?GIC\\r |
+---------------+---------+


response

+-----+-----+-----+
| GIC | aaa | "b" |
+-----+-----+-----+


+-------+----------------+
| field | description    |
+=======+================+
| aaa   | size of url    |
+-------+----------------+
| b     | url of picture |
+-------+----------------+


Directory information
~~~~~~~~~~~~~~~~~~~~~

Instead of read the screen information of directory you can request directly the information of directories and retrieve the picture associated.


+--------------------------------+-------------------+
| order                          | command           |
+================================+===================+
| get directory list and picture | ?GIAaaaaabbbbb\\r |
+--------------------------------+-------------------+

+-------+--------------------------+
| field | description              |
+=======+==========================+
| aaaaa | number of the first line |
+-------+--------------------------+
| bbbbb | number of the last line  |
+-------+--------------------------+



response

+-----+-------+-------+-----+----+-----+-----+-----+
| GIB | aaaaa | bbbbb | ccc | dd | "e" | fff | "g" |
+-----+-------+-------+-----+----+-----+-----+-----+

Example::

    GIB000020000201016"Toute la musique"066"http://127.0.0.1:5000/transcoder/jpegtnscaler.cgi/ebdart/23320.jpg"

Each field ahve following description

+-------+-----------------------------------------------------+
| field | description                                         |
+=======+=====================================================+
| aaaaa | number of line displayed on screen (between 1 & 8 ) |
+-------+-----------------------------------------------------+
| bbbbb | number of line                                      |
+-------+-----------------------------------------------------+
| ccc   |                                                     |
+-------+-----------------------------------------------------+
| dd    | number of characters in directory name              |
+-------+-----------------------------------------------------+
| e     | directory name                                      |
+-------+-----------------------------------------------------+
| fff   | number of characters in picture url                 |
+-------+-----------------------------------------------------+
| g     | picture url                                         |
+-------+-----------------------------------------------------+



Amplifactor
-----------


Power
~~~~~

The power of amplificator is little different than power of network player.
You have only one command to start and stop the amplificator.
Also it is not possible to know the state of power of amplificator.

+------------+-----------------+
| order      | command         |
+============+=================+
| Start/Stop | 0A51CFFFFROI\\r |
+------------+-----------------+


Volume
~~~~~~

+-------+-----------------+
| order | command         |
+=======+=================+
| up    | 0A50AFFFFROI\\r |
+-------+-----------------+
| down  | 0A50BFFFFROI\\r |
+-------+-----------------+

Source
~~~~~~

+--------+-----------------+
| order  | command         |
+========+=================+
| change | 0A555FFFFROI\\r |
+--------+-----------------+


