from config import sftp_config
from email_helper import send_email
import paramiko
import os


def upload_to_sftp(csv_file_path):
    ssh = None
    sftp = None
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        ssh.connect(
            sftp_config["host"],
            username=sftp_config["username"],
            password=sftp_config["password"],
        )

        # Create an SFTP session
        sftp = ssh.open_sftp()

        # Change to the desired directory
        sftp.chdir("inventory")

        file_name = os.path.basename(csv_file_path)

        # Upload the CSV file
        sftp.put(csv_file_path, file_name)
        print(f"File '{file_name}' uploaded successfully.")

    except paramiko.AuthenticationException:
        error_message = "Authentication failed, please verify your credentials."
        print(error_message)
        send_email(
            "Error in Xtreme Mat's process",
            f"Process Name: skuvault_inventory_to_ftp\n{error_message}",
        )
    except paramiko.SSHException as sshException:
        error_message = f"Unable to establish SSH connection: {sshException}"
        print(error_message)
        send_email(
            "Error in Xtreme Mat's process",
            f"Process Name: skuvault_inventory_to_ftp\n{error_message}",
        )
    except paramiko.SFTPError as sftpException:
        error_message = f"SFTP error: {sftpException}"
        print(error_message)
        send_email(
            "Error in Xtreme Mat's process",
            f"Process Name: skuvault_inventory_to_ftp\n{error_message}",
        )
    except FileNotFoundError:
        error_message = f"The file {csv_file_path} was not found."
        print(error_message)
        send_email(
            "Error in Xtreme Mat's process",
            f"Process Name: skuvault_inventory_to_ftp\n{error_message}",
        )
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        send_email(
            "Error in Xtreme Mat's process",
            f"Process Name: skuvault_inventory_to_ftp\n{error_message}",
        )
    finally:
        # Ensure SFTP session is closed
        if sftp:
            sftp.close()
            print("SFTP session closed.")
        # Ensure SSH connection is closed
        if ssh:
            ssh.close()
            print("SSH connection closed.")
