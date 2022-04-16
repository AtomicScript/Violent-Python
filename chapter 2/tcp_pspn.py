# Integerating the Nmap Port scanner

# two functions needed here
# nmap scan that uses nmap to scan the targeted port and and host
# main that parses

import nmap
from optparse import OptionParser

# popular ports
popular_ports_list = ['23', '554' , '3306', '179', '1080', '161', '162', '445', '5432', '9092', '6379', '80', '443', '22', '21', '8080', '23', '25' ,'53', '587', '993', '995', '8443', '465', '1080']


def nmapScan(tgtHost, tgtPort):
    # create an instance of the port scanner
    nmScan = nmap.PortScanner()
    # PortScanner has the function scan tages in two arguments
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    if state == 'open':
        print(f"[+] {tgtHost} tcp/{tgtPort} {state}")
    elif state == 'closed':
        print(f"[-] {tgtHost} tcp/{tgtPort} {state}")
    else:
        print(f"[!!] Something went wrong {tgtHost}/{tgtPort}")




def main():
    # The usage summary to print when your program is run incorrectly or with a help option
    parser = OptionParser('usage %prog -H <target host> -p <target port> ')

    # adding options we have two options host and ports

    # seems like add option has 4 arguments
    # 1 the option
    # 2 the variable
    # 3 type of variable
    # 4 help
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port, separated by comma')

    # scanning popular ports
    parser.add_option('--p', dest='pp', default=False)


    # when arguments are given parse them
    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(",")
    # want it as a boolean
    ppoption = bool(options.pp)


    # now we need to print the usage if no arguments are given
    if (tgtHost == None) | (tgtPorts[0] == None) :
        print(parser.usage)
        exit(0)

    # if its true add it to the tgtports
    if ppoption == True:
        print("[!] Activated using Popular Lists")
        for port in popular_ports_list:
            if port not in tgtPorts:
                tgtPorts.append(port)


    for port in tgtPorts:
        nmapScan(tgtHost, port)


if __name__ == '__main__':
    main()
