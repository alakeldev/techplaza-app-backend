from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def welcome_view(request):
    return JsonResponse({"message": "Welcome to Techplaza API"})
