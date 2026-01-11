from django.core.cache import cache
import logging
from django_redis import get_redis_connection

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

        # cache.set("all_properties", Property.objects.all(), 3600) # BAD Why?

        # QuerySets hold DB connections

        # Not JSON-serializable

        # Can raise pickle/connection errors

        # Causes subtle bugs in production

    return properties


logger = logging.getLogger(__name__)


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ration.
    """

    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total = hits + misses

        hit_ratio = (hits / total) if total > 0 else 0

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 4),
        }

        logger.info(
            "Redis cache metrics | hits=%s misses=%s hit_ratio=%.4f",
            hits,
            misses,
            hit_ratio,
        )

        return metrics

    except Exception as e:
        logger.error("Failed to retrieve Redis cache metrics: %s", e)
        logger.exception("Failed to retrieve Redis cache metrics: %s", e)
        return {
            "kespace_hits": 0,
            "kespace_misses": 0,
            "hit_ratio": 0.0,
            "error": str(e),
        }


# get_redis_cache_metrics()
