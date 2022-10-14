from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_customer_from_id, get_salesman_from_id, get_chart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

@login_required
def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    no_data = None

    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

        sale_qs = Sale.objects.filter(created__date__gte= date_from ,created__date__lte= date_to)
        print(len(sale_qs))
        if len(sale_qs) > 0:
            sales_df = pd.DataFrame(sale_qs.values())

            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created'] = sales_df['created'].apply(lambda x: x.strftime('%Y-%m-%d'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x: x.strftime('%Y-%m-%d'))

            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)

            positions_data = []
            for sale in sale_qs:
                for pos in sale.get_positions():
                    obj = {
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                        'sales_id': pos.get_sales_id(sale.salesman),
                    }
                    positions_data.append(obj)
                    

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            merged_df.drop('total_price',axis=1,inplace=True)

            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')
            df.rename({'price':'Total_Price'},axis=1,inplace=True)
            
            chart = get_chart(chart_type, sales_df, results_by)
            #print('chart', chart)
            sales_df = sales_df.to_html(classes='table table-striped text-center', justify='center')
            positions_df = positions_df.to_html(classes='table table-striped text-center', justify='center')
            merged_df = merged_df.to_html(classes='table table-striped text-center', justify='center')
            df = df.to_html(classes='table table-striped text-center', justify='center')

        else: 
            no_data = 'No data is available in this date range'


    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'no_data': no_data,
    }
    return render(request, 'sales/home.html', context)

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/detail.html'

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@csrf_exempt
def to_csv(request):
    if is_ajax(request):
        data=request.POST.get('data')
        data1=pd.read_html(data,index_col=0)
        # data1=pd.read_html(data,index_col=0)   ==> return list
        # data1=pd.read_html(data,index_col=0)[0] ==> return DataFrame object

        data1[0].to_csv(r'C:\Users\Shaam\Desktop\export.csv')  # with other applicable parameters
        return JsonResponse({})
    return JsonResponse({})
    
 
