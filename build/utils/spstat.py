import sys

stat = [0] * 65536

def noi2sym(filename):
    with open(filename) as f:
        line = f.readline()
        while line:
            decoded_line = [x.strip() for x in line.split('=')]
            if decoded_line[0] == 'SP':
                addr = int(decoded_line[1], 16)
                stat[addr] = stat[addr] + 1
            line = f.readline()
    with open(f"{filename}.stat", "w") as f:
        for index, item in enumerate(stat):
            f.write(f"{index},{item}\n")

if __name__=='__main__':
    noi2sym(sys.argv[1])
