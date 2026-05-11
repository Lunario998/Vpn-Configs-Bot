import os
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv("Token")
Github_Black_Full = os.getenv("Github_Black_Full")
Github_Black_Mobile = os.getenv("Github_Black_Mobile")
Github_White_Full = os.getenv("Github_White_Full")
Github_White_Mobile = os.getenv("Github_White_Mobile")
Xray = os.getenv("Xray", "xray")
AdminID = int(os.getenv("AdminID", "123"))
