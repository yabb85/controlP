.. ControlP documentation master file, created by
   sphinx-quickstart on Mon Nov 11 22:54:12 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ControlP's documentation!
====================================

This project try to provide interface to command your N-50A network player.
It can also command your amplificator if cable "control" is plugged between your
amplificator and your network player.
It can run on Linux and Android, maybe on windows and macOS but not tested.
This project is reverse engineering of Pioneer protocol and it can be have some limitations.


Known issue:
    - latency on menu
    - slider on player view display only, it is not possible to move in music with slider.
    - album cover not correctly displayed in menu


Work in progress:
    - preload menu list in background to improve navigation


Todo:
    - add index to navigate by letter if list is too long


The most important part of this documentation is the explaination of the protocol



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   protocol



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
