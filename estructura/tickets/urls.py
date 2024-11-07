"""
URL configuration for estructura project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path("",views.ticket_list,name="ticket_list"),
    path("add/",views.add_ticket,name="addTicket"),
    path("current/",views.current_ticket,name="current_ticket"),
    path("sorted/",views.list_tickets,name="list_tickets"),
    path("search/", views.search_ticket_page, name="search_ticket_page"),
    path('eliminar_ticket/<int:ticket_id>/', views.eliminar_ticket, name='eliminar_ticket'),
    path('eliminar_ticket_confirmar/<int:ticket_id>/', views.eliminar_ticket_confirmar, name='eliminar_ticket_confirmar'),
    path('reset-id/', views.reset_id, name='reset_id'),
    path("search_ticket/", views.search_ticket, name="search_ticket"),
    path('download_tickets/<str:tipo>/', views.download_tickets, name='download_tickets'),
     path('upload_csv/', views.upload_csv, name='upload_csv'),
]
