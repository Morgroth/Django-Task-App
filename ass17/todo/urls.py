from unicodedata import name
from django.urls import path

from . import views





app_name='todo'
urlpatterns = [
    path('',views.sign_in, name='login_page'),
    path('register', views.sign_up, name='sign_up'),
    path('success', views.SuccessView.as_view(),name='success' ),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<email>/add_task/',views.add_task, name='add_task'),
    path('<email>/edit_task',views.edit_task, name='edit_task'),
    path('<email>/dashboard/<date>', views.task_date, name='task_date'),
    path('<email>/date', views.date_handler, name='date_handler'),
    path('logout',views.logout_view, name='logout_page')
]

