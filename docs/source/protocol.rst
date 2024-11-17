Définition du protocol
======================


Cette page explique le protocol de communication pioneer qui a été utlisé pour le lecteur reseau N-50A.
Cette documentation a été obtenu par ingenieurie inverse a l'aide de l'outil wireshark, d'un lecteur N-50A et de l'application control.

lecteur <-- ethernet --> pc <-- wifi --> smartphone

La communication entre l'application et le lecteur s'effectue sur un socker ouvert avec le port 8102.
Les details de communication peuvent etre obtenu par upnp a l'aide d'un requete ssdp.
Cependant la reponse retourné par le lecteur contient un xml malformé et ne peux etre lu par les librairie upnp standard.
Si un NAS est utilisé pour stocker les fichier, il est possible d'utiliser http pour retrouver les jacquettes des musiques.
Le protocol utilise deux types de commandes, le premier type est une commande sans reponse et le second est une commande avec reponse



A faire
-------

    - Comprendre l'usage de la commande ICA ainsi que ses réponses

Lecteur reseau
--------------


Alimentation
~~~~~~~~~~~~

Cette section explique comment controller l'alimation du lecteur

+-------+----------+
| ordre | commande |
+=======+==========+
| ON    | PO\\r    |
+-------+----------+
| OFF   | PF\\r    |
+-------+----------+


Pour connaitre le status de votre lecteur vous pouvez envoyer la commande suivante

+--------+----------+
| ordre  | commande |
+========+==========+
| status | ?P\\r    |
+--------+----------+


La réponse de cette commande est

+--------+----------+
| status | réponse  |
+========+==========+
| ON     | PWR0     |
+--------+----------+
| OFF    | PWR2     |
+--------+----------+


Entrées
~~~~~~~

+--------------------+----------+
| entrée             | commande |
+====================+==========+
| DAC                | 13FN\\r  |
+--------------------+----------+
| ipod/usb façade    | 17FN\\r  |
+--------------------+----------+
| radio              | 38FN\\r  |
+--------------------+----------+
| NAS                | 44FN\\r  |
+--------------------+----------+
| favoris            | 45FN\\r  |
+--------------------+----------+
| spotify            | 57FN\\r  |
+--------------------+----------+
| entrée numérique 1 | 59FN\\r  |
+--------------------+----------+
| entrée numérique 2 | 60FN\\r  |
+--------------------+----------+
| ipod/usb arrière   | 61FN\\r  |
+--------------------+----------+

Pour connaitre l'entrée selectionné par votre lecteur réseau, vous pouvez utiliser la commande suivante:

+--------+----------+
| ordre  | commande |
+========+==========+
| status | ?F\\r    |
+--------+----------+

La réponse de cette commande est

+--------------------+----------+
| entrée             | réponse  |
+====================+==========+
| DAC                | FN13     |
+--------------------+----------+
| ipod/usb façade    | FN17     |
+--------------------+----------+
| radio              | FN38     |
+--------------------+----------+
| NAS                | FN44     |
+--------------------+----------+
| favoris            | FN45     |
+--------------------+----------+
| spotify            | FN57     |
+--------------------+----------+
| entrée numérique 1 | FN59     |
+--------------------+----------+
| entrée numérique 2 | FN60     |
+--------------------+----------+
| ipod/usb arrière   | FN61     |
+--------------------+----------+

Lecteur de musique
~~~~~~~~~~~~~~~~~~

+-----------------------------+----------+
| ordre                       | commande |
+=============================+==========+
| play                        | 10PB\\r  |
+-----------------------------+----------+
| pause                       | 11PB\\r  |
+-----------------------------+----------+
| precedent                   | 12PB\\r  |
+-----------------------------+----------+
| suivant                     | 13PB\\r  |
+-----------------------------+----------+
| afficher l'écran de lecture | 18PB\\r  |
+-----------------------------+----------+
| stop                        | 20PB\\r  |
+-----------------------------+----------+
| entrer                      | 30PB\\r  |
+-----------------------------+----------+
| retour                      | 31PB\\r  |
+-----------------------------+----------+
| ajouter aux favoris         | 32PB\\r  |
+-----------------------------+----------+
| répéter                     | 34PB\\r  |
+-----------------------------+----------+
| mélanger                    | 35PB\\r  |
+-----------------------------+----------+


État de l'ecran
~~~~~~~~~~~~~~~

Pour connaitre les informations affiché a l'ecran, vous pouvez execture la commande suivante:

+--------+----------+
| ordre  | commande |
+========+==========+
| status | ?GAP\\r  |
+--------+----------+


