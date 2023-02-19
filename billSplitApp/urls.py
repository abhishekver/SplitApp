"""billSplitApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from billSplitApp.api.view.group.create_group import CreateGroupAPIView, AddMembersInGroupAPIView
from billSplitApp.api.view.group.view_group import ViewGroupAPIView, ViewGroupBalanceSheetAPIView, \
    ViewGroupTransactionsAPIView
from billSplitApp.api.view.transaction.create_transaction import CreateTransactionAPIView, SettleBalanceSheetAPIView
from billSplitApp.api.view.transaction.view_transaction import ViewTransactionAPIView
from billSplitApp.api.view.user.create_user import CreateUserAPIView
from billSplitApp.api.view.user.view_user import ListUserAPIView, ListUserBalanceSheetAPIView

user_urls = [
    path('create/', CreateUserAPIView.as_view()),
    path('view/<user_id>/', ListUserAPIView.as_view()),
    path('view/<user_id>/balance_sheet', ListUserBalanceSheetAPIView.as_view()),
]

transaction_urls = [
    path('create/', CreateTransactionAPIView.as_view()),
    path('settle_balance/', SettleBalanceSheetAPIView.as_view()),
    path('view/<transaction_id>/', ViewTransactionAPIView.as_view()),
]

group_urls = [
    path('create/', CreateGroupAPIView.as_view()),
    path('view/<group_id>/', ViewGroupAPIView.as_view()),
    path('add_members/', AddMembersInGroupAPIView.as_view()),
    path('view/<group_id>/balance_sheet', ViewGroupBalanceSheetAPIView.as_view()),
    path('view/<group_id>/transactions', ViewGroupTransactionsAPIView.as_view()),
]

api_urls = [
    path('user/', include(user_urls)),
    path('transaction/', include(transaction_urls)),
    path('group/', include(group_urls)),
]


urlpatterns = [
    path('api/', include(api_urls)),
    path('admin/', admin.site.urls),
    path('view-auth/', include('rest_framework.urls'))
]
