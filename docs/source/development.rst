Development
===========


Generer le trousseau de clé
---------------------------


.. code::

    keytool -genkey -v -keystore ./keystores/controlP.keystore -alias controlP -keyalg RSA -keysize 2048 -validity 10000

    keytool -importkeystore -srckeystore ./keystores/controlP.keystore  -destkeystore ~/keystores/controlP.keystore -deststoretype pkcs12




Construire une version final
----------------------------

.. code::

    export P4A_RELEASE_KEYSTORE=./keystores/controlP.keystore
    export P4A_RELEASE_KEYSTORE_PASSWD=
    export P4A_RELEASE_KEYALIAS_PASSWD=
    export P4A_RELEASE_KEYALIAS=controlP

    buildozer -v android release
    jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ./keystores/controlP.keystore ./bin/controlP-0.1-arm64-v8a_armeabi-v7a-release-unsigned.apk controlP
