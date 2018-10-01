from django.conf.urls import url

from weavedin_inventory_app import api as handler
"""
API endpoints for accessing the website for Blockwala Bitcoin Explorer.
"""
urlpatterns = [
    url(r'^createStoreEntry', handler.create_store_entry, name='create_store_entry'),
    url(r'^createBranchEntry', handler.create_branch_entry, name='create_branch_entry'),
    url(r'^createItemEntry', handler.create_item_entry, name='create_item_entry'),
    url(r'^getItem', handler.get_item, name='get_item'),
    url(r'^create_variant_entry', handler.create_variant_entry, name='create_variant_entry'),
    url(r'^get_variants', handler.get_variants, name='get_variants'),
    url(r'^edit_variants', handler.edit_variants, name='edit_variants'),
    url(r'^edit_items', handler.edit_items, name='edit_items'),
    url(r'^getLogs', handler.get_logs, name='get_logs'),
]
