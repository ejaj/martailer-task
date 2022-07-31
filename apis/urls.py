from django.urls import path, include
from apis.views import (
    HelloApiView
)

urlpatterns = [
    path('', HelloApiView.as_view(), name="hello"),
    path('youtube/videos', include('apis.youtube.urls'))
]
