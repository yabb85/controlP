import socket
import re
import requests
from lxml import etree as ElementTree
from logging import debug

DISCOVER_TIMEOUT = 2
SSDP_TARGET = ("239.255.255.250", 1900)
SSDP_MX = DISCOVER_TIMEOUT
ST_ROOTDEVICE = "upnp:rootdevice"


def ssdp_request(ssdp_st, ssdp_mx=SSDP_MX):
    """
    Return request bytes for given st and mx.
    """
    return "\r\n".join(
        [
            "M-SEARCH * HTTP/1.1",
            "ST: {}".format(ssdp_st),
            "MX: {:d}".format(ssdp_mx),
            'MAN: "ssdp:discover"',
            "HOST: {}:{}".format(*SSDP_TARGET),
            "",
            "",
        ]
    ).encode("utf-8")


def ssdp_scan(req: str) -> set:
    """
    Return list of url for each upnp device
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(DISCOVER_TIMEOUT)
    sock.sendto(req, SSDP_TARGET)

    urls = set()
    try:
        while True:
            response, addr = sock.recvfrom(65507)
            locations = re.findall(
                r"LOCATION: *(?P<url>\S+)\s+", response.decode('utf-8'), re.IGNORECASE
            )
            if locations and len(locations) >0:
                urls.add(locations[0])
    except socket.timeout:
        sock.close()
    return urls


def ssdp_pioneer_device(urls: set) -> dict:
    """
    Request upnp device and return information only for pionner device.
    """
    devices = []
    for location in urls:
        # TODO: split pour pouvoir refresh seulement un appareil si besoin
        resp = requests.get(location, timeout=10, auth=None, headers=None)
        resp.raise_for_status()
        content = resp.content
        content_decoded = content.decode()
        content_decoded = content_decoded.replace('=" ', '="')  # fix issue on pioneer xml
        root = ElementTree.fromstring(content_decoded.encode())
        ns = root.nsmap
        for device in root.findall(f".//manufacturer[.='PIONEER CORPORATION']/..", ns):
            friendly_name = device.find(f'.//friendlyName', ns)
            model = device.find(f'.//modelName', ns)
            remote_ready = device.xpath("//*[local-name() = 'X_ipRemoteReady']")[0]
            remote_port = device.xpath("//*[local-name() = 'X_ipRemoteTcpPort']")[0]
            remote_ip = re.sub(r'http?://(\d+\.\d+\.\d+\.\d+).*', r'\1', location)
            devices.append({
                'friendly_name': friendly_name.text,
                'model': model.text,
                'remote_ready': remote_ready.text,
                'remote_port': int(remote_port.text),
                'remote_ip': remote_ip
            })
    return devices


def scan():
    req = ssdp_request(ST_ROOTDEVICE)
    urls = ssdp_scan(req)
    return ssdp_pioneer_device(urls)
