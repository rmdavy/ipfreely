import netaddr
from netaddr import IPNetwork
import argparse


def banner():
    print("""                               
 ___________  __               _       
|_   _| ___ \/ _|             | |      
  | | | |_/ / |_ _ __ ___  ___| |_   _ 
  | | |  __/|  _| '__/ _ \/ _ \ | | | |
 _| |_| |   | | | | |  __/  __/ | |_| |
 \___/\_|   |_| |_|  \___|\___|_|\__, |
                                  __/ |
                                 |___/ 

Version 0.1a
@rd_pentest

""")

def main():

    #Show Banner
    banner()

    #Get command line args
    p = argparse.ArgumentParser("python3 ipfreely.py --subnets subnets.txt --exclusions exclusions.txt --output ips.txt", formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=20,width=150),description = "Creates a set of ips to work with")

    p.add_argument("-fs", "--subnets", dest="subnets", required=True,help="File containins allowed subnet(s)")
    p.add_argument("-fe", "--exclusions", dest="exclusions", required=True,help="File containing ip/subnet exlusions")
    p.add_argument("-fo", "--outputfile", dest="outputfile", default="",help="Output filename for list of ips")

    args = p.parse_args()

    #READ IN ALL THE SUBNETS/IPS TO WORK WITH
    GoodList=[]

    #Open subnets file and read in
    file = open(args.subnets,  'r')
    lines = file.readlines()
    for line in lines:
        for address in IPNetwork(line.strip()):
            GoodList.append(address)

    #Sort and unique Goodlist
    GoodList = sorted(set(GoodList))


    #READ IN ALL THE SUBNETS/IPS TO EXCLUDE
    BadList=[]

    #Open exclusions file and read in
    file = open(args.exclusions,  'r')
    lines = file.readlines()
    for line in lines:
        for address in IPNetwork(line.strip()):
            BadList.append(address)

    #Sort and unique badlist
    BadList = sorted(set(BadList))

    #Find exluded ips in goodlist and remove
    for b_ip in BadList:
        for g_ip in GoodList:
            if b_ip==g_ip:
                GoodList.remove(b_ip)

    #Either display IPs on screen or save them to file
    if args.outputfile=="":    
        for f in GoodList:
            print (f)
    else:
        myfile = open(args.outputfile, mode='wt', encoding='utf-8')
        #IPs and write to file
        for f in GoodList:
            myfile.write(str(f)+"\n")
        #Close file handler
        myfile.close

        print ("[*] IPs to work with have been written to "+args.outputfile)

#Loads up main
if __name__ == '__main__':
    #Call main routine.
    main()