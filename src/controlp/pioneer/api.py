from logging import getLogger
from re import match as re_match
from socket import AF_INET, SOCK_STREAM, socket
from socket import timeout as exception_timeout
from threading import RLock
from time import sleep

"""
Module to communicate with Pioneer N-50A

All command are set by simple characters send by socket on port 8102

Power:
    ON: 'PO\r'
    OFF: 'PF\r'

Power status:
    Status: '?P\r'

    Response:
        PWR0: ON

Input Status:
    Status: '?F\r'

    Response
    FN13 = DAC
    FN17 = ipod/usb front
    FN38 = radio
    FN44 = NAS
    FN45 = favorite
    FN57 = spotify
    FN59 = digital input 1
    FN60 = digital input 2
    FN61 = ipod/usb rear

Commandes:
    10PB : play
    11PB : pause
    12PB : precedent
    13PB : suivant
    18PB : afficher lecture en cour
    20PB : stop
    30PB : entrer
    31PB : return -> response GID1
    32PB : ajoute au favori
    34PB : repeat
    35PB : shuffle


Cover image information
    Status: '?GIC\r'

    Response:
        GICaaa"b"
            aaa = ???,
            b = url of image


Dossier image information
    Status: '?GIAaaaaabbbbb' aaaaa = numero de la premiere ligne, bbbbb numero de la derniere ligne

    Example : '?GIA0000100009'

    Response:
        GIBaaaaabbbbbcccdd"e"fff"g"
            aaaaa = numero de ligne a l'ecran (entre 1 et 8),
            bbbbb = numero de ligne,
            dd = nombre de lettre dans le nom du dossier,
            e = nom du dossier
            fff = nombre de caractere de l'url,
            g = url du fichier image
        GIB000020000201016"Toute la musique"070"http://192.168.1.38:50002/transcoder/jpegtnscaler.cgi/ebdart/23320.jpg"


Screen information
    Status: '?GAP'

    Response:
        GCP
        GDP
        GEP
        GBP

    screen type:
        00 : error
        01 : list
        02 : file info
        03 : file info with pause
        06 : loading

    screen vue:
        000 : list
        110 : file view
        002 : music server root

    screen shuffle:
        0 : disabled
        1 : enabled

    screen repeat:
        0 : no repeat
        1 : one repeat
        2 : repeat

    screen play:
        0 : stopped
        1 : pause
        2 : play


Amplifier command:

Power:
    Start/Stop ampli: '0A51CFFFFROI'

Volume:
    UP: '0A50AFFFFROI'
    DOWN: '0A50BFFFFROI'

Source:
    change: '0A555FFFFROI'

Volume Status:
    Maybe work on integrated amplifier but not on N-50A
    Status: '?VOL\r'

    Response:
        VOL40


CD player command:

Power:
    Start/Strop cd player : 0A21CFFFFROI

Track:
    Previous: 0A211FFFFROI
    Play : 0A217FFFFROI
    Next : 0A210FFFFROI
    Stop : 0A216FFFFROI
    Pause : 0A218FFFFROI

"""

LOGGER = getLogger(__name__)
log_debug = LOGGER.debug


