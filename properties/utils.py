from django.core.cache import cache
from .models import Property

CACHE_KEY = "all_properties"
CACHE_TIMEOUT = 60 * 15  # 15 minutes


def get_all_properties():
    """
    Fetch all properties from Redis if available.
    Otherwise query the database, cache the result, and return it.
    """

    properties = cache.get(CACHE_KEY)

    if properties is None:
        # Serialize safely
        properties = list(
            Property.objects.all().values(
                "id",
                "title",
                "price",
                "location",
                "created_at",
            )
        )
        cache.set(CACHE_KEY, properties, CACHE_TIMEOUT)

    return properties
