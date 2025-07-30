from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing_collection"  # Cambia el nombre según tu colección en Firebase

    # Aquí puedes agregar los métodos CRUD (get, post, put, patch, delete) según lo necesites