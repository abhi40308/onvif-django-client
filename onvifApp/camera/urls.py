from django.conf.urls import url
from .views import(CameraView, CameraLoginView)

urlpatterns = [

		url(r'^(?P<id>[^\.]+)/$', CameraView.as_view(), 
			name = "camera_detail"),
		url(r'^$', CameraLoginView.as_view(), 
			name = "camera_login"),
]