from django.http import JsonResponse

def hello(request):
    data = {"message": "Hello, Auth"}
    return JsonResponse(data)
