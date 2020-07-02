from django.db import models
from login.models import User

# Create your models here.
class Error(models.Model):
    CATEGORY_CHOICES = (
        ('PRODUÇÃO', 'Produção'),
        ('HOMOLOGAÇÃO', 'Homologação'),
        ('DEV', 'Dev')
    )
    LEVEL_CHOICES = (
        ('ERROR', 'Error'),
        ('WARNING', 'Warning'),
        ('DEBUG', 'Debug')
    )
    
    title       = models.TextField(max_length=50, blank=False)
    category    = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    level       = models.CharField(max_length=16, choices=LEVEL_CHOICES)
    archived    = models.BooleanField(default=False)
    description = models.TextField()
    address     = models.GenericIPAddressField(max_length=39, protocol='IPv4', null=True)
    date        = models.DateTimeField(auto_now_add= True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' +str(self.pk) + ' - ' + str(self.user)