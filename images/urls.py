from django.urls import path
from .views import upload_image_view, image_detail_view, like_image_view, image_list_view

urlpatterns = [
    path('', image_list_view, name='image_list'),
    path('upload/', upload_image_view, name='upload'),
    path('detail/<int:id>/<slug:slug>/', image_detail_view, name='image_detail'),
    path('like/', like_image_view, name='like_image'),
]

