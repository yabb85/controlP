This software is a Gtk UI to command pioneer N-50A network player.

# Information

This code is a reverse engineering of pioneer protocol analyzed with wireshark.
Some commands are missing but the original android player is down and is not possible to analyze protocol again.
It is possible to command basicaly the player and power on/off an amplificator connected on player with input control link.

# Installation

```bash
git clone https://github.com/yabb85/controlP.git

cd controlP

python -m controlP.client
```

