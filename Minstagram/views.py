from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self, request):
        print("get 으로 호출")
        return render(request, "Minstagram/main.html")

    def post(self, request):
        print("post 으로 호출")
        return render(request, "Minstagram/main.html")