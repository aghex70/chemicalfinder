from django.urls import path

from . import views
urlpatterns = [
    path('patents/generate/', views.PatentParserViewSet.as_view({
        'post': 'create',
    }), name='generate_patents'),
    path('patents/', views.PatentParserViewSet.as_view({
        'get': 'list',
    }), name='patents'),
    path('ner/', views.NERViewSet.as_view({
        'get': 'list',
    }), name='training'),
    path('ner/train/', views.TrainedNERViewSet.as_view({
        'post': 'train',
    }), name='training'),
    # path('ner/train/', views.TrainedNERViewSet.as_view({
    #     'post': 'train',
    # }), name='training'),
    path('trained_ner/', views.TrainedNERViewSet.as_view({
        'post': 'create',
    }), name='create'),
]

