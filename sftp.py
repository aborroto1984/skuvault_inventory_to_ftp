from config import sftp_config
import paramiko


def upload_to_sftp(local_file_path, remote_directory):
    try:
        # Create a transport object
        transport = paramiko.Transport((sftp_config["host"], 22))
        transport.connect(
            username=sftp_config["usewrname"], password=sftp_config["password"]
        )

        # Create an SFTP session
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Change to the target directory on the SFTP server
        try:
            sftp.chdir(remote_directory)
        except IOError:
            # If the directory does not exist, create it
            sftp.mkdir(remote_directory)
            sftp.chdir(remote_directory)

        # Upload the file
        sftp.put(
            local_file_path, remote_directory + "/" + local_file_path.split("/")[-1]
        )
        print(f"Successfully uploaded {local_file_path} to {remote_directory}")

    except Exception as e:
        print(f"Failed to upload {local_file_path}: {e}")

    finally:
        # Close the SFTP session and transport
        if "sftp" in locals():
            sftp.close()
        if "transport" in locals():
            transport.close()


upload_to_sftp("test_path", "remote_directory")
