import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from tools import get_champions, get_current_patch
from dotenv import load_dotenv


load_dotenv()

def lambda_handler(event, context):
    patch = get_current_patch()
    region = os.environ["region"]
    data_frames = get_champions(region, patch)
    conn = get_snowflake_connection()

    try:
        for table_name, df in data_frames.items():
            publish_to_snowflake(table_name, df, conn)
    finally:
        conn.close()

def get_snowflake_connection():
    return snowflake.connector.connect(
            account=os.environ["snowflake_account"],
            user=os.environ["snowflake_user"],
            authenticator="PROGRAMMATIC_ACCESS_TOKEN",
            token=os.environ["SNOWFLAKE_PAT"],
            role=os.environ["snowflake_role"],
            warehouse=os.environ["snowflake_wearhouse"],
            database=os.environ["snowflake_database"],
            schema=os.environ["snowflake_schema"]
        )

def publish_to_snowflake(table_name, df, conn):
    success, n_chunks, n_rows, _ = write_pandas(
    conn,
    df,
    table_name=table_name,
    auto_create_table=True,
    overwrite=False,
    )
    print(success, n_rows)
