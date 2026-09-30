#!/usr/bin/env python3

import logging
import os
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd

# Configure logging for non-main functions
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Read credentials from environment variables using same pattern as process.py
DBHOST = os.environ.get("DBHOST", "ds2022.cgls84scuyle.us-east-1.rds.amazonaws.com")
DBUSER = os.environ.get("DBUSER", "")
DBPASS = os.environ.get("DBPASS", "")
DBNAME = os.environ.get("DBNAME", "")

# Establish global connection matching basic-sql.py structure
try:
    db = mysql.connector.connect(
        user=DBUSER, host=DBHOST, password=DBPASS, database=DBNAME, port=3306
    )
    cur = db.cursor()
except mysql.connector.Error as err:
    logging.error(f"Failed to connect to MySQL database: {err}")
    db = None
    cur = None


def get_data_by_group(value):
    """
    Returns rows from the 'mock' table where the 'group' column equals value.
    Takes one argument, value, and returns a list of tuples containing the matching rows, or None on error.
    """
    logging.info(f"Fetching rows from 'mock' where `group` = '{value}'")
    # `group` is quoted in backticks because GROUP is a reserved SQL keyword
    query = "SELECT * FROM `mock` WHERE `group` = %s;"
    try:
        cur.execute(query, (value,))
        results = cur.fetchall()
        output = []
        for r in results:
            output.append(r)
        return output
    except mysql.connector.Error as e:
        logging.error(f"MySQL Error: {e}")
        return None


def plot_counts(groupby):
    """
    Count rows per distinct value of a given column, show a bar chart, and return a DataFrame.
    Takes one argument, groupby, and returns a dataframe containing distinct values and their counts, or None on error
    """
    logging.info(f"Grouping and counting rows by column '{groupby}'")
    # Dynamic column grouping with backtick quoting around the column name
    query = f"SELECT `{groupby}`, COUNT(`{groupby}`) FROM `mock` GROUP BY `{groupby}`;"
    try:
        cur.execute(query)
        results = cur.fetchall()
        output = []
        for r in results:
            output.append(r)
        df = pd.DataFrame(output, columns=[groupby, "count"])
        
        # Plot bar chart matching basic-sql.py approach
        df.plot.bar(x=groupby, y="count")
        plt.tight_layout()
        plt.show()
        return df
    except mysql.connector.Error as e:
        logging.error(f"MySQL Error: {e}")
        return None


def main():
    """Runs demonstration queries and closes the database connection."""
    print("=== Filter by group ('Online') ===")
    online_results = get_data_by_group("Online")
    print(online_results)

    print("\n=== Plot counts by group ===")
    df_group = plot_counts("group")
    print(df_group)

    print("\n=== Plot counts by item_name ===")
    df_item = plot_counts("item_name")
    print(df_item)

    if cur:
        cur.close()
    if db and db.is_connected():
        db.close()


if __name__ == "__main__":
    main()
