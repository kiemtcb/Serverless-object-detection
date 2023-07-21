import os
import time
import csv
import sys

# sudo tc qdisc add dev eth2 root handle 1: tbf rate 2mbit burst 30Kb lat 1ms


def TC(namefile, rootInterface, firstInterface, secondInterface, delay, jitter, burst):
    os.system(f'sudo tc qdisc del dev {rootInterface} root')
    os.system(f'sudo tc qdisc del dev {firstInterface} root')
    os.system(f'sudo tc qdisc del dev {secondInterface} root')
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
                        f'sudo tc qdisc add dev {rootInterface} root handle 1: netem delay {delay}ms {jitter}ms distribution normal')
                    os.system(
                        f'sudo tc qdisc add dev {rootInterface} parent 1: handle 2: tbf rate {DL_bitrate}mbit burst {burst}Kb lat 1ms')
                    os.system(
                        f'sudo tc qdisc add dev {firstInterface} root handle 1: tbf rate {DL_bitrate}mbit burst {burst}Kb lat 1ms')
                    os.system(
                        f'sudo tc qdisc add dev {secondInterface} root handle 1: tbf rate {DL_bitrate}mbit burst {burst}Kb lat 1ms')
                    os.system(f'sudo tc qdisc show dev {rootInterface}')
                    line_count += 1
                    time.sleep(1)
                    continue

                os.system(
                    f'sudo tc qdisc change dev {rootInterface} parent 1: handle 2: tbf rate {DL_bitrate}mbit burst {burst}Kb lat 1ms')
                os.system(
                    f'sudo tc qdisc change dev {firstInterface} root handle 1: tbf rate {DL_bitrate}mbit burst {burst}Kb lat 1ms')
                os.system(
                    f'sudo tc qdisc change dev {secondInterface} root handle 1: tbf rate {DL_bitrate}mbit burst {burst}Kb lat 1ms')
                os.system(f'sudo tc qdisc show dev {rootInterface}')
                time.sleep(3)


if __name__ == "__main__":

    network = str(sys.argv[1])
    rootInterface = "eth0"
    firstInterface = "eth1"  # Jetson
    secondInterface = "eth2"  # Stream
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
    TC(filename, rootInterface, firstInterface,
       secondInterface, str(delay), str(jitter), str(burst))
