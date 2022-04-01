import csv
import ipaddress


class CIDR:
    def open_file(self, file):
        with open(self.outfile, 'w') as o:
            writer = csv.writer(o)
            with open(file) as f:
                reader = csv.reader(f)
                if self.SKIP_HEADER:
                    next(reader, )
                for i in reader:
                    ip = self.process_ip(i[self.IP_LOC1], i[self.IP_LOC2])
                    if self.IP_LOC1 == 0 and self.IP_LOC2 == 1:
                        row = [ip] + i[2:]
                    elif self.IP_LOC1 == 0:
                        row = [ip] + i[1:self.IP_LOC2] + i[self.IP_LOC2+1:]
                    else:
                        row = i[:self.IP_LOC1] + i[self.IP_LOC2:]
                    writer.writerow(row)
            f.close()
        o.close()
        print('COMPLETE')

    def process_ip(self, ip1, ip2):
        ip1 = ipaddress.ip_address(int(ip1))
        ip2 = ipaddress.ip_address(int(ip2))
        data = [ipaddr for ipaddr in ipaddress.summarize_address_range(ip1, ip2)]
        # ip1 = ipaddress.ip_address(int(ip1))
        # ip2 = ipaddress.ip_address(int(ip2))
        # mask = self.mask_cal(self.bin_convert(ip1), self.bin_convert(ip2))
        # con_ip = str(ip1)+'/'+ str(mask)
        return data[0]

    def bin_convert(self, ip):
        bin_str = ''
        for i in str(ip).split('.'):
            bnr = bin(int(i)).replace('0b', '')
            x = bnr[::-1]
            while len(x) < 8:
                x += '0'
            bnr = x[::-1]
            bin_str += bnr
        return bin_str

    def mask_cal(self, ip1, ip2):
        count = 0
        for i in range(0, 32):
            if ip1[i] == ip2[i]:
                count += 1
            else:
                break
        return count

    def __init__(self):
        self.SKIP_HEADER = False
        self.IP_LOC1 = 0
        self.IP_LOC2 = 1
        self.outfile = 'processed.csv'
        self.open_file('IP-COUNTRY-REGION-CITY.CSV')


if __name__ == '__main__':
    CIDR()
