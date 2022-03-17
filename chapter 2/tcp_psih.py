# TCP port scanner that utilizes a TCP full connect scan to identify hosts

# // two things to learn:
## how to code a basic TCP port scanner
## how to use the optparse  to parse hostname and ports

# // basic steps
# first we need hostname and ports
# second if hostnames transalated into ipv4
# for loop for the list of ports connect to the ipv4 and that property
# reply if port is open or not

# metaspoitabl e= 192.168.52.128

from optparse import OptionParser
from socket import *
from threading import *

# lock that prevents other threads from proceeding
screenlock = Semaphore(value=1)

# popular ports
popular_ports_list = ['23', '554' , '3306', '179', '1080', '161', '162', '445', '5432', '9092', '6379', '80', '443', '22', '21', '8080', '23', '25' ,'53', '587', '993', '995', '8443', '465', '1080']

# connScan (tgtHost, tgtPort) --> connection to the target host and port
def connScan(tgtHost, tgtPort):
    try:
        # creating a socket
        s = socket(AF_INET, SOCK_STREAM)
        # connecting it
        s.connect((tgtHost, tgtPort))
        message = bytes("message\r\n", "utf-8")
        s.send(message)
        results = s.recv(1024)
        screenlock.acquire()
        print("[+] "+ str(tgtPort) + "/tcp Opened")
        print("[#] " + str(results))
    except:
        screenlock.acquire()
        print("[-] "+ str(tgtPort) + "/tcp Closed")
    finally:
        screenlock.release()
        s.close()


# portScan (ipv4 + port) --> get host ipv4 enemurate each port attempting to connect using the connScan
def portScan(tgtHost, tgtPorts):
    # we need to resolve the host to ipv4
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[!] Cannot resolve, Unknown host")
        return

    # now connect it
    try:
        tgtName = gethostbyaddr(tgtIP)
        print("Scan result for " + tgtName[0])
    except:
        print("Scan result for " + tgtIP)

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()




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

    portScan(tgtHost, tgtPorts)


if __name__ == '__main__':
    main()
