from django.urls import path
from . import views
urlpatterns = [
    path('doctor/',views.get_add_doctor,name='get_add_doctor'),
    path('doctor/<int:doctor_id>/patients/',views.get_doctor_patients,name='get_update_delete_doctor'),
]