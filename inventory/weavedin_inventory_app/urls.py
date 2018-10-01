from django.conf.urls import url
from app import urls

from weavedin_inventory_app import views as handler
"""
API endpoints for accessing the website for Blockwala Bitcoin Explorer.
"""
urlpatterns = [
#url(r'^base_view/$',views_ui_front.base_view,name='base_view'),
url(r'^createItemEntry/$', handler.create_item_entry,name='create_item_entry'),
]
