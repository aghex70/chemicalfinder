from django.urls import path

from . import views

urlpatterns = [
    path('patent/', views.PatentParserViewSet.as_view({
        'post': 'create',
        'get': 'list',
    }), name='patents'),
    path('ner/', views.NERViewSet.as_view({
        'get': 'list',
        'post': 'create_ner',
        'delete': 'destroy_ner',
    }), name='ner'),
    path('ner/train/', views.NERViewSet.as_view({
        'post': 'train',
    }), name='train_ner'),
    path('chemner/', views.NERViewSet.as_view({
        'post': 'create_chemner',
        'delete': 'destroy_chemner',
    }), name='chemner'),
    path('trained_ner/', views.NERViewSet.as_view({
        'post': 'create_trained_ner',
        'delete': 'destroy_trained_ner',
    }), name='chemner'),
    path('database/', views.BaseViewSet.as_view({
        'delete': 'wipe_database',
    }), name='wipe_database'),
    path('inventor/', views.InventorViewSet.as_view({
        'get': 'list',
    }), name='inventors'),
]

