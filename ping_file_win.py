# Import modules
import subprocess
import ipaddress
import easygui
import time
import re
import colorama

#### Select host file ####
print("Select a text file, listing IP addresses to ping.\n")
time.sleep(2)
file = easygui.fileopenbox(title='Host File')
print("\n")

def ping_stuff(i):
    # Prompt the user to input a network address
    net_addr = str.strip(i)

    # Configure subprocess to hide the console window
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = subprocess.SW_HIDE

    # For each IP address in the subnet, 
    # run the ping command with subprocess.popen interface
    output = subprocess.Popen(['ping', '-n', '2', '-w', '50', str(net_addr)], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
    timedout = re.search('.*100%', str(output))
    if timedout:
        print(colorama.Fore.RED + f'{net_addr} timed out')
    else:
        print(colorama.Fore.GREEN + f'{net_addr} responds to ICMP')

f = open(file)
netlist = f.readline()

while netlist:
    ping_stuff(netlist)
    netlist = f.readline()

f.close()
input (colorama.Fore.RESET + "Press enter to exit. :)")
