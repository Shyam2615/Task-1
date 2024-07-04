# import os

# sender_email = os.getenv('EMAIL')
# password = os.getenv('PASSWORD')

# print("Running")
# print(sender_email, password)

import os
from dotenv import load_dotenv

load_dotenv()

def check_env_variables():
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    print(f"EMAIL: {email}")
    print(f"PASSWORD: {password}")

check_env_variables()