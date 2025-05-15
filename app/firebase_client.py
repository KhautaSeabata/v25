import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load credentials from environment variable
firebase_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)
db = firestore.client()
