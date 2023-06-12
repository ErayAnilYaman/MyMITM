import scapy.all as scapy
import optparse


def get_user_input():

    parse_object = optparse.OptionParser()

    parse_object.add_option("-i","--ip_address",dest="ip_address",help="Enter the ip address");
    (ip_address_list,arguments) = parse_object.parse_args();
    if not ip_address_list:
        print("Wrong Ip");
    else:
        return ip_address_list;

def scan_network(ip_address_list):
    arp_request_packet = scapy.ARP(pdst=ip_address_list.ip_address)
    broadcast_request_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    combined_packet = broadcast_request_packet/arp_request_packet;

    (answered_list,unanswered_list) = scapy.srp(combined_packet,timeout=1)
    answered_list.summary();

scan_network(get_user_input())


