from django.urls import path

from . import views

app_name = 'help'

urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),

    path('notice/',
         views.NoticeListView.as_view(), name='notice-list'),

    path('notice/<int:pk>/',
         views.NoticeDetailView.as_view(), name='notice-detail'),

    path('faq/',
         views.FaqListView.as_view(), name='faq-list'),

    path('qna/',
         views.CustomerQuestionListView.as_view(), name='question-list'),

    path('qna/<int:pk>/',
         views.CustomerQuestionDetailView.as_view(), name='question-detail'),

    path('qna/create/',
         views.CustomerQuestionCreateView.as_view(), name='question-create'),

    path('qna/create/<uuid:uuid>/',
         views.CustomerQuestionCreateOrderView.as_view(), name='question-create-order'),

    path('testimonials/',
         views.TestimonialsListView.as_view(), name='testimonials-list'),

    path('testimonials/<int:pk>/',
         views.TestimonialsDetailView.as_view(), name='testimonials-detail'),

    path('testimonials/create/',
         views.TestimonialsCreateView.as_view(), name='testimonials-create'),

    path('testimonials/<int:pk>/answer',
         views.TestimonialsAnswerView.as_view(), name='testimonials-answer'),

    path('guide/',
         views.GuideView.as_view(), name='guide'),

    path('about/',
         views.AboutView.as_view(), name='about'),

    path('terms/',
         views.TermsView.as_view(), name='terms'),

    path('privacy/',
         views.PrivacyView.as_view(), name='privacy'),
]
