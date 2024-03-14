from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone
from django.db.models import Count

from restaurant.serializers.restaurant import MenuSerializer
from restaurant.models import Menu


@api_view(['GET'])
def list_menu(request):
    """
    List all non-empty menu items with optional sorting and filtering.

    The better solution would be to use django-filter which would allow user to filter by any field and provides 
    much more flexibility to filtering by GET params. But in this particular assigment, with only 3 fields on mind 
    (filtering), I won't add whole python module just to achieve it. That is the simplest and fastest way to 
    filter 3 fields, but in more complex system I would definitively implement django-filter.

    Parameters:
    - sort_by: Sort the menu items by a field (e.g., 'name', 'num_dishes')
    - name: Filter menu items by name (case-insensitive)
    - start_created_dt: Filter menu items created after a certain date and time (format: 'YYYY-MM-DD HH:MM')
    - end_created_dt: Filter menu items created before a certain date and time (format: 'YYYY-MM-DD HH:MM')
    - start_updated_dt: Filter menu items updated after a certain date and time (format: 'YYYY-MM-DD HH:MM')
    - end_updated_dt: Filter menu items updated before a certain date and time (format: 'YYYY-MM-DD HH:MM')

    Example:
    /list_menu?sort_by=name&name=pizza&start_created_dt=2024-03-01%2012:00&end_created_dt=2024-03-14%2012:00
    """

    menu_items = Menu.objects.prefetch_related('dishes').annotate(
        num_dishes=Count('dishes')).filter(num_dishes__gt=0)

    sort_by = request.GET.get('sort_by', None)

    if sort_by:
        menu_items = menu_items.order_by(sort_by)

    name_filter = request.query_params.get('name', None)

    start_created_dt = request.query_params.get('start_created_dt', None)
    end_created_dt = request.query_params.get('end_created_dt', None)

    start_updated_dt = request.query_params.get('start_updated_dt', None)
    end_updated_dt = request.query_params.get('end_updated_dt', None)

    filter_params = {}

    filter_params.update({"name__icontains": name_filter}
                         ) if name_filter else None
    filter_params.update({"created_dt__gte": timezone.make_aware(datetime.strptime(start_created_dt, '%Y-%m-%d %H:%M'))}
                         ) if start_created_dt else None
    filter_params.update({"created_dt__lte": timezone.make_aware(datetime.strptime(end_created_dt, '%Y-%m-%d %H:%M'))}
                         ) if end_created_dt else None
    filter_params.update({"updated_dt__gte": timezone.make_aware(datetime.strptime(start_updated_dt, '%Y-%m-%d %H:%M'))}
                         ) if start_updated_dt else None
    filter_params.update({"updated_dt__lte": timezone.make_aware(datetime.strptime(end_updated_dt, '%Y-%m-%d %H:%M'))}
                         ) if end_updated_dt else None

    if filter_params:
        menu_items = menu_items.filter(**filter_params)

    serializer = MenuSerializer(menu_items, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
