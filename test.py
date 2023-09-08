import ipaddress

ip1 = "17430272"
ip2 = "17430783"


def process_ip(ip1, ip2):
    ip1 = ipaddress.ip_address(int(ip1))
    ip2 = ipaddress.ip_address(int(ip2))
    data = [ipaddr for ipaddr in ipaddress.summarize_address_range(ip1, ip2)]
    return data

ranges = process_ip(ip1, ip2)

for i in ranges:
    print(str(i))
