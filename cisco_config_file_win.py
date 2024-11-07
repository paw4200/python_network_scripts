import logging
import easygui
import getpass
import time
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect


# Set logging parameters
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='config_file.log', level=logging.INFO)

# Welcome message
print("Welcome to the network device configuration script.")
print("This script uses a text file listing configuration")
print("commands to configure devices listed in another")
print("text file. The configuration is saved on each device.\n")
time.sleep(1)

#### Select host file ####
print("Select a text file, listing IP addresses of your devices.\n")
time.sleep(2)
file = easygui.fileopenbox(title='Host File')
print("\n")

#### Select the configuration file ####
print("Select a text file, listing configuration commands.\n")
time.sleep(2)
conf_file = easygui.fileopenbox(title='Config File')
print("\n")

#### Select directory for output file ####
print("Select the folder where the output file should be saved.\n")
time.sleep(2)
d = easygui.diropenbox(title='Output File Location')
path = d

# Set the username and password for SSH sessions.
print("Enter the username and password used to connect to devices.")
user = input("Username: ")
password = getpass.getpass()

print("\n")
print("Device Types\n")
print("1. Cisco IOS\n")
print("2. Cisco NXOS\n")

device_type = "empty"

while device_type == "empty":
    while True:
        try:
            choice = int(input("Select the device type (1-2): "))
            break
        except ValueError:
            print ("\nSorry, that is not a valid number.")
    if choice not in (1,2,3):
        print ("\nSorry, please select an option (1, 2, or 3)")
    else:
        device_type = (choice)

if device_type == 1:
    device = "cisco_ios"
else:
    device = "cisco_nxos"

print('\n')

### Connection Function ###
def showcmd(i):

    # SSH settings
    ssh = {
        'device_type': device,
        'host': i,
        'username': user,
        'password': password,
        'fast_cli': False
    }

    # SSH to the device and run command
    logging.info(f'Configuring {i}')
    print(f'\nConfiguring {i}')
    
    try:
        connect = ConnectHandler(**ssh)
        output = connect.send_config_from_file(conf_file)
        output += connect.save_config()
    except Exception:
        logging.error(f'Failed to connect to {i}')
        print(f'ERROR: Failed to connect to {i}')
        return
    logging.info(output)
    fout.write(f'\n! Command Output From {i}')
    fout.write(output)
    print(output)


#Open a text file for output.
fout = open(f'{path}/config_file.txt','a+')

# Open the host text file and read each line
f = open(file)
line = f.readline()

while line:
    showcmd(line)
    line = f.readline()

f.close()
print(f'Results have been written to {path}\\config_file.txt')
input ("Press enter to exit. :)")
