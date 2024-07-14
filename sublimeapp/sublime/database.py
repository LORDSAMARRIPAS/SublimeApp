import boto3
import psycopg2


class DatabaseManager:
    def __init__(self, s3_access_key, s3_secret_key, s3_bucket_name, db_name, db_user, db_password, db_host, db_port):
        self.s3_access_key = s3_access_key
        self.s3_secret_key = s3_secret_key
        self.s3_bucket_name = s3_bucket_name
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def connect(self):
        s3 = boto3.resource('s3',
                            aws_access_key_id=self.s3_access_key,
                            aws_secret_access_key=self.s3_secret_key)
        bucket = s3.Bucket(self.s3_bucket_name)
        return bucket

    def connect_to_database(self):
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            return conn
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)
            return None

    def upload_data(self, file_path, s3_key):
        bucket = self.connect()
        bucket.upload_file(file_path, s3_key)

    def delete_data(self, s3_key):
        bucket = self.connect()
        obj = bucket.Object(s3_key)
        obj.delete()

    def modify_data(self, query):
        conn = self.connect_to_database()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
                cur.close()
                print("Data modified successfully")
            except psycopg2.Error as e:
                print("Error executing query:", e)
            finally:
                conn.close()


if __name__ == "__main__":
    # Initialize DatabaseManager
    db_manager = DatabaseManager(
        s3_access_key="S3_ACCESS_KEY",
        s3_secret_key="S3_SECRET_KEY",
        s3_bucket_name="S3_BUCKET_NAME",
        db_name="DB_NAME",
        db_user="DB_USER",
        db_password="DB_PASSWORD",
        db_host="DB_HOST",
        db_port="DB_PORT"
    )

    # db_manager.upload_data("example.csv", "data/example.csv")
    # db_manager.delete_data("data/example.csv")
    # db_manager.modify_data("UPDATE table_name SET column_name = 'new_value' WHERE condition;")
