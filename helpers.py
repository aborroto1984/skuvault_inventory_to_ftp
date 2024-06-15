import os
from datetime import datetime


def create_temp_folder_with_csv(df):
    # Define the main tmp folder
    main_tmp_folder = os.path.join(os.getcwd(), "tmp")

    # Ensure the main tmp folder exists
    os.makedirs(main_tmp_folder, exist_ok=True)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a timestamped subfolder inside the main tmp folder
    timestamped_folder = os.path.join(main_tmp_folder, f"tmp_{timestamp}")
    os.makedirs(timestamped_folder, exist_ok=True)

    # Path for the new CSV file
    csv_file_path = os.path.join(timestamped_folder, "XtremeQty.csv")

    # Save the DataFrame to the CSV file
    df.to_csv(csv_file_path, index=False)

    return timestamped_folder, csv_file_path
