from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import  SignInViaUsernameForm
# from core.models import ArticleContext;
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.http import HttpResponse
from authentication.forms import ArticleContextForm;


class ChangeLanguageView(TemplateView):
    template_name = 'change_language.html'


#登录界面需要
class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            # context = {'form': View}
            # return render(request, 'accounts/log_in.html')
            # return redirect("accounts/index");

            name = request.GET.get("name")
            return render(request, "accounts/index.html", {"name": name})

        return super().dispatch(request, *args, **kwargs)

#登录界面
class LogInView(GuestOnlyView, FormView):
    template_name = 'accounts/log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        # if settings.USE_REMEMBER_ME:
        #     if not form.cleaned_data['remember_me']:
        #         request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        # return redirect("admin_index");
        name = request.GET.get("name")
        return render(request, "accounts/index.html", {"name": name})

def viewAllNews(request):
    keywords = request.GET.get('keywords')
    # articleContext = ArticleContext();
    articleContext=None;
    context = {}
    # 资讯列表信息
    allNews = list(articleContext.find_alltype(keywords));
    # print(allNews)
    paginator = Paginator(allNews, 25)  # 每页显示25条
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    context['newsList'] = contacts;
    if keywords is None:
        keywords = '';
    context['keywords']=keywords;
    html_template = loader.get_template('accounts/news_manager.html')
    return HttpResponse(html_template.render(context, request));

def detailNews(request, **kwargs):
    '''显示详细信息'''
    # articleContext = ArticleContext();
    articleContext=None;
    queryset = articleContext.find_by_title(title=kwargs['title']);
    context = {}
    context['segment'] = 'newsDetail'
    context['title'] = queryset['title'].__str__();
    context['keywords'] = queryset['keywords'].__str__();
    context['shortitle'] = queryset['shortitle'].__str__();
    context['updatedate'] = queryset['updatedate'].__str__();
    context['writer'] = queryset['writer'].__str__();
    context['titleimg1'] = queryset['titleimg1'].__str__();
    context['totallevel'] = queryset['totallevel'].__str__();
    context['typeid'] = queryset['typeid'].__str__();
    context['modelid'] = queryset['modelid'].__str__();
    context['arcrank'] = queryset['arcrank'].__str__();
    context['click'] = queryset['click'].__str__();
    context['resource'] = queryset['resource'].__str__();
    context['sendate'] = queryset['sendate'].__str__();
    context['contentimg1'] = queryset['contentimg1'].__str__();
    context['content'] = queryset['content'].__str__();
    html_template = loader.get_template('accounts/news_detail.html')

    # 推荐相关阅读
    recommendNews = articleContext.find_all();
    context['recommendNews'] = recommendNews;

    return HttpResponse(html_template.render(context, request));

def updateNews(request):
    '''更新新闻信息'''
    # articleContext = ArticleContext();
    articleContext=None;
    articleContextForm = ArticleContextForm(request.POST)
    title = articleContextForm.data['title'];
    articleContext.updateNews(articleContextForm)
    queryset = articleContext.find_by_title(title=title);
    context = {}
    context['segment'] = 'newsDetail'
    context['title'] = queryset['title'].__str__();
    context['keywords'] = queryset['keywords'].__str__();
    context['shortitle'] = queryset['shortitle'].__str__();
    context['updatedate'] = queryset['updatedate'].__str__();
    context['writer'] = queryset['writer'].__str__();
    context['titleimg1'] = queryset['titleimg1'].__str__();
    context['content'] = queryset['content'].__str__();
    html_template = loader.get_template('accounts/news_detail.html')

    # 推荐相关阅读
    recommendNews = articleContext.find_all();
    context['recommendNews'] = recommendNews;

    return HttpResponse(html_template.render(context, request));

