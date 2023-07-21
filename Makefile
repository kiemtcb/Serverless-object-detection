SHELL := /bin/bash # Use bash syntax
.PHONY: 4G
4G:
        sudo tc qdisc add dev eth0 root handle 1: netem delay 15ms
        sudo tc qdisc add dev eth0 parent 1: handle 2: tbf rate 40mbit burst 125Kb lat 1ms
.PHONY: 3.5G
3.5G:
        sudo tc qdisc add dev eth0 root handle 1: netem delay 25ms
        sudo tc qdisc add dev eth0 parent 1: handle 2: tbf rate 14mbit burst 97Kb lat 1ms

.PHONY: 3G
3G:
        sudo tc qdisc add dev eth0 root handle 1: netem delay 25ms
        sudo tc qdisc add dev eth0 parent 1: handle 2: tbf rate 2mbit burst 30Kb lat 1ms

.PHONY: wifi
wifi:
        sudo tc qdisc add dev eth0 root handle 1: netem delay 5ms
        sudo tc qdisc add dev eth0 parent 1: handle 2: tbf rate 150mbit burst 3500Kb lat 1ms

.PHONY: show
show:
        sudo tc qdisc show

.PHONY: del
del:
        sudo tc qdisc del dev eth0 root