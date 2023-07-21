import boto3
import os
from datetime import datetime

def backup_secrets(output_dir):
    # Create a session using your AWS credentials and regional settings
    session = boto3.Session()

    # Create the AWS Secrets Manager client using the created session
    client = session.client('secretsmanager')

    # List all secrets
    secrets = client.list_secrets(MaxResults=100)['SecretList']

    # Create a directory for backups if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for secret in secrets:
        secret_name = secret['Name']
        get_secret_response = client.get_secret_value(SecretId=secret_name)

        # Decode the secret value as it comes in bytes format
        if 'SecretString' in get_secret_response:
            secret_data = get_secret_response['SecretString']
        else:
            # If the secret is binary, convert it to base64 to save to a file
            import base64
            secret_data = base64.b64encode(get_secret_response['SecretBinary']).decode()

        # Save the secret to a file with the secret name as the filename
        backup_file_path = os.path.join(output_dir, f"{secret_name.replace('/', '_')}.txt")
        with open(backup_file_path, "w") as backup_file:
            backup_file.write(secret_data)

        print(f"Backup of '{secret_name}' saved to '{backup_file_path}'.")

if __name__ == "__main__":
    # Replace 'backup_directory' with the directory where you want to save the backups
    backup_directory = "/backup"

    backup_secrets(backup_directory)

