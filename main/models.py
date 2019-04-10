from django.db import models
from django.utils import timezone

class Member(models.Model):
    card_id = models.CharField(max_length=64)
    name = models.CharField(max_length=32)
    atd_checked = models.IntegerField(default=1)
    last_checked = models.DateTimeField(default=timezone.now)
    
    def atd_check(self):
        self.atd_checked = self.atd_checked + 1
        self.last_checked = timezone.now()
        self.save()

    def __str__(self):
        return self.name