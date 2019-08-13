from django.urls import path

from keyword_meter.views.response import import_to_database, check_database_with_each_algorithm, rollback_response, \
    reset_all

urlpatterns = [
    # it just works in local
    path('import/', import_to_database, name='import_to_database'),

    path('run/', check_database_with_each_algorithm, name='check_database_with_each_algorithm'),

    path('run/all/<int:number>/', reset_all, name='reset_all'),

]


