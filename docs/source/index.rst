.. ControlP documentation master file, created by
   sphinx-quickstart on Mon Nov 11 22:54:12 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bienvenue dans la documentation de ControlP !
=============================================

Ce projet tente de fournir une interface pour commander votre lecteur réseau N-50A.
Il peut également commander votre amplificateur si un câble "contrôle" est branché entre
votre amplificateur et votre lecteur réseau.
Il peut fonctionner sous Linux et Android, peut-être sous Windows et macOS mais pas encore testé.
Ce projet est une rétro-ingénierie du protocole Pioneer et il peut avoir certaines limitations.

Problemes connues:
    - latence dans les menus
    - curseur sur l'affichage de la vue en lecture uniquement, il n'est pas possible de se déplacer dans la musique avec le curseur.
    - la couverture de l'album n'est pas correctement affichée dans le menu


Travail en cours:
    - précharger les menus en arriere plan pour améliorer la navigation.


À faire:
    - ajouter un index pour naviguer par lettre si la liste est trop longue


La partie la plus importante de cette documentation est l'explication du protocole



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   protocol
   development
