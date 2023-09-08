import csv
import ipaddress
import sys


class CIDR:
    def open_file(self, file):
        with open(self.outfile, 'w', newline='') as o:
            writer = csv.writer(o)
            with open(file) as f:
                reader = csv.reader(f)
                if self.SKIP_HEADER:
                    next(reader, )
                for i in reader:
                    ip_ranges = self.process_ip(i[0], i[1])
                    for ip_range in ip_ranges:
                        row = [str(ip_range)] + i[2:]
                        writer.writerow(row)
            f.close()
        o.close()
        print('COMPLETE')

    def process_ip(self, ip1, ip2):
        ip1 = ipaddress.ip_address(int(ip1))
        ip2 = ipaddress.ip_address(int(ip2))
        data = [ipaddr for ipaddr in ipaddress.summarize_address_range(ip1, ip2)]
        return data

    def __init__(self):
        self.SKIP_HEADER = False
        self.outfile = sys.argv[2]
        self.open_file(sys.argv[1])


if __name__ == '__main__':
    CIDR()
