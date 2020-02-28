import socket
from netaddr import IPNetwork
import sys
import subprocess
from scapy.all import *

port_list = open('/etc/services')
port_list.readline()
port_list.readline()

port_details = {}

for port_info in port_list.readlines():

    filtered = port_info.split()
    port_number = filtered[1].split('/')[0]
    protocol = filtered[1].split('/')[1]

    port_details[port_number] = (filtered[0], protocol)


def check_host(HOST):

    try:
        host_up = subprocess.check_output(["ping", "-c", "1", HOST])
        return True

    except:
        return False


# https://github.com/cptpugwash/Scapy-port-scanner/blob/master/port_scanner.py
def udp_scan(HOST, port):
    soc = sr1(IP(dst=HOST)/UDP(sport=port, dport=port), timeout=2, verbose=0)
    if soc == None:
        if str(port) in port_details:
            port_name = port_details[str(port)][0]
            print(f'Port {port}({port_name}): is open')
        else:
            print(f'Port {port} : is open')

    else:
        if soc.haslayer(ICMP):
            pass
        elif soc.haslayer(UDP):
            if str(port) in port_details:
                port_name = port_details[str(port)][0]
                print(f'Port {port}({port_name}): is open')
            else:
                print(f'Port {port} : is open')

        else:
            pass


def tcp_scan(HOST, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # soc.settimeout(1)

    dest = (HOST, int(port))

    test = soc.connect_ex(dest)
    if test == 0:
        if str(port) in port_details:
            port_name = port_details[str(port)][0]
            print(f'Port {port}({port_name}): is open')
        else:
            print(f'Port {port} : is open')

    soc.close()


def port_scan(HOST, PORT, protocol):

    range_check = ":" in PORT

    if range_check:
        ports = [int(x) for x in PORT.split(':')]
        for port in range(ports[0], ports[1]):
            if protocol == 0:
                tcp_scan(HOST, port)

            else:
                udp_scan(HOST, port)
    else:
        if protocol == 0:
            tcp_scan(HOST, PORT)

        else:
            udp_scan(HOST, PORT)


def scan_host(HOST, PORT, protocol=0):

    sep_str = '-' * 50

    mult_host = '/' in HOST

    if mult_host:
        for ip in IPNetwork(HOST)[1:]:
            if check_host(str(ip)):
                print(f'{sep_str}\n Scanning host {ip}\n{sep_str}\n')
                port_scan(str(ip), PORT, protocol)
                print(f'\n{sep_str}\n')
            else:
                pass
                # print(f'{sep_str}\n {ip} is down\n{sep_str}\n')
                # print(f'\n{sep_str}\n')

    else:

        print(f'{sep_str}\n Scanning host {HOST}\n{sep_str}\n')

        port_scan(HOST, PORT, protocol)

    print(f'\n{sep_str}\nScan process has finished\n{sep_str}')


# host = '192.168.50.235'
# host = '192.168.50.0/24'
# port = '1:100'
# scan_host(host, port, 'udp')
