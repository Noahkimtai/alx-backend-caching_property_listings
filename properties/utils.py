def getallproperties():
    """
    Checks Redis for all_properties using cache.get('all_properties').
    FetchesProperty.objects.all() if not found.
    Stores the queryset in Redis with cache.set('all_properties', queryset, 3600).
    Returns the queryset.
    Update property_list to useget_all_properties().
    """
