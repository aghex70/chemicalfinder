from django.urls import path

from . import views
urlpatterns = [
    # path('agppatents/generate/', views.AGPPatentViewSet.as_view({
    #     'post': 'create',
    # }), name='generate_agppatents_ner'),
    # path('agppatents/chemner/generate/', views.AGPPatentViewSet.as_view({
    #     'post': 'create_chemner',
    # }), name='generate_agppatents_chemner'),
    # path('agppatents/trained_ner/generate/', views.AGPPatentViewSet.as_view({
    #     'post': 'create_trained_ner',
    # }), name='generate_agppatents_trained_ner'),
    # path('agppatents/ner_train/', views.AGPPatentViewSet.as_view({
    #     'post': 'train',
    # }), name='train_ner'),





    path('patents/generate/', views.PatentParserViewSet.as_view({
        'post': 'create',
    }), name='generate_patents'),
    path('patents/', views.PatentParserViewSet.as_view({
        'get': 'list',
    }), name='patents'),


    path('ner/train/', views.TrainedNERViewSet.as_view({
        'post': 'train',
    }), name='training'),
    path('trained_ner/', views.TrainedNERViewSet.as_view({
        'post': 'create',
    }), name='create'),
]

