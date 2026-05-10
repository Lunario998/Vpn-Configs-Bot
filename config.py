import os
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv("Token")
Github_Url = os.getenv("Github_Url")
Xray = os.getenv("Xray", "xray")
AdminID = int(os.getenv("AdminID", "123"))