Cette commande retourne la réponse suivante:

+-----------------------------------+-------------------------+
| type d'information                | réponse                 |
+===================================+=========================+
| informations d'en-tête d'écran    | GCPaabcdefghijkkklmm"n" |
+-----------------------------------+-------------------------+
| informations sur l'écran          | GDPaaaaabbbbbccccc      |
+-----------------------------------+-------------------------+
| informations sur la ligne d'écran | GEPaabcc"d"             |
+-----------------------------------+-------------------------+

Souvent la réponse contient plusieurs des valeurs contenu dans cette table.

Exemple d'écran sur une chanson jouée::

    'GBP08\r\nGCP02110100000110200""\r\nGDP000010000100001\r\nGEP01020"Milk"\r\nGEP02021"Garbage"\r\nGEP03022"Garbage"\r\nGEP04026"mp3"\r\nGEP05028""\r\nGEP06029"320kbps"\r\nGEP07023"0:23"\r\nGEP08034"3:52"\r\n'

Exemple lorsque l'écran affiche une liste de chansons::

    'GBP08\r\nGCP01110100000000200"Garbage"\r\nGDP000010000800012\r\nGEP01002"Supervixen"\r\nGEP02102"Queer"\r\nGEP03002"Only Happy When It Rains"\r\nGEP04002"As Heaven Is Wide"\r\nGEP05002"Not My Idea"\r\nGEP06002"A Stroke Of Luck"\r\nGEP07002"Vow"\r\nGEP08002"Stupid Girl"\r\n'


GBP
***

Première instruction renvoyée lorsque l'état de l'écran est requis, explique le nombre de GEP qui doivent être analysés.

+-----+----+
| GBP | aa |
+-----+----+

Chaque champ a la description suivante

+--------+--------------------------------------+
| champs | description                          |
+========+======================================+
| aa     | nombre de lignes affichées à l'écran |
+--------+--------------------------------------+

GCP
***

Cette réponse est envoyée pour décrire la vue

+-----+----+---+---+---+---+---+---+---+---+---+-----+---+----+-----+
| GCP | aa | b | c | d | e | f | g | h | i | j | kkk | l | mm | "n" |
+-----+----+---+---+---+---+---+---+---+---+---+-----+---+----+-----+

Exemple::

    GCP01110100000000200"Garbage"


Chaque champ a la description suivante

+--------+-------------------------+
| champs | description             |
+========+=========================+
| aa     | type d'écran            |
+--------+-------------------------+
| b      |                         |
+--------+-------------------------+
| c      | bouton top menu activé  |
+--------+-------------------------+
| d      |                         |
+--------+-------------------------+
| e      | bouton retour activé    |
+--------+-------------------------+
| f      |                         |
+--------+-------------------------+
| g      | mode mélangé activé     |
+--------+-------------------------+
| h      | mode répété activé      |
+--------+-------------------------+
| i      |                         |
+--------+-------------------------+
| j      |                         |
+--------+-------------------------+
| kkk    | type de la vue          |
+--------+-------------------------+
| l      | status de lecture       |
+--------+-------------------------+
| mm     |                         |
+--------+-------------------------+
| n      | titre                   |
+--------+-------------------------+


Le champ type d'écran peut avoir differentes valeurs decrite dans le tableau suivant:

+------+----------------------+
| code | description          |
+======+======================+
| 00   | erreur               |
+------+----------------------+
| 01   | liste                |
+------+----------------------+
| 02   | file info            |
+------+----------------------+
| 03   | file info with pause |
+------+----------------------+
| 06   | chargement           |
+------+----------------------+


La vue peut afficher different types d'informations.

+------+-------------------------------------------+
| code | description                               |
+======+===========================================+
| 000  | the view is a list                        |
+------+-------------------------------------------+
| 002  | the view display the root of music server |
+------+-------------------------------------------+
| 110  | the view display information of file      |
+------+-------------------------------------------+


Le champ lecture affiche l'etat de la lecture courante

+------+-------------+
| code | description |
+======+=============+
| 0    | stopé       |
+------+-------------+
| 1    | pause       |
+------+-------------+
| 2    | lecture     |
+------+-------------+


GDP
***

+-----+-------+-------+-------+
| GDP | aaaaa | bbbbb | ccccc |
+-----+-------+-------+-------+

Exemple::

    GDP000010000800012


+--------+--------------------------+
| champs | description              |
+========+==========================+
| aaaaa  | premiere ligne a l'ecran |
+--------+--------------------------+
| bbbbb  | derniere ligne a l'ecran |
+--------+--------------------------+
| ccccc  | nombre total de lignes   |
+--------+--------------------------+


