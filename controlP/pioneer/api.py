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
    20PB : stop
    30PB : entrer
    31PB : return
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
            g²= url du ficheir image
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


Amplificator command:

Power:
    Start/Stop ampli: '0A51CFFFFROI'

Volume:
    UP: '0A50AFFFFROI'
    DOWN: '0A50BFFFFROI'

Source:
    change: '0A555FFFFROI'

Volume Status:
    Status: '?VOL\r'

    Response:
        VOL40


"""

LOGGER = getLogger(__name__)


class Pioneer(object):
    """
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
        self.socket = socket(AF_INET, SOCK_STREAM)
        # self.socket.setblocking(False)
        self.socket.connect((self.ip, self.port))

    def _send_command(self, command, rep_flag=True):
        """docstring for send_command"""
        with self.locker:
            formatted = u'{command}\r'.format(command=command)
            LOGGER.debug('formatted command: {}'.format(formatted))
            try:
                self.socket.send(formatted.encode('utf-8'))
            except BrokenPipeError as err:
                self.close()
                self._connect()
                self.power_status()
            response = None
            if rep_flag:
                response = self._read()
                LOGGER.debug('response: {}'.format(response))
            return response

    def _read(self):
        """
        """
        with self.locker:
            response = self.socket.recv(99999999)
            return response.decode('utf-8')

    def _clean_buffer(self):
        with self.locker:
            self.socket.settimeout(0.3)
            try:
                while True:
                    self._read()
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

    def power_off(self):
        """
        Stop player
        """
        self._send_command('PF', False)
        self.power = False

    def ampli_power(self):
        """
        """
        self._send_command('0A51CFFFFROI', False)

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
        """
        response = self._send_command('?V')
        return response.strip()

    def input_status(self):
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
        LOGGER.debug('Power state : {0}'.format(self.power))
        if not self.power:
            return
        self._clean_buffer()
        response = self._send_command('?GAP')
        # if 'GBP08\r\n' == response or 'GBP02\r\n' == response or 'GBP03\r\n' == response:
        # response += self.read()
        if re_match('^GBP0.\r\n$', response):
            sleep(0.1)
            response += self._read()
        result = self.parse_menu_response(response)
        return result

    def img_status(self):
        """
        """
        if not self.power:
            return
        response = self._send_command('?GIC')
        return self.parse_image_response(response)

    def directory_status(self, begin, size):
        if not self.power:
            return
        response = self._send_command('?GIA{:05d}{:05d}'.format(begin,begin + size))
        return self.parse_directory_response(response)

    def parse_menu_response(self, response):
        """
        """
        result = {}
        string = response.split('\r\n')
        gcp_pattern = r'GCP(?P<type>..)(?P<view>.)(?P<top>.)(?P<unknown1>.)(?P<return>.)(?P<unknown2>.)(?P<shuffle>.)(?P<repeat>.)(?P<unknown3>.)(?P<unknown4>.)(?P<vue>...)(?P<play>.)(?P<unknown5>..)"(?P<title>.*)"'
        gdp_pattern = (
            r'GDP(?P<begin_disp>.....)(?P<end_disp>.....)(?P<total_line>.....)'
        )
        gep_pattern = r'GEP(?P<number>..)(?P<highlight>.)(?P<tag>..)"(?P<value>.*)"'
        for line in string:
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
                result.update(status)
            match = re_match(gep_pattern, line)
            if match:
                status = match.groupdict()
                # result.update(status)
                result.setdefault('lines', {})
                result['lines'][int(status['number'])] = status
        return result

    def parse_image_response(self, response):
        result = {}
        lines = response.split('\r\n')
        gic_pattern = r'GIC(?P<url_size>...)"(?P<url>.*)"'
        for line in lines:
            match = re_match(gic_pattern, line)
            if match:
                status = match.groupdict()
                result.update(status)
        return result

    def parse_directory_response(self, response):
        result = {}
        lines = response.split('\r\n')
        gib_pattern = r'GIB(?P<begin_disp>\d{5})(?P<begin_line>\d{5})...(?P<size_name>\d{2})"(?P<name>.*)"(?P<size_url>\d{3})"(?P<url>.*)"'
        for line in lines:
            match = re_match(gib_pattern, line)
            if match:
                status = match.groupdict()
                status['begin_disp'] = int(status['begin_disp'])
                status['begin_line'] = int(status['begin_line'])
                status['size_name'] = int(status['size_name'])
                status['size_url'] = int(status['size_url'])
                result[status['begin_disp']] = status
        return result

    def play(self):
        """
        """
        self._send_command('10PB')

    def pause(self):
        """
        """
        self._send_command('11PB')

    def previous(self):
        self._send_command('12PB')

    def next(self):
        self._send_command('13PB')

    def stop(self):
        self._send_command('20PB')

    def enter(self):
        """
        """
        self._send_command('30PB')

    def ret(self):
        self._send_command('31PB')

    def repeat(self):
        self._send_command('34PB')

    def shuffle(self):
        self._send_command('35PB')

    def volume_down(self):
        self._send_command('0A50BFFFFROI', False)

    def volume_up(self):
        self._send_command('0A50AFFFFROI', False)

    def next_source(self):
        self._send_command('0A555FFFFROI', False)

    def select_line(self, nb):
        """
        """
        self._send_command('{:05d}GGP'.format(nb))

    def set_line(self, nb):
        """
        """
        self._send_command('{:05d}GHP'.format(nb))

    def set_input(self, input):
        """
        """
        self._send_command('{0}FN'.format(input))


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
