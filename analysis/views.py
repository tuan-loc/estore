from django.shortcuts import render
from django.conf import settings
from analysis.utils import *
import pandas as pd
import numpy as np
import os
import io



# Create your views here.
def work_with_series(request):
    # Tạo series
    views1 = pd.Series([90006, 101141, 97297, 117182, 99637])
    views1 = pd.DataFrame({'views': views1})
    views1 = views1.to_html()

    # Tạo series có index
    likes = pd.Series([402, 389, 403, 397, 404], index=['c1', 'c2', 'c3', 'c4', 'c5'])
    likes_df = pd.DataFrame({'views': likes})
    likes1 = likes_df.to_html()

    # ánh xạ từ likes
    double_likes = likes.map(lambda x: x * 2)
    double_likes = pd.DataFrame({'double_likes': double_likes})
    double_likes = double_likes.to_html()

    # đọc tập tin
    views2 = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'analysis/data_views.csv'), squeeze=True)
    views2 = pd.DataFrame({'views': views2})
    headviews2 = views2.head().to_html()
    tailviews2 = views2.tail().to_html()

    # chiều dài series
    len_views2 = len(views2)

    # thống kê chung
    stats = likes.describe()
    stats_df = pd.DataFrame(stats)
    stats_html = stats_df.to_html()

    return render(request, 'analysis/series.html', {
        'views1': views1,
        'likes1': likes1,
        'double_likes': double_likes,
        'headviews2': headviews2,
        'tailviews2': tailviews2,
        'len_views2': len_views2,
        'stats_html': stats_html,
    })


def work_with_dataframe(request):
    # tao dataframe
    views_likes = np.array([[90006, 402], [101141, 389],
                            [97297, 403], [117182, 397]])
    df_views_likes = pd.DataFrame(views_likes,
                                  columns=["views", "likes"])
    df_views_likes_html = df_views_likes.to_html()

    dic_views_like = {"views": [90006, 101141, 97297, 117182],
                      "likes": [402, 389, 403, 397]}
    df2_views_likes = pd.DataFrame(dic_views_like)

    # lay cot views tu dataframe
    get_views = df_views_likes[['views']].to_html()
    # them cot share tu dataframe
    df_views_likes['shared'] = pd.Series([20, 18, 19, 17])
    df_views_likes_now = df_views_likes.to_html()

    # cap nhat index cho dataframe
    df_views_likes.index = ["04/2020", "05/2020", "06/2020", "07/2020"]
    df_views_likes_stridx = df_views_likes.to_html()

    # tao dataframe tu du lieu lay tu tap tin
    data = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'analysis/data.csv'), header=0)
    buf = io.StringIO()
    # print(buf)
    data.info(buf=buf)
    data_info = "<p>" + buf.getvalue().replace("\n", "<br>") + "</p>"
    data_head = data.head().to_html()
    data_tail = data.tail().to_html()
    data_shape = str(data.shape)

    # thống kê chung
    stats = data.describe(include='all')
    stats_df = pd.DataFrame(stats)
    stats_html = stats_df.to_html()

    # products
    products = pd.DataFrame({
                            'category': ['furniture', 'furniture', 'furniture', 'electronic device', 'furniture', 'electronic device', 'electronic device'],
                            'product': ['table', 'chair', 'chair', 'mobile phone', 'table', 'mobile phone', 'tablet'],
                            'value': [20.45, 22.89, 32.12, 111.22, 33.22, 100.00, 99.99],
                            })
    products_html = products.to_html()

    # group by
    product_count_html = pd.DataFrame(
        products.groupby('product').size()).to_html()
    product_count_sum_html = pd.DataFrame(products.groupby(
        ['category', 'product']).agg({'value': ['sum', 'count']})).to_html()

    # pivot
    pivot2 = pd.pivot_table(products, values='value', index=['product'], columns=['category'], aggfunc=['count', 'sum'])
    pivot2_html = pivot2.to_html()
    return render(request, "analysis/dataframe.html", {
        'df_views_likes_html': df_views_likes_html,
        'data_info': data_info,
        'data_head': data_head,
        'data_tail': data_tail,
        'data_shape': data_shape,
        'get_views': get_views,
        'df_views_likes_now': df_views_likes_now,
        'df_views_likes_stridx': df_views_likes_stridx,
        'stats_html': stats_html,
        'products_html': products_html,
        'product_count_html': product_count_html,
        'product_count_sum_html': product_count_sum_html,
        'pivot2_html': pivot2_html,
    })

def work_with_chart_1(request):
    # histogram
    data_second = pd.read_excel(os.path.join(
        settings.MEDIA_ROOT, 'analysis/dataset.xlsx'), sheet_name='Wait_times')
    hist = get_hist(data_second, 'seconds', "Customer Wait Time")

    # boxplot
    data_salary = pd.read_excel(os.path.join(
        settings.MEDIA_ROOT, 'analysis/salaries.xlsx'))
    box = get_box(data_salary, 'salary', 'Salary')

    # barchart
    data_activiry = pd.read_excel(os.path.join(
        settings.MEDIA_ROOT, 'analysis/dataset.xlsx'), sheet_name='Activity')
    bar = get_bar(data_activiry, 'Activity',
                  'Number_of_Students', "After-School Activities")

    # lineplot
    water_consumption = pd.DataFrame({'m_3': [11, 13, 10, 14, 12, 12, 9, 10, 12, 15, 10, 14]},
                                     index=['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06',
                                            '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12'])
    line = get_plot(water_consumption, "Water Consumption 2020")

    # pie chart
    df = pd.DataFrame(
        {
            'Name': ['Hillary Clinton', 'Donald Trump', 'Others'],
            'Virginia': [1981473, 1769443, 233715],
            'Maryland': [1677928, 943169, 160349],
            'West Virginia': [188794, 489371, 36258],
        }
    )
    df['Total'] = df['Virginia'] + df['Maryland'] + df['West Virginia']
    pie = get_pie(df.Total, df.Name, 'Presidential Election Results')

    # scatter plot & regplot
    scatter = get_scatter(data_salary, 'years', 'salary', 'Years vs. Salary')

    return render(request, "analysis/chart.html", {
        'hist': hist,
        'box': box,
        'bar': bar,
        'line': line,
        'pie': pie,
        'scatter': scatter
    })