class Pioneer(object):
    """
    Class used to send order at pioneer network player
    """

    def __init__(self, ip, port):
        super(Pioneer, self).__init__()
        self.ip = ip
        self.port = port
        self.socket = False
        self._connect()
        self.locker = RLock()
        self.power = False

    def close(self):
        """
        Close connection
        """
        if self.socket:
            self.socket.close()

    def _connect(self):
        """
        open e new socket to send command and receive status
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        # self.socket.setblocking(False)
        self.socket.connect((self.ip, self.port))

    def _send_command(self, command: str, rep_flag=True):
        """
        Send command on opened socket
        """
        # log_debug('_send_command')
        with self.locker:
            response = None
            formatted = u'{command}\r'.format(command=command)
            # log_debug(f'formatted command: {formatted}')
            try:
                self.socket.send(formatted.encode('utf-8'))
                if rep_flag:
                    response = self._read()
            except BrokenPipeError as err:
                self.close()
                self._connect()
                self.power_status()
            return response

    def _read(self, timeout=None, exception=False):
        """
        read status returned by player
        """
        # log_debug('_read')
        response = None
        with self.locker:
            save_timeout = self.socket.gettimeout()
            if timeout:
                self.socket.settimeout(timeout)
            try:
                response = self.socket.recv(99999999)
                response = response.decode('utf-8')
                # log_debug('_read: response: {}'.format(response))
                # log_debug(f'_read: reponse size: {len(response)}')
            except exception_timeout as socket_timeout:
                if exception:
                    raise
            finally:
                self.socket.settimeout(save_timeout)
            return response

    def _clean_buffer(self, timeout=0.3):
        """
        clean socket buffer to remove old status
        """
        with self.locker:
            self.socket.settimeout(timeout)
            try:
                while True:
                    self._read(exception=True)
            except exception_timeout as socket_timeout:
                pass
            finally:
                self.socket.settimeout(None)

    def power_on(self):
        """
        Start player
        """
        if self.power_status() == 'PWR2':
            self._send_command('PO', False)
            self.power= True
            self._clean_buffer(1)

    def power_off(self):
        """
        Stop player
        """
        self._send_command('PF', False)
        self.power = False

    def power_status(self):
        """
        Status of power player
        """
        response = self._send_command('?P')
        response = response.strip()
        self.power = response == 'PWR0'
        return response

    def volume_status(self):
        """
        Read the volume status of Hi-Fi
        TODO : not work
        """
        response = self._send_command('?V')
        return response.strip()

    def input_status(self):
        """
        Return code of current input selected by network player
        """
        response = self._send_command('?F')
        try:
            return int(response[2:])
        except:
            return self.input_status()

    def input_status_pretty(self):
        """
        Return name of current input selected by network player
        """
        response = self._send_command('?F')
        status = ''
        if 'FN13' in response:
            status = 'DAC'
        elif 'FN17' in response:
            status = 'ipod/usb front'
        elif 'FN38' in response:
            status = 'radio'
        elif 'FN44' in response:
            status = 'NAS'
        elif 'FN45' in response:
            status = 'favorite'
        elif 'FN57' in response:
            status = 'spotify'
        elif 'FN59' in response:
            status = 'digital input 1'
        elif 'FN60' in response:
            status = 'digital input 2'
        elif 'FN61' in response:
            status = 'ipod/usb rear'
        return status

    def screen_status(self):
        """
        """
        if not self.power:
            return
        self._clean_buffer()
        response = self._send_command('?GAP')
        result = self.parse_menu_response(response)
        while 'nb_lines' not in result or 'lines' not in result or len(result['lines']) < result['nb_lines']:
            sleep(0.1)
            response += self._read()
            result.update(self.parse_menu_response(response))
        return result

    def img_status(self):
        """
        Return url of image displayed on network player screen
        """
        if not self.power:
            return
        response = self._send_command('?GIC')
        return self.parse_image_response(response)

    def directory_status(self, begin: int, size: int):
        if not self.power:
            return
        response = self._send_command('?GIA{:05d}{:05d}'.format(begin,begin + size - 1))
        status = self.parse_directory_response(response)
        while len(status) < size:
            sleep(0.1)
            response = self._read()
            status.update(self.parse_directory_response(response))
        return status

    def parse_menu_response(self, response: str):
        """
        Read response and extract all informations, number of lines and information of each lines
        """
        result = {}
        string = response.split('\r\n')
        gbp_pattern = r'GBP(?P<nb_lines>..)'
        gcp_pattern = r'GCP(?P<type>..)(?P<view>.)(?P<top>.)(?P<unknown1>.)(?P<return>.)(?P<unknown2>.)(?P<shuffle>.)(?P<repeat>.)(?P<unknown3>.)(?P<unknown4>.)(?P<vue>...)(?P<play>.)(?P<unknown5>..)"(?P<title>.*)"'
        gdp_pattern = (
            r'GDP(?P<begin_disp>.....)(?P<end_disp>.....)(?P<total_line>.....)'
        )
        gep_pattern = r'GEP(?P<number>..)(?P<highlight>.)(?P<tag>..)"(?P<value>.*)"'
        for line in string:
            match = re_match(gbp_pattern, line)
            if match:
                status = match.groupdict()
                status['nb_lines'] = int(status['nb_lines'])
                result.update(status)
                continue
            match = re_match(gcp_pattern, line)
            if match:
                status = match.groupdict()
                status['shuffle'] = int(status['shuffle'])
                status['repeat'] = int(status['repeat'])
                status['play'] = int(status['play'])
                result.update(status)
            match = re_match(gdp_pattern, line)
            if match:
                status = match.groupdict()
                status['begin_disp'] = int(status['begin_disp'])
                status['end_disp'] = int(status['end_disp'])
                status['total_line'] = int(status['total_line'])
                result.update(status)
            match = re_match(gep_pattern, line)
            if match:
                status = match.groupdict()
                # result.update(status)
                result.setdefault('lines', {})
                status['number'] = int(status['number'])
                result['lines'][status['number']] = status
        return result

    def parse_image_response(self, response: str):
        """
        Extract url on message return by network player for image displayed
        """
        result = {}
        lines = response.split('\r\n')
        gic_pattern = r'GIC(?P<url_size>...)"(?P<url>.*)"'
        for line in lines:
            match = re_match(gic_pattern, line)
            if match:
                status = match.groupdict()
                result.update(status)
        return result

    def parse_directory_response(self, response: str):
        """
        """
        result = {}
        lines = response.split('\r\n')
        gib_pattern = r'GIB(?P<begin_disp>\d{5})(?P<begin_line>\d{5})...(?P<size_value>\d{2})"(?P<value>.*)"(?P<size_url>\d{3})"(?P<url>.*)"'
        for line in lines:
            match = re_match(gib_pattern, line)
            if match:
                status = match.groupdict()
                status['begin_disp'] = int(status['begin_disp'])
                status['begin_line'] = int(status['begin_line'])
                status['size_value'] = int(status['size_value'])
                status['size_url'] = int(status['size_url'])
                result[status['begin_disp']] = status
        return result

    def play(self):
        """
        Play track
        """
        self._send_command('10PB')

    def pause(self):
        """
        Pause current track played
        """
        self._send_command('11PB')

    def previous(self):
        """
        Play previous track
        """
        self._send_command('12PB')

    def next(self):
        """
        Play next track
        """
        self._send_command('13PB')

    def current_play(self):
        """
        Go screen to current playing
        """
        self._send_command('18PB')

    def stop(self):
        """
        Stop play
        """
        self._send_command('20PB')

    def enter(self):
        """
        Select OK for current item selected
        """
        self._send_command('30PB')

    def ret(self):
        """
        Return to previous menu
        """
        self._send_command('31PB')

    def repeat(self):
        """
        Repeat track/album
        """
        self._send_command('34PB')

    def shuffle(self):
        """
        Suffle playing order
        """
        self._send_command('35PB')

    def select_line(self, nb: int):
        """
        select a line in menu to highlight
        """
        self._send_command('{:05d}GGP'.format(nb), False)

    def set_line(self, nb: int):
        """
        set the line to be opened to continue exploration
        """
        self._send_command('{:05d}GHP'.format(nb))

    def set_input(self, input: int):
        """
        """
        self._send_command('{0}FN'.format(input))

    # amplifier section
    def ampli_power(self):
        """
        if the network player is connected to amplificator
        this command can power on/off the amplificator
        """
        self._send_command('0A51CFFFFROI', False)

    def volume_down(self):
        """
        If amplifier is linked with network player reduce volume
        """
        self._send_command('0A50BFFFFROI', False)

    def volume_up(self):
        """
        If amplifier is linked with network player up volume
        """
        self._send_command('0A50AFFFFROI', False)

    def next_source(self):
        """
        Change current source on amplifier
        """
        self._send_command('0A555FFFFROI', False)

    #cd player section
    def cd_player_power(self):
        """
        if the network player is connected to amplificator
        this command can power on/off the cd player
        """
        self.send_command('0A21CFFFFROI')

    def cd_player_previous(self):
        """
        Play previous track on cd player
        """
        self.send_command('0A211FFFFROI')

    def cd_player_play(self):
        """
        Play music on cd player
        """
        self.send_command('0A217FFFFROI')

    def cd_player_next(self):
        """
        Play next track on cd player
        """
        self.send_command('0A210FFFFROI')

    def cd_player_stop(self):
        """
        Stop music on cd player
        """
        self.send_command('0A216FFFFROI')

    def cd_player_pause(self):
        """
        Pause current track on cd player
        """
        self.send_command('0A218FFFFROI')


def main():
    """docstring for main"""
    # create pioneer connection
    pioneer = Pioneer('192.168.1.100', 8102)
    pioneer.power_on()
    pioneer.power_status()
    pioneer.volume_status()
    pioneer.input_status()
    pioneer.screen_status()
    pioneer.img_status()

    pioneer.close()
    # XXXXXGHP definie la ligne selectionner dans le menu
    # 00002GHP -> selectionne la deuxieme ligne dans le menu

    # socket.send(u'?RGB44\r\n')
    # socket.send(u'?RGD\r')
    # socket.send(u'?RGF\r')


if __name__ == '__main__':
    main()
