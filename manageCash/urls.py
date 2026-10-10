from django.urls import path
from manageCash.views import *

urlpatterns = [
    path('', register_view, name = 'register_view'),
    path('login/', login_view, name = 'login_view'),
    path('dashboard/',dashboard_view,name="dashboard_view"),
    path('expense/',expense_view,name="expense_view"),
    path('addCash/',addCash_view,name="addCash_view"),
    path('logout/',logout_view,name="logout_view"),
    path('delete/<str:model_input>/<int:id>/', delete_view, name='delete_view'),
    path('edit/<str:model_input>/<int:id>/', edit_view, name='edit_view'),

]