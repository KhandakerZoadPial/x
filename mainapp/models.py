from django.db import models

# Create your models here.
class Classes(models.Model):
    cls_name = models.TextField()
    ownedby = models.TextField()
    clsCode = models.TextField()


class Submit(models.Model):
    stu_id = models.CharField(max_length=20)
    cls_name = models.TextField()
    ownedby = models.TextField()


class MutualTable(models.Model):
    cls_name = models.TextField()
    ownedby = models.TextField()
    is_active = models.BooleanField(default=True)

