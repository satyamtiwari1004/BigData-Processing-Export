import logging
from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Location
from .serializers import AccountSerializer, LocationSerializer
from django.db.models import Sum, Avg, Count
from django.db.models.functions import ExtractYear
from django.http import HttpResponse
import pandas as pd
from datetime import datetime
from django.core.paginator import Paginator

logger = logging.getLogger('dashboard_app')

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'status']
    search_fields = ['account_number']

    def get_queryset(self):
        logger.info(f"Fetching accounts with filters: {self.request.query_params}")
        return super().get_queryset()

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        logger.info(f"Fetching locations with filters: {self.request.query_params}")
        return super().get_queryset()

def dashboard(request):
    logger.info(f"Accessing dashboard with parameters: {request.GET}")
    
    # Get filter parameters
    location = request.GET.get('location')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page = request.GET.get('page', 1)
    page_size = int(request.GET.get('page_size', 100))  # Default to 100 records per page

    # Base queryset
    accounts = Account.objects.all()
    locations = Location.objects.all()

    # Log initial counts
    logger.info(f"Total accounts in database: {Account.objects.count()}")
    logger.info(f"Total locations in database: {Location.objects.count()}")
    logger.info(f"Initial accounts queryset count: {accounts.count()}")

    # Apply filters
    if location and location != 'ALL':
        logger.debug(f"Filtering by location: {location}")
        accounts = accounts.filter(location=location)
        logger.debug(f"Accounts count after location filter: {accounts.count()}")
    if start_date:
        logger.debug(f"Filtering by start date: {start_date}")
        accounts = accounts.filter(opening_date__gte=start_date)
        logger.debug(f"Accounts count after start date filter: {accounts.count()}")
    if end_date:
        logger.debug(f"Filtering by end date: {end_date}")
        accounts = accounts.filter(opening_date__lte=end_date)
        logger.debug(f"Accounts count after end date filter: {accounts.count()}")

    # Get statistics
    total_accounts = accounts.count()
    total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
    avg_balance = accounts.aggregate(avg=Avg('balance'))['avg'] or 0

    logger.info(f"Dashboard statistics - Total accounts: {total_accounts}, Total balance: {total_balance}, Avg balance: {avg_balance}")

    # Get yearly statistics
    yearly_stats = list(accounts.annotate(
        year=ExtractYear('opening_date')
    ).values('year').annotate(
        total=Sum('balance'),
        count=Count('id')
    ).order_by('year'))
    logger.info(f"Raw yearly stats: {yearly_stats}")

    # Get location-wise distribution
    location_dist = list(accounts.values('location__name').annotate(
        count=Count('id'),
        total=Sum('balance')
    ))
    logger.info(f"Raw location distribution: {location_dist}")

    # Convert to JSON-serializable format
    try:
        yearly_stats = [{'year': str(item['year']), 'total': float(item['total'] or 0), 'count': int(item['count'])} for item in yearly_stats]
        logger.info(f"Processed yearly stats: {yearly_stats}")
    except Exception as e:
        logger.error(f"Error processing yearly stats: {str(e)}")
        yearly_stats = []

    try:
        location_dist = [{'location__name': item['location__name'] or 'Unknown', 'count': int(item['count']), 'total': float(item['total'] or 0)} for item in location_dist]
        logger.info(f"Processed location distribution: {location_dist}")
    except Exception as e:
        logger.error(f"Error processing location distribution: {str(e)}")
        location_dist = []

    # Paginate accounts
    paginator = Paginator(accounts, page_size)
    try:
        paginated_accounts = paginator.page(page)
    except:
        paginated_accounts = paginator.page(1)

    # Log the final context data
    logger.info("Preparing context with processed data")
    context = {
        'total_accounts': total_accounts,
        'total_balance': total_balance,
        'avg_balance': avg_balance,
        'yearly_stats': yearly_stats,
        'location_dist': location_dist,
        'locations': locations,
        'accounts': paginated_accounts,
        'page_size': page_size,
        'page_size_options': [50, 100, 200, 500, 1000],
    }
    logger.info(f"Context prepared with {len(yearly_stats)} yearly stats and {len(location_dist)} location entries")
    return render(request, 'dashboard_app/dashboard.html', context)

def export_data(request):
    logger.info(f"Exporting data with parameters: {request.GET}")
    
    # Get filter parameters
    location = request.GET.get('location')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Base queryset
    accounts = Account.objects.all()

    # Apply filters
    if location and location != 'ALL':
        logger.debug(f"Filtering export by location: {location}")
        accounts = accounts.filter(location=location)
    if start_date:
        logger.debug(f"Filtering export by start date: {start_date}")
        accounts = accounts.filter(opening_date__gte=start_date)
    if end_date:
        logger.debug(f"Filtering export by end date: {end_date}")
        accounts = accounts.filter(opening_date__lte=end_date)

    # Log the number of records being exported
    logger.info(f"Exporting {accounts.count()} filtered records")

    # Convert to DataFrame
    data = list(accounts.values(
        'account_number',
        'location__name',
        'opening_date',
        'closing_date',
        'balance',
        'status'
    ))
    df = pd.DataFrame(data)

    # Create Excel file
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=accounts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    # Write to Excel
    df.to_excel(response, index=False)
    return response
