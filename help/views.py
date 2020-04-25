from django.views import generic


class HomeView(generic.TemplateView):
    template_name = 'help/home.html'


class NoticeListView(generic.TemplateView):
    template_name = 'help/notice_list.html'


class NoticeDetailView(generic.TemplateView):
    template_name = 'help/notice_detail.html'


class FaqListView(generic.TemplateView):
    template_name = 'help/faq_list.html'


class CustomerQuestionListView(generic.TemplateView):
    template_name = 'help/question_list.html'


class CustomerQuestionDetailView(generic.TemplateView):
    template_name = 'help/question_detail.html'


class CustomerQuestionCreateView(generic.TemplateView):
    template_name = 'help/question_create.html'


class CustomerQuestionCreateOrderView(generic.TemplateView):
    template_name = 'help/question_create.html'


class TestimonialsListView(generic.TemplateView):
    template_name = 'help/testimonials_list.html'


class TestimonialsDetailView(generic.TemplateView):
    template_name = 'help/testimonials_detail.html'


class TestimonialsCreateView(generic.TemplateView):
    template_name = 'help/testimonials_create.html'


class TestimonialsAnswerView(generic.TemplateView):
    template_name = 'help/testimonials_answer.html'


class GuideView(generic.TemplateView):
    template_name = 'help/guide.html'


class AboutView(generic.TemplateView):
    template_name = 'help/about.html'


class TermsView(generic.TemplateView):
    template_name = 'help/terms.html'


class PrivacyView(generic.TemplateView):
    template_name = 'help/privacy.html'
