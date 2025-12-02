from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan_name}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - ${self.amount}"

import uuid

# ... your existing models (Transaction, Subscription) are above ...

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    # This generates a unique code like "8f32-12a..."
    certificate_id = models.CharField(max_length=20, unique=True, editable=False)
    date_issued = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            # Generate a short unique ID (e.g., TSB-1234AB)
            uid = str(uuid.uuid4())[:8].upper()
            self.certificate_id = f"TSB-{uid}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.certificate_id}"
