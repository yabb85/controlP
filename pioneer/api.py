from re import match as re_match
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import timeout as exception_timeout
from time import sleep
"""
Module to communicate with Pioneer N-50A

All command are set by simple characters send by socket on port 8102

Power:
    ON: 'PO\r'
    OFF: 'PF\r'
    Start/Stop ampli: '0A51CFFFFROI'

Power status:
    Status: '?P\r'

    Response:
        PWR0: ON


Volume:
    UP: '0A50AFFFFROI'
    DOWN: '0A50BFFFFROI'

Volume Status:
    Status: '?VOL\r'

    Response:
        VOL40

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

Image information
    Status: '?GIC\r'

    Response:
        GICaaa"b" : aaa = ???, b = url of image

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

screen type:
    00 : error
    01 : list
    02 : file info
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
"""


class Pioneer(object):
    """
    """
    def __init__(self, ip, port):
        super(Pioneer, self).__init__()
        self.ip = ip
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        # self.socket.setblocking(False)
        self.socket.connect((self.ip, self.port))

    def close(self):
        """
        Close connection
        """
        self.socket.close()

    def send_command(self, command, rep_flag=True):
        """docstring for send_command"""
        formatted = u'{command}\r'.format(command=command)
        self.socket.send(formatted.encode('utf-8'))
        response = None
        if rep_flag:
            response = self.read()
        return response

    def read(self):
        """
        """
        response = self.socket.recv(99999999)
        return response.decode('utf-8')

    def clean_buffer(self):
        self.socket.settimeout(0.5)
        try:
            while True:
                self.read()
        except exception_timeout as socket_timeout:
            pass
        finally:
            self.socket.settimeout(None)

    def power_on(self):
        """
        Start player
        """
        if self.power_status() == 'PWR2':
            self.send_command('PO')

    def power_off(self):
        """
        Stop player
        """
        self.send_command('PF')

    def ampli_power(self):
        """
        """
        self.send_command('0A51CFFFFROI')

    def power_status(self):
        """
        Status of power player
        """
        response = self.send_command('?P')
        return response.strip()

    def volume_status(self):
        """
        Read the volume status of Hi-Fi
        """
        response = self.send_command('?V')
        return response.strip()

    def input_status(self):
        """
        Return name of current input selected by network player
        """
        response = self.send_command('?F')
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
        self.clean_buffer()
        response = self.send_command('?GAP')
        # if 'GBP08\r\n' == response or 'GBP02\r\n' == response or 'GBP03\r\n' == response:
            # response += self.read()
        if re_match('^GBP0.\r\n$', response):
            sleep(0.1)
            response += self.read()
        result = self.parse_menu_response(response)
        return result

    def img_status(self):
        """
        """
        response = self.send_command('?GIC')
        return self.parse_menu_response(response)

    def parse_menu_response(self, response):
        """
        """
        result = {}
        string = response.split('\r\n')
        gdc_pattern = r'GCP(?P<type>..)(?P<view>.)(?P<top>.)(?P<unknown1>.)(?P<return>.)(?P<unknown2>.)(?P<shuffle>.)(?P<repeat>.)(?P<unknown3>.)(?P<unknown4>.)(?P<vue>...)(?P<play>.)(?P<unknown5>..)"(?P<title>.*)"'
        gdp_pattern = r'GDP(?P<begin_disp>.....)(?P<end_disp>.....)(?P<total_line>.....)'
        gep_pattern = r'GEP(?P<number>..)(?P<highlight>.)(?P<tag>..)"(?P<value>.*)"'
        gic_pattern = r'GIC(?P<img>...)"(?P<url>.*)"'
        for line in string:
            match = re_match(gdc_pattern, line)
            if match:
                status = match.groupdict()
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
                result['lines'][status['number']] = status
            match = re_match(gic_pattern, line)
            if match:
                status = match.groupdict()
                result.update(status)
        return result

    def play(self):
        """
        """
        self.send_command('10PB')

    def pause(self):
        """
        """
        self.send_command('11PB')

    def previous(self):
        self.send_command('12PB')

    def next(self):
        self.send_command('13PB')

    def stop(self):
        self.send_command('20PB')

    def enter(self):
        """
        """
        self.send_command('30PB')

    def ret(self):
        self.send_command('31PB')

    def shuffle(self):
        self.send_command('35PB')

    def volume_down(self):
        self.send_command('0A50BFFFFROI')

    def volume_up(self):
        self.send_command('0A50AFFFFROI')

    def select_line(self, nb):
        """
        """
        self.send_command('{:05d}GGP'.format(nb))

    def set_line(self, nb):
        """
        """
        self.send_command('{:05d}GHP'.format(nb))

    def set_input(self, input):
        """
        """
        self.send_command('{0}FN'.format(input))


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
