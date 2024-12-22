import pandas as pd
from minio import Minio
from minio.error import S3Error
import time
import os


def main():
    df = pd.read_parquet(
        "hf://datasets/Norod78/ChristmasClaymation-blip-captions/data/train-00000-of-00001-c8a3f24f82edb8a0.parquet"
    )

    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "minio:9000",
        access_key="user",
        secret_key="userkey123",
        secure=False,
    )

    # The destination bucket and filename on the MinIO server
    bucket_name = "bucket"

    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    for i, row in df.iterrows():
        time.sleep(0.5)
        with open("image.png", "wb") as f:
            f.write(row["image"]["bytes"])
        source_file = "image.png"
        destination_file = f"img_{i}.png"
        try:
            # Upload the file, renaming it in the process
            client.fput_object(
                bucket_name,
                destination_file,
                source_file,
            )
            print(
                source_file,
                "successfully uploaded as object",
                destination_file,
                "to bucket",
                bucket_name,
            )
            os.remove(source_file)
        except S3Error as exc:
            print("error occurred while loading", i, exc)


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
