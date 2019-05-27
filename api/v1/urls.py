from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api.v1.views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, base_name='books')

urlpatterns = [
    url(r'^', include(router.urls)),

]
