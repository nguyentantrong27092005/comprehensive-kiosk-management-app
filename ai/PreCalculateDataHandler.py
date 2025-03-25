import pymysql
import pandas as pd
from datetime import datetime
import os
from google.cloud import storage
from dotenv import load_dotenv
from common.sql_func import Database


def main():
    db = Database()
    sql_files = ["best_seller.sql", "evoucher.sql", "mon_duoc_tang.sql", "tong_doanh_thu_monthly.sql", "tong_doanh_thu_weekly.sql"]  # List of your SQL files
    load_dotenv(dotenv_path='.env')
    try:
        for sql_file in sql_files:
            print(f"Executing {sql_file}...")
            results = db.execute_sql_file("sql/ai_calculate_measures/"+sql_file)
            print(f"Finished executing {sql_file}.\n")
            df = pd.DataFrame(results)
            txt_path = f'ai/tmp/{sql_file.replace(".sql", "")}.txt'
            df.to_csv(txt_path, index=False, encoding='utf-8-sig', sep=',')
            print(df)
            bucket_name = "kioskappstorage"
            destination_blob_name = f'mysql_aggregated_data/{sql_file.replace(".sql", "")}.txt'
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_filename(txt_path)
            print(f"Uploaded to GCS: gs://{bucket_name}/{destination_blob_name}")
            os.remove(txt_path)

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

    finally:
        if db.conn:
            db.conn.close()
            print("Connection closed.")




if __name__ == '__main__':
    main()
