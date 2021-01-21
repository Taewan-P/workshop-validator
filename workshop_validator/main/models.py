from django.db import models


# Create your models here.
class Member(models.Model):
    username = models.CharField(max_length=50)
    q1 = models.BooleanField(default=False)
    q2 = models.BooleanField(default=False)
    q3 = models.BooleanField(default=False)
    q4 = models.BooleanField(default=False)
    q5 = models.BooleanField(default=False)
    q6 = models.BooleanField(default=False)
    q7 = models.BooleanField(default=False)
    q8 = models.BooleanField(default=False)
    q9 = models.BooleanField(default=False)
    q10 = models.BooleanField(default=False)

    def __str__(self):
        return self.username
