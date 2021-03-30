from django.urls.conf import path

from main import views


app_name = "main"  # pylint: disable=invalid-name


urlpatterns = [  # pylint: disable=invalid-name
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('find/user/<str:email>/', views.UserRetrieveView.as_view(), name='find_user'),
    path('risk-type/add/', views.RiskTypeView.as_view(), name='add_risk_type'),
    path('risk-type/<uuid:user_id>/fetch/', views.AllRiskTypeRetrieveView.as_view(), name='fetch_all_risk_type'),
    path(
        'risk-type/<uuid:id>/fetch/single/',
        views.RiskTypeRetrieveView.as_view(),
        name='fetch_single_risk_type'
    ),
    path(
        'risk-type/<uuid:id>/update/single/',
        views.RiskTypeRetrieveUpdateView.as_view(),
        name='update_single_risk_type'
    ),
    path('field/add/', views.FieldView.as_view(), name='add_field'),
    path('field/fetch/all/', views.AllFieldRetrieveView.as_view(), name='fetch_all_field'),
    path('risk/add/', views.RiskView.as_view(), name='add_risk'),
    path('risk/<uuid:user_id>/fetch/', views.AllRiskRetrieveView.as_view(), name='fetch_all_risk'),
    path(
        'risk/<uuid:id>/fetch/single/',
        views.RiskRetrieveView.as_view(),
        name='fetch_single_risk'
    ),
    path(
        'risk/<uuid:id>/update/single/',
        views.RiskRetrieveUpdateView.as_view(),
        name='update_single_risk'
    ),
]
