import uuid

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append(
    {
        "id": str(uuid.uuid4()),
        "name": "User01",
        "email": "user01@example.com",
        "is_active": True,
    }
)
data_list.append(
    {
        "id": str(uuid.uuid4()),
        "name": "User02",
        "email": "user02@example.com",
        "is_active": True,
    }
)
data_list.append(
    {
        "id": str(uuid.uuid4()),
        "name": "User03",
        "email": "user03@example.com",
        "is_active": False,
    }
)  # Ejemplo de item inactivo


class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        active_items = [item for item in data_list if item.get("is_active", False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Validación mínima
        if "name" not in data or "email" not in data:
            return Response(
                {"error": "Faltan campos requeridos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["id"] = str(uuid.uuid4())
        data["is_active"] = True
        data_list.append(data)

        return Response(
            {"message": "Dato guardado exitosamente.", "data": data},
            status=status.HTTP_201_CREATED,
        )


class DemoRestApiItem(APIView):
    def get(self, request, id):
        for item in data_list:
            if item["id"] == id:
                return Response(item, status=status.HTTP_200_OK)
        return Response(
            {"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request, id):
        data = request.data
        if "id" not in data or data["id"] != id:
            return Response(
                {"error": "El campo id es obligatorio y debe coincidir con la URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for idx, item in enumerate(data_list):
            if item["id"] == id:
                new_item = data.copy()
                new_item["id"] = id
                data_list[idx] = new_item
                return Response(
                    {"message": "Elemento reemplazado exitosamente.", "data": new_item},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    def patch(self, request, id):
        data = request.data
        for item in data_list:
            if item["id"] == id:
                item.update({k: v for k, v in data.items() if k != "id"})
                return Response(
                    {"message": "Elemento actualizado parcialmente.", "data": item},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request, id):
        for item in data_list:
            if item["id"] == id:
                item["is_active"] = False
                return Response(
                    {"message": "Elemento eliminado lógicamente."},
                    status=status.HTTP_200_OK,
                )
        return Response(
            {"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

