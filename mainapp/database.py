import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("quiz-db.json")
firebase_admin.initialize_app(cred, {
    "projectId": "quiz-db-326518"
})
db = firestore.client()