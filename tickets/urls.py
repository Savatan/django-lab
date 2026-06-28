from django.urls import path
from . import views, api

app_name = 'tickets'

urlpatterns = [
    # Веб-интерфейс
    path('tickets/', views.ticket_list, name='list'),
    path('tickets/new/', views.ticket_create, name='create'),
    path('tickets/<int:pk>/', views.ticket_detail, name='detail'),
    path('tickets/<int:pk>/edit/', views.ticket_edit, name='edit'),
    path('tickets/<int:pk>/delete/', views.ticket_delete, name='delete'),
    path('moderator/', views.moderator_panel, name='moderator'),

    # REST API
    path('api/tickets/', api.api_tickets, name='api_tickets'),
    path('api/tickets/<int:pk>/', api.api_ticket_detail, name='api_ticket_detail'),
    path('api/tickets/<int:pk>/comments/', api.api_ticket_comments, name='api_ticket_comments'),
]
