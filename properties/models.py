from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    # max_digits=10 allows values up to 99,999,999.99
    price = models.DecimalField(max_digits=10, decimal_places=2)

    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ["-created_at"]  # Latest properties appear first

    def __str__(self):
        return self.title
