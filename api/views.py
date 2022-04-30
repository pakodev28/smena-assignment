import base64
import json
import os.path

import requests
from django.shortcuts import render
from django_rq import job
from django.core.files.base import ContentFile
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Check, Printer
from .serializers import CreateCheckSerializer, GetCheckSerializer


class ListNewCheckAPIView(ListAPIView):
    queryset = Check.objects.all()
    serializer_class = GetCheckSerializer

    def list(self, request, *args, **kwargs):
        try:
            printer = Printer.objects.get(api_key=request.query_params.get("api_key"))
            new_checks = printer.checks.filter(status="new")
            serializer = self.get_serializer(new_checks, many=True)
            return Response({"checks": serializer.data}, status=status.HTTP_200_OK)
        except Printer.DoesNotExist:
            return Response(
                {"error": "Ошибка авторизации"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@job
def create_pdf_file(check):
    url = "http://wkhtmltopdf_service:80/"
    if check.type == "client":
        template = "client_check.html"
    else:
        template = "kitchen_check.html"
    context = {"order": check.order}
    data = {
        "contents": base64.b64encode(render(None, template, context).content).decode(
            "utf-8"
        ),
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    filename = f"{check.order.get('id')}_{check.type}.pdf"
    check.status = "rendered"
    check.pdf_file.save(filename, ContentFile(response.content))
    with open(check.pdf_file.path, "wb") as f:
        f.write(response.content)
    check.save()


class CreateChecksAPIView(CreateAPIView):
    queryset = Check.objects.all()
    serializer_class = CreateCheckSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        printers = Printer.objects.filter(point_id=data.get("point_id"))
        if printers is None:
            return Response(
                {"error": "Для данной точки не настроено ни одного принтера"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        checks = Check.objects.filter(order__id=data.get("id")).exists()
        if checks:
            return Response(
                {"error": "Для данного заказа уже созданы чеки"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for printer in printers:
            check = Check.objects.create(
                printer_id=printer, type=printer.check_type, order=data
            )
            create_pdf_file.delay(check)
        return Response({"ok": "Чеки успешно созданы"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_check_pdf(request):
    api_key = request.query_params.get("api_key")
    check_id = request.query_params.get("check_id")

    printer = Printer.objects.filter(api_key=api_key).exists()
    if printer == False:
        return Response(
            {"error": "Ошибка авторизации"}, status=status.HTTP_401_UNAUTHORIZED
        )

    check = Check.objects.filter(pk=check_id).first()
    if check is None:
        return Response(
            {"error": "Данного чека не существует"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    file = check.pdf_file
    if file is None:
        return Response(
            {"error": "Для данного чека не сгенерирован PDF-файл"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    file = open(file.path, "rb")
    response = HttpResponse(file, content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f"attachment; filename={os.path.basename(file.name)}"
    check.status = "printed"
    check.save()
    return response
