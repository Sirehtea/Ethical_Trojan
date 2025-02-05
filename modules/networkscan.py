import asyncio
import threading
from scapy.all import *
import socket
import subprocess, platform
import ipinfo
import requests
import os
import logging

def get_uuid():
    with open("uuid.txt", "r") as file:
        return file.read().strip()

def get_log_dir():
    uuid = get_uuid()
    log_dir = os.path.join("data", uuid, "network_scan_results")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

log_dir = get_log_dir()
log_path = os.path.join(log_dir, "network_scan_results.log")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', filename=log_path, filemode='a')

def list_ip_and_mac():
    logging.info("Available devices in the network:")
    logging.info("IP" + " "*18 + "MAC")
    for client in scan_range(scan_range_ip):
        logging.info("{:16}    {}".format(client['ip'], client['mac']))

def list_pinged_devices():
    responsive_ips = ping_devices(scan_range_ip)
    logging.info("----------------------- UP HOSTS ----------------------------")
    for ip in responsive_ips:
        logging.info(f"The host {ip} is up")
        logging.info("----------------------------------------------------------------------------------")

def scan_open_ports():
    for port in range(min, max + 1):
        try:
            serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv.bind((target, port))
        except:
            logging.info(f'[OPEN] Port open : {port}')
        serv.close()

def scan_common_open_ports():
    common_ports = [
        21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 587, 993, 995, 1433, 3306, 3389, 8080
    ]
    logging.info(f"Open ports of: {target}")
    for port in common_ports:
        try:
            serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv.bind((target, port))
        except:
            logging.info(f'[OPEN] Port open :{port}')
        serv.close()

def OS_detection():
    ttl_to_os = {
        128: "Windows",
        64: "Linux/FreeBSD/OSX/Juniper/HP-UX",
        255: "Cisco Devices",
        254: "Solaris/AIX",
        252: "Windows Server 2003/XP",
        240: "Novell",
        200: "HP-UX",
        190: "MacOS",
        127: "MacOS (Alternate)",
        100: "IBM OS/2",
        60: "AIX",
        50: "Windows 95/98/ME",
        48: "BSDI",
        30: "SunOS",
    }
    
    for ip in ping_devices(scan_range_ip):
        icmp = IP(dst=ip)/ICMP()
        resp = sr1(icmp, timeout=10)

        ttl = resp.ttl
        if ttl in ttl_to_os:
            logging.info(f"OS van {ip} = {ttl_to_os[ttl]}")
        else:
            logging.info(f"unknown OS")

def list_wifi_networks():
    command = "netsh wlan show networks"
    output = subprocess.check_output(command, shell=True, text=True)
    logging.info(output)

def get_public_ip():
    response = requests.get("https://ipinfo.io/ip")
    external_ip = response.text.strip()
    logging.info(external_ip)
    return external_ip

def geolocate_ip():
    access_token = "03a936abd67152"  # access token (is geen leak)
    ip = get_public_ip()
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip)
    for key, value in details.all.items():
        logging.info(f"{key} : {value}")

def scan_range(target_ip):
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    clients = [{'ip': received.psrc, 'mac': received.hwsrc} for sent, received in result]
    return clients

def ping_devices(range_ip):
    responsive_ips = []
    for client in scan_range(scan_range_ip):
        ip = client['ip']
        icmp = IP(dst=ip)/ICMP()
        resp = sr1(icmp, timeout=10)
        if resp:
            responsive_ips.append(ip)
    return responsive_ips

def start_function_in_thread(function):
    def wrapper():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        function()

    thread = threading.Thread(target=wrapper)
    thread.start()
    return thread
