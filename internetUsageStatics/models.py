from django.db import models

# Create your models here.
class DataUsage(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    mac_address = models.CharField(unique=True, null=False, max_length=17)
    start_time = models.DateTimeField(null=False)
    usage_time = models.TimeField()
    upload = models.FloatField(default=0)
    download = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.username


class DataUsageRouter:
    route_app_labels = ["internetUsageStatics"]
    route_db_label = "users"

    def db_for_read(self, model: models.base.ModelBase, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.route_db_label
        return False

    def db_for_wirte(self, model: models.base.ModelBase, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.route_db_label
        return False

    def allow_migrate(self, db: str, app_label: str, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == self.route_db_label
        return False
