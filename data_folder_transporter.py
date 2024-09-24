import re

import paramiko
import ast
import os
import pdb





def parse_Linux_credentials():
  Linux_credentials = {}

  with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'), 'r') as file:
    lines = file.readlines()

    for line in lines:
      # Split the string on '='
      key, value = line.split('=')
      key = key.strip()
      value = value.strip()

      Linux_credentials[key] = value

  return Linux_credentials



credentials = parse_Linux_credentials()

username=credentials["username"]
password_host1 = credentials["password_host1"]
password_host2 = password_host1
host1 = credentials['host1']
host2 = credentials['host2']
local_data_folder=credentials['local_data_folder']



#_______________________________

def copy_dir(local_dir, remote_dir, sftp_object):
  for item in os.listdir(local_dir):
    local_path = os.path.join(local_dir, item)
    local_path = re.sub(r"\\", "/", local_path)
    remote_path = f"{remote_dir}/{item}"

    if os.path.isdir(local_path):
      try:
        sftp_object.stat(remote_path)
      except FileNotFoundError:
        sftp_object.mkdir(remote_path)
      copy_dir(local_path, remote_path, sftp_object)
    else:
      sftp_object.put(local_path, remote_path)
      print(f"[SUCCESS] {local_path} copied to {remote_path}")
#________________________

def send_folder_to_Virtual_Machine(local_folder_path, remote_folder_path):


  client1 = paramiko.SSHClient()
  client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client1.connect(host1, 22, username, password=password_host1)



  separator = '/'
  if os.name == "nt":
    # The operating system is Windows.
    print("The operating system is Windows.")
    separator = '\\'

  else:
    # The operating system is not Windows.
    print("The operating system is not Windows.")
    separator = '/'



  # Copy the file from local to the first server
  sftp = client1.open_sftp()

  # sftp.put(f"{local_file_path}/{file_name}", f"{remote_directory}/{file_name}")


  try:
    sftp.stat(remote_folder_path)
  except FileNotFoundError:
    sftp.mkdir(remote_folder_path)

  copy_dir(local_dir=local_folder_path, remote_dir=remote_folder_path, sftp_object=sftp)

  sftp.close()

  client1.close()



#_______________________________________




def send_folder_to_Virtual_Machine_via_JumpBox(local_folder_path,  remote_folder_path,  second_host_ip=None):
      separator = '/'
      if os.name == "nt":
          #The operating system is Windows.
          print("The operating system is Windows.")
          separator = '\\'

      else:
          #The operating system is not Windows.
          print("The operating system is not Windows.")
          separator = '/'


      if second_host_ip == None:
          second_host_ip = host2

      
      
      client1 = paramiko.SSHClient()
      client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client1.connect(host1, 22, username, password=password_host1)

      transport = client1.get_transport()
      dest_addr = (second_host_ip, 22)
      local_addr = (host1, 22)
      channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

      client2 = paramiko.SSHClient()
      client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client2.connect(host2, 22, username, password=password_host2, sock=channel)



      # Copy the file from local to the first server
      sftp = client1.open_sftp()

      
      # sftp.put(f"{local_file_path}/{file_name}", f"{remote_directory}/{file_name}")

      # Open an SFTP session on the second server
      sftp2 = client2.open_sftp()

      print("connected....")
      try:
          sftp2.stat(remote_folder_path)
      except FileNotFoundError:
          sftp2.mkdir(remote_folder_path)


      copy_dir(local_dir=local_folder_path, remote_dir=remote_folder_path, sftp_object=sftp2)

      

      sftp.close()
      sftp2.close()


      client1.close()
      client2.close()


#_______________________________________


if __name__ == "__main__":
  local_folder_path = "C:/Users/xario/OneDrive/Documents/work/public-dashboard/Data"
  remote_folder_path = "/root/public-dashboard/Data"

  # local_folder_path = "C:/Users/xario/OneDrive/Documents/work/copydebug"
  # remote_folder_path = "/root/testing"
  #send_folder_to_Virtual_Machine(local_folder_path, remote_folder_path)


  local_folder_path = local_data_folder
  remote_folder_path = "/user_apps/singularity_user_containers/R_rocker_tephi/app/secondTEPHIDemo/public-dashboard/Data"
  send_folder_to_Virtual_Machine_via_JumpBox(local_folder_path, remote_folder_path)