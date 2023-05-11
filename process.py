import subprocess
import xlsxwriter
from time import sleep
workbook = xlsxwriter.Workbook('Example2.xlsx')
worksheet = workbook.add_worksheet()
file_image = ["4K.jpg", "2K.jpg", "FullHD.jpg",
              "HD.jpg", "480p.jpg", "360.jpg"]


def measure(file, column):
    for x in range(5):
        row = 0
        address = 'http://mec.default.svc.cluster.local/api/picture'
        command = 'curl -w @curl-format.txt ' + \
            '-F upload=@' + file + ' -o /dev/null -s ' + address
        time_namelookup = subprocess.getoutput(command)
        result = list(time_namelookup.split(" "))
        for item in result:
            worksheet.write(row, column, item)
            row += 1
        sleep(5)
        row += 3
        time_namelookup = subprocess.getoutput(command)
        result = list(time_namelookup.split(" "))
        for item in result:
            worksheet.write(row, column, item)
            row += 1
        column += 1
        sleep(45)


column = 0
for x in file_image:
    print(x)
    measure(x, column)
    column = column + 2
workbook.close()
