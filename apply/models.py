from django.conf import settings
from django.db import models


class Application(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
        null=True,
        blank=True,
    )
    character_name = models.CharField(max_length=100)
    discord_id = models.CharField(max_length=100, unique=True)
    rank_id = models.CharField(max_length=100)
    chase_handling = models.TextField()
    vehicle_experience = models.TextField()
    apply_reasons = models.TextField()
    unit_tasks = models.TextField()
    vehicle_deploy = models.TextField()
    chase_scenario = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.character_name
