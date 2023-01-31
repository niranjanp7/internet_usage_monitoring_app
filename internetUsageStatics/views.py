from .const import CONST
from .models import DataUsage

import time
import re

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class DataUsageDetails(View):
    def get(self, request: WSGIRequest):
        return HttpResponse(request.GET.get("s"))

    def post(self, request: WSGIRequest):

        # form data
        if request.POST.__len__() > 0:
            response = self.__handle_form_data(request)
            return JsonResponse(response, status=response["status"])

        # file
        if request.FILES.get("file"):
            print(request.FILES.get("file"))

        return JsonResponse(
            data={"status": 400, "error": "Invalid request body"}, status=400
        )

    def __handle_form_data(self, request: WSGIRequest):

        response: dict[str, int | str] = {
            "status": 200,
        }

        data = {
            CONST.USERNAME: request.POST.get(CONST.USERNAME, ""),
            CONST.MAC_ADDRESS: request.POST.get(CONST.MAC_ADDRESS, ""),
            CONST.START_TIME: request.POST.get(CONST.START_TIME, "01-01-1999 00.00"),
            CONST.USAGE_TIME: request.POST.get(CONST.USAGE_TIME, "00.00.00"),
            CONST.UPLOAD: request.POST.get(CONST.UPLOAD, 0.0),
            CONST.DOWNLOAD: request.POST.get(CONST.DOWNLOAD, 0.0),
            "status": 200,
        }

        errors: list[str] = []

        self.__validate_username(data[CONST.USERNAME], CONST.USERNAME, errors)
        self.__validate_mac_address(data[CONST.MAC_ADDRESS], CONST.MAC_ADDRESS, errors)

        if errors.__len__() > 0:
            response["error"] = "[" + ", ".join(errors) + "]"
            response["status"] = 400
            return response

        return data

    def __validate_username(self, field: str, field_name: str, errors: list[str]) -> None:

        MIN_LEN = 4
        MAX_LEN = DataUsage._meta.get_field(field_name).max_length

        REGEX = "^[0-9]|[^a-zA-Z0-9]+"

        if field.__len__() == 0:
            errors.append("'" + field_name + "' cannot be empty.")
        if field.__len__() < 4 or field.__len__() > 50:
            errors.append(
                "'"
                + field_name
                + "' must contain atleast "
                + str(MIN_LEN)
                + " and maximum "
                + str(MAX_LEN)
                + " characters"
            )
        if re.search(REGEX, field) != None:
            errors.append(
                "'"
                + field_name
                + "' can only contain alphabets and numbers, and must start with a letter"
            )

    def __validate_mac_address(self, field: str, field_name: str, errors: list[str]) -> None:

        REGEX = "^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"

        if re.search(REGEX, field) == None:
            errors.append("Invalid MAC address")