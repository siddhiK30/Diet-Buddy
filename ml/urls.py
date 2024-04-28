from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('streamlit/', views.streamlit_view, name = 'streamlit_view'),
   # path('streamlit1/', views.streamlit_view2, name = 'streamlit_view')
]