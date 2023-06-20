import sys
import os
from ipwhois import IPWhois
from prettytable import PrettyTable


# Функция получения ip-адреса при помощи утилиты tracert
def get_ip(name):
    result = os.popen(f"tracert {name}").read()
    list_ip = list()
    for i in result.split('\n'):
        if 'ms' in i:
            list_ip.append(i.split()[-1].strip('[]'))
    return list_ip


# Функция получения информации об ip-адресах
def get_inf(ip):
    if ip.startswith('192.168.') or ip.startswith('10.') or (
            ip.startswith('172.') and 15 < int(ip.split('.')[1]) < 32):
        return ip, '-', '-', '-'
    try:
        ipwhois_data = IPWhois(ip).lookup_rdap()
        return ip, ipwhois_data['asn'], ipwhois_data['asn_country_code'], ipwhois_data['network']['name']
    except:
        return ip, '', '', ''


# Функция создания нужной таблицы с информацией об ip-адресах
def result_table(ipp):
    table = PrettyTable(["№", "IP", "AS Name", "Country", "Provider"])
    for i, ip in enumerate(ipp):
        inf = get_inf(ip)
        table.add_row([i, *inf])
    return table


# Функция запуска программы в терминале
def main():
    if len(sys.argv) == 2:
        ip = get_ip(sys.argv[1])
        print(result_table(ip))


if __name__ == '__main__':
    main()
