from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AIChatView, UserViewSet, TransactionViewSet, SubscriptionViewSet, chat_interface
router = DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'subscriptions', views.SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chat-ui/', chat_interface),
    path('chat/', views.AIChatView.as_view()),
]
