import boto3
from botocore.exceptions import ClientError
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        # Retrieve the secret
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # Handle the error
        raise e
    else:
        # Secrets Manager decrypts the secret value and returns it as a string.
        secret = response['SecretString']
        return secret

def linkedin_login(username, password):
    # Path to your GeckoDriver executable
    driver_path = 'path to geckodriver binary'
    firefox_binary_path = 'C:/Program Files/Mozilla Firefox/firefox.exe'
    firefox_options = Options()
    firefox_options.binary_location = firefox_binary_path
    firefox_options.add_argument("--private")  # Open in private mode

    service = Service(driver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.get("https://www.linkedin.com/login")
    driver.maximize_window()

    time.sleep(3)

    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)

    time.sleep(10)
    driver.close() #or quit()

secret_name = "webapp_creds" #name of the secret, webapp_creds in the pic
region_name = "us-east-1"

secret_json = get_secret(secret_name, region_name)
secret = json.loads(secret_json)

# Extract credentials from the secret
username = secret["email"] #var name, email on the example pic
password = secret["password"] # same for passoword

linkedin_login(username, password)
