from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# --- THE ROLES ---
ROLE_CHOICES = (
    ('CLIENT', 'Client'),
    ('FREELANCER', 'Freelancer'),
    ('ADMIN', 'Admin'),
)

# --- TABLE 1: THE USERS ---
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True) 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CLIENT')
    is_verified = models.BooleanField(default=False)
    paystack_customer_code = models.CharField(max_length=100, blank=True, null=True)
    paystack_subaccount_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.email} ({self.role})"

# --- TABLE 2: SUBSCRIPTIONS ---
class Subscription(models.Model):
    PLAN_CHOICES = (('FREE', 'Free Tier'), ('PRO', 'Pro - R150/m'),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='FREE')
    is_active = models.BooleanField(default=True)
    paystack_auth_token = models.CharField(max_length=255, blank=True, null=True)
    next_billing_date = models.DateTimeField(null=True, blank=True)

# --- TABLE 3: TRANSACTIONS ---
class Transaction(models.Model):
    TYPE_CHOICES = (('SUBSCRIPTION', 'Sub Fee'), ('GIG_PAYMENT', 'Gig Payment'),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount_in_cents = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, default='PENDING')
    paystack_reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
