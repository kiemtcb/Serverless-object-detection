import os
import time
import csv
import sys


def TC(namefile, nic, delay, jitter, burst):
    os.system(f'sudo tc qdisc del dev {nic} root')
    while True:
        with open(namefile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if namefile == "wifi.csv":
                    DL_bitrate = 150
                else:
                    DL_bitrate = float(row[12])/1000
                if line_count == 0:
                    os.system(
                        f'sudo tc qdisc add dev {nic} root handle 1: netem delay {delay}ms {jitter}ms distribution normal')
                    os.system(
                        f'sudo tc qdisc add dev {nic} parent 1: handle 2: tbf rate {DL_bitrate}mbit burst {burst}Kb lat 1ms')
                    os.system(f'sudo tc qdisc show dev {nic}')
                    line_count += 1
                    time.sleep(1)
                    continue

                os.system(
                    f'sudo tc qdisc change dev eth0 parent 1: handle 2: tbf rate {DL_bitrate}mbit burst {burst}Kb lat 1ms')
                os.system(f'sudo tc qdisc show dev {nic}')
                time.sleep(3)


if __name__ == "__main__":

    network = str(sys.argv[1])
    interface = "eth0"
    delay = 0
    jitter = 0
    burst = 0
    filename = ''
    match network:
        case "4G":
            delay = 15
            jitter = 4
            burst = 125
            filename = "4G.csv"
        case "3G":
            delay = 25
            jitter = 10
            burst = 30
            filename = "3G.csv"
        case "wifi":
            delay = 5
            jitter = 0
            burst = 3500
            filename = "wifi.csv"
    print(filename, delay, jitter)
    TC(filename, interface, str(delay), str(jitter), str(burst))