GEP
***

+-----+----+---+----+-----+
| GEP | aa | b | cc | "d" |
+-----+----+---+----+-----+

Exemple::

    GEP01002"Supervixen"


+--------+-------------------+
| champs | description       |
+========+===================+
| aa     | nombre de lignes  |
+--------+-------------------+
| b      | ligne sélectionée |
+--------+-------------------+
| cc     |                   |
+--------+-------------------+
| "d"    | texte de la ligne |
+--------+-------------------+


Information sur l'image
~~~~~~~~~~~~~~~~~~~~~~~

Cette commande permet de connaite l'image affiché sur l'ecran du lecteur

+--------------------------+----------+
| ordre                    | commande |
+==========================+==========+
| obetnir l'url de l'image | ?GIC\\r  |
+--------------------------+----------+


réponse

+-----+-----+-----+
| GIC | aaa | "b" |
+-----+-----+-----+


+--------+-----------------+
| champs | description     |
+========+=================+
| aaa    | taille de l'url |
+--------+-----------------+
| b      | url de l'image  |
+--------+-----------------+


Information sur le répertoire
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Au lieu de lire a l'écran les informations du répertoire, vous pouvez demander directement les informations des répertoires et récupérer l'image associée.


+------------------------------------------------+-------------------+
| ordre                                          | commande          |
+================================================+===================+
| obtenir la liste des répertoires et les images | ?GIAaaaaabbbbb\\r |
+------------------------------------------------+-------------------+

+--------+--------------------------+
| champs | description              |
+========+==========================+
| aaaaa  | number of the first line |
+--------+--------------------------+
| bbbbb  | number of the last line  |
+--------+--------------------------+



réponse

+-----+-------+-------+-----+----+-----+-----+-----+
| GIB | aaaaa | bbbbb | ccc | dd | "e" | fff | "g" |
+-----+-------+-------+-----+----+-----+-----+-----+

Exemple::

    GIB000020000201016"Toute la musique"066"http://127.0.0.1:5000/transcoder/jpegtnscaler.cgi/ebdart/23320.jpg"

Chaque champ a la description suivante

+--------+-----------------------------------------------------+
| champs | description                                         |
+========+=====================================================+
| aaaaa  | nombre de lignes affichées a l'écran (entre 1 & 8 ) |
+--------+-----------------------------------------------------+
| bbbbb  | nombre de lignes                                    |
+--------+-----------------------------------------------------+
| ccc    |                                                     |
+--------+-----------------------------------------------------+
| dd     | nombre de caracteres dans le nom du répertoire      |
+--------+-----------------------------------------------------+
| e      | nom du répertoire                                   |
+--------+-----------------------------------------------------+
| fff    | nombre de caracteres dans l'url de l'image          |
+--------+-----------------------------------------------------+
| g      | url de l'image                                      |
+--------+-----------------------------------------------------+



Amplificateur
-------------


Alimentation
~~~~~~~~~~~~

L'alimentation de l'amplificateur est un petit peu differente decelle du lecteur réseau.
Il existe une unique commande pour démarrer ou arreter l'amplificateur.
Aussi il n'est pas possible de savoir le status de l'alimentation de l'amplificateur.

+------------+-----------------+
| ordre      | commande        |
+============+=================+
| Start/Stop | 0A51CFFFFROI\\r |
+------------+-----------------+


Volume
~~~~~~

+-------+-----------------+
| ordre | commande        |
+=======+=================+
| haut  | 0A50AFFFFROI\\r |
+-------+-----------------+
| bas   | 0A50BFFFFROI\\r |
+-------+-----------------+

Source
~~~~~~

+--------+-----------------+
| ordre  | commande        |
+========+=================+
| change | 0A555FFFFROI\\r |
+--------+-----------------+


Lecteur CD
----------

Alimentation
~~~~~~~~~~~~

Comme l'amplificateur le lecteur CD a une seule commande pour démarrer et arreter l'appareil sans retourn du status de l'alimentation.

+------------+--------------+
| ordre      | commande     |
+============+==============+
| Start/Stop | 0A21CFFFFROI |
+------------+--------------+


Piste
~~~~~

+-----------+--------------+
| ordre     | commande     |
+===========+==============+
| precedent | 0A211FFFFROI |
+-----------+--------------+
| lecture   | 0A217FFFFROI |
+-----------+--------------+
| suivant   | 0A210FFFFROI |
+-----------+--------------+
| stop      | 0A216FFFFROI |
+-----------+--------------+
| pause     | 0A218FFFFROI |
+-----------+--------------+
