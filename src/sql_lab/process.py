import os
import logging
import pandas as pd
import mysql.connector

# Configure logging to report status
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_data(filename):
    """
    Loads data from a CSV file into a pandas DataFrame.

    Parameters:
        filename (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded dataset.
    """
    logging.info(f"Reading CSV file from: {filename}")

    # Load CSV data into a pandas DataFrame
    df = pd.read_csv(filename)

    logging.info(f"Successfully loaded {len(df)} rows from {filename}")
    return df


def clean_data(data):
    """
    Prepares the DataFrame for upload by removing rows with missing values.

    Parameters:
        data (pd.DataFrame): The raw DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame with NULL rows dropped.
    """
    logging.info("Cleaning data: removing rows with missing values...")
    initial_count = len(data)

    # Drop any rows containing missing (NaN / NULL) values
    cleaned_df = data.dropna().copy()

    removed_count = initial_count - len(cleaned_df)
    logging.info(
        f"Removed {removed_count} rows containing missing values. "
        f"{len(cleaned_df)} rows remaining."
    )
    return cleaned_df


def load_data(data, table="mock"):
    """
    Creates the destination table in MySQL if it does not exist and uploads 
    the DataFrame rows using parameterized INSERT statements.

    Parameters:
        data (pd.DataFrame): The cleaned DataFrame to upload.
        table (str): The name of the MySQL table (defaults to 'mock').
    """
    # Read DB host, DB name, DB user, DB password from environment variables
    db_host = (os.getenv("DBHOST") or "").strip()
    db_user = (os.getenv("DBUSER") or "").strip()
    db_pass = (os.getenv("DBPASS") or "").strip()
    db_name = (os.getenv("DBNAME") or "").strip()
    # Validate that all required environment variables are present
    if not all([db_host, db_user, db_pass, db_name]):
        logging.error("Missing required environment variables (DBHOST, DBUSER, DBPASS, DBNAME).")
        return

    conn = None
    cursor = None

    try:
        logging.info(f"Connecting to MySQL database '{db_name}' at {db_host}...")
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            port=3306
        )
        cursor = conn.cursor()

        # Step 1: Create table if it doesn't exist
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS `{table}` (
            `id` BIGINT,
            `group` VARCHAR(255),
            `item_name` VARCHAR(255),
            `quantity` DOUBLE,
            `price` BIGINT,
            `store_location` VARCHAR(255)
        );
        """
        cursor.execute(create_table_sql)
        logging.info(f"Table '{table}' ensured in database.")

        # Step 2: Prepare parameterized INSERT query (%s placeholders to prevent SQL injection)
        cols = ", ".join([f"`{c}`" for c in data.columns])
        placeholders = ", ".join(["%s"] * len(data.columns))
        insert_sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"

        # Convert DataFrame rows into a list of tuples
        records = [tuple(row) for row in data.itertuples(index=False)]

        logging.info(f"Uploading {len(records)} rows to table '{table}'...")
        cursor.executemany(insert_sql, records)
        conn.commit()
        logging.info(f"Successfully loaded {cursor.rowcount} rows into table '{table}'.")

    except mysql.connector.Error as err:
        logging.error(f"Database error occurred: {err}")
    finally:
        # Wrap database connection cleanup in finally block
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logging.info("MySQL connection closed.")


def main():
    """
    Main function executing read_data, clean_data, and load_data in sequence.
    """
    csv_file = "MOCK_DATA.csv"

    # Step 1: Read raw CSV
    raw_df = read_data(csv_file)

    # Step 2: Clean missing rows
    cleaned_df = clean_data(raw_df)

    # Step 3: Load into table 'mock'
    load_data(cleaned_df, table="mock")


if __name__ == "__main__":
    main()
