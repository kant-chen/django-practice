from django.db import models


class Base(models.Model):
    """
    This is the abstract base model to be inherited by all other models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
