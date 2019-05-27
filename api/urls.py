from django.conf.urls import include, url
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
# app_name = 'api'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url('', include(router.urls)),
    url('external-books/', views.BooksList.as_view(), name='external_books'),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('v1/', include('api.v1.urls', namespace='v1'))
]
