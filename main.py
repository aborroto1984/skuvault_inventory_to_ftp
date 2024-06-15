from sku_vault_api import get_products_inventory, get_items_inventory
from helpers import create_temp_folder_with_csv
from email_helper import send_email

from sftp import upload_to_sftp
import pandas as pd


def main():
    try:
        # inventory = get_products_inventory()
        inventory = get_items_inventory()
        df = pd.DataFrame(inventory)
        temp_folder, csv_file_path = create_temp_folder_with_csv(df)
        upload_to_sftp(csv_file_path, "remote_directory")
        pass
    except Exception as e:
        send_email(
            "Error in Xtreme Mat's process",
            f"Process Name: skuvault_inventory_to_ftp\n{str(e)}",
        )
        return


if __name__ == "__main__":
    main()
