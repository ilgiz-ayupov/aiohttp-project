import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate("quiz-db-326518-26815d260006.json")
firebase_admin.initialize_app(cred)

db = firestore.client()