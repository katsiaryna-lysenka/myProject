from django.urls import path
from .views import (
    OrganizationListCreateView,
    OrganizationDetailView,
    UserProfileListCreateView,
    UserProfileDetailView,
    Form1ListCreateView,
    Form1DetailView,
    Form2ListCreateView,
    Form2DetailView,
    Form3ListCreateView,
    Form3DetailView,
    ExportExcelView
)

urlpatterns = [
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('userprofiles/', UserProfileListCreateView.as_view(), name='userprofile-list-create'),
    path('userprofiles/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile-detail'),
    path('form1/', Form1ListCreateView.as_view(), name='form1-list-create'),
    path('form1/<int:pk>/', Form1DetailView.as_view(), name='form1-detail'),
    path('form2/', Form2ListCreateView.as_view(), name='form2-list-create'),
    path('form2/<int:pk>/', Form2DetailView.as_view(), name='form2-detail'),
    path('form3/', Form3ListCreateView.as_view(), name='form3-list-create'),
    path('form3/<int:pk>/', Form3DetailView.as_view(), name='form3-detail'),
    path('export/excel/', ExportExcelView.as_view(), name='export-excel'),
]
