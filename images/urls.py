from django.urls import path
from .views import upload_image_view, image_detail_view

urlpatterns = [
    path('upload/', upload_image_view, name='upload'),
    path('detail/<int:id>/<slug:slug>/', image_detail_view, name='image_detail'),
]

