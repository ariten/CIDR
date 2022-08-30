import csv
import ipaddress
import datetime
import os.path


class CIDR:
    def open_file(self, file):
        with open(file) as f:
            reader = csv.reader(f)
            if self.SKIP_HEADER:
                next(reader, )
            max_row = len(list(reader))
        f.close()
        cached_update = 0.0
        print('\r'+str(cached_update)+'%', end='', flush=True)
        with open(file) as f:
            reader = csv.reader(f)
            if self.SKIP_HEADER:
                next(reader, )
            count = 0
            for i in reader:
                if count >= max_row:
                    if i[self.IP_LOC1] != '0':
                        watchlist_ref = self.sub_list(i[self.IP_LOC1], i[self.IP_LOC2], i[2], i[3], i[4], i[5])
                        self.main_list(i[self.IP_LOC1], i[self.IP_LOC2], i[2], i[3], f'{self.split_file}{watchlist_ref}', last_row=True)
                else:
                    if i[self.IP_LOC1] != '0':
                        watchlist_ref = self.sub_list(i[self.IP_LOC1], i[self.IP_LOC2], i[2], i[3], i[4], i[5])
                        self.main_list(i[self.IP_LOC1], i[self.IP_LOC2], i[2], i[3], f'{self.split_file}{watchlist_ref}')

                count += 1
                cur_per = round((count/max_row)*100, 0)
                if cached_update < cur_per:
                    cached_update = cur_per
                    print('\r'+str(cached_update)+'%', end='', flush=True)

        f.close()
        print('\nCOMPLETE')

    def main_list(self, ip1, ip2, country_code, country, watchlist_ref, last_row=False):
        if self.last_ip == 0:
            self.last_ip = int(ip2)
            self.start_ip = int(ip1)
            self.buffer = [country_code, country, watchlist_ref]
        elif last_row:
            if self.buffer[0] != country_code or self.buffer[2] != watchlist_ref:
                self.create_main_row(self.start_ip, self.last_ip, self.buffer[0], self.buffer[1], self.buffer[2])
                self.create_main_row(int(ip1), int(ip2), country_code, country, watchlist_ref)
            else:
                self.create_main_row(self.start_ip, ip2, self.buffer[0], self.buffer[1], self.buffer[2])
        elif int(ip1) - self.last_ip == 1:
            if self.buffer[0] != country_code or self.buffer[2] != watchlist_ref:
                self.create_main_row(self.start_ip, self.last_ip, self.buffer[0], self.buffer[1], self.buffer[2])
                self.start_ip = int(ip1)
                self.last_ip = int(ip2)
                self.buffer = [country_code, country, watchlist_ref]
            else:
                self.last_ip = int(ip2)
        else:
            print(self.start_ip, self.last_ip, self.buffer)
            print(ip1, ip2, country_code, country)
            exit(-1)

    def sub_list(self, ip1, ip2, country_code, country, region, city, last_row=False):
        self.count += (len(ip1) + len(ip2) + len(country_code) + len(country) + len(region) + len(city))
        if self.count >= 450000000:
            self.watchlist_ref_counter += 1
            with open(f'{self.split_file}{self.watchlist_ref_counter}.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(self.sub_list_buffer)
            f.close()
            self.sub_list_buffer = []
            ip = self.process_ip(ip1, ip2)
            self.sub_list_buffer.append([ip, country_code, country, region, city])
            self.count = (len(ip1) + len(ip2) + len(country_code) + len(country) + len(region) + len(city))
        elif last_row:
            with open(f'{self.split_file}{self.watchlist_ref_counter}.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(self.sub_list_buffer)
            f.close()
            ip = self.process_ip(ip1, ip2)
            self.sub_list_buffer.append([ip, country_code, country, region, city])
        else:
            ip = self.process_ip(ip1, ip2)
            self.sub_list_buffer.append([ip, country_code, country, region, city])
            if len(self.sub_list_buffer) >= self.buffer_size:
                with open(f'{self.split_file}{self.watchlist_ref_counter}.csv', 'a+', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(self.sub_list_buffer)
                f.close()
                self.sub_list_buffer = []
        return self.watchlist_ref_counter

    def create_main_row(self, start_ip, last_ip, country_code, country, watchlist_ref):
        ip = self.process_ip(start_ip, last_ip)
        row = [str(ip), country_code, country, watchlist_ref]
        self.write_main_row(row)

    def write_main_row(self, row, last_row=False):
        if len(self.main_list_buffer) >= self.buffer_size or last_row:
            self.main_list_buffer.append(row)
            with open(self.outfile, 'a+', newline='') as o:
                writer = csv.writer(o)
                writer.writerows(self.main_list_buffer)
            o.close()
            self.main_list_buffer = []
        else:
            self.main_list_buffer.append(row)

    def process_ip(self, ip1, ip2):
        ip1 = ipaddress.ip_address(int(ip1))
        ip2 = ipaddress.ip_address(int(ip2))
        data = [ipaddr for ipaddr in ipaddress.summarize_address_range(ip1, ip2)]
        return data[0]

    def __init__(self):
        self.main_list_buffer = []
        self.sub_list_buffer = []
        self.SKIP_HEADER = False
        self.buffer_size = 5000
        self.IP_LOC1 = 0
        self.IP_LOC2 = 1
        self.last_ip = 0
        self.count = 0
        self.watchlist_ref_counter = 1
        self.start_ip = 0
        self.buffer = []
        self.outfile = 'OverseasMain.csv'
        self.split_file = 'OverseasLookup_'
        if os.path.exists(self.outfile):
            os.remove(self.outfile)
        for i in os.listdir():
            if i.startswith(self.split_file):
                os.remove(i)
        self.open_file('IP-COUNTRY-REGION-CITY.CSV')


if __name__ == '__main__':
    CIDR()
