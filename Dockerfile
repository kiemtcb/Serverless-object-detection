FROM ubuntu
RUN apt update 
RUN apt install curl nano vim net-tools iputils-ping -y
RUN apt install python3-pip -y
RUN pip3 install xlsxwriter
RUN mkdir curl
COPY curl curl
COPY process.py curl
WORKDIR curl
CMD ["sleep","infinity"]

