import logging
import easygui
import getpass
import time
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect


# Set logging parameters
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='single_cmd.log', level=logging.INFO)

# Welcome message
print("Welcome to the network device single command script.\n\n")

#### Select host file ####
print("Select a text file, listing IP addresses of your devices.\n")
time.sleep(2)
file = easygui.fileopenbox(title='Host File')
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

# Set the command and device type
print("\nEnter the command to be run on all devices.")
command = input("Command: ")

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
    }

    # SSH to the device and run command
    logging.info(f'Running command on {i}')
    print(f'Running command on {i}')
    cmd = command
    try:
        connect = ConnectHandler(**ssh)
        output = connect.send_command(cmd, expect_string=r'#')
    except Exception:
        logging.error(f'Failed to connect to {i}')
        print(f'ERROR: Failed to connect to {i}')
        return
    logging.info(output)
    print(output)
    fout.write(f'\n! Command Output From {i}')
    fout.write(output)


#Open a text file for output.
fout = open(f'{path}/output.txt','a+')

# Open the host text file and read each line
f = open(file)
line = f.readline()

while line:
    showcmd(line)
    line = f.readline()

f.close()
print(f'Results have been written to {path}\\output.txt')
input ("Press enter to exit. :)")
