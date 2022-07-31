from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import views


class HelloApiView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
