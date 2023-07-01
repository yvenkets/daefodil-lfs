from django.urls import include, path
from . import views
from API.views import SubmitFormView

urlpatterns = [
    # path('submitform/', views.submitform, name='submitform'),
    # path('upload/', FileUploadView.as_view(), name='file_upload'),
    # path('my-api/', MyAPI.as_view()),
    path('submitform/', SubmitFormView.as_view()),
    # path('submitform/', submitform, name='submitform'),
]