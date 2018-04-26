from django.conf.urls import url

from apps.ycharts.views import YChartsAPIView

urlpatterns = [
    url('', YChartsAPIView.as_view(), name='ycharts'),
]