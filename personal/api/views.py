from django.views import generic
from personal.api import form
from blog.models import Blog, References, BlogHistory, ReferenceHistory
from communities.models import Communities, CommunityHistory
from account.models import TokenAuthentication
from .form import BlogForm, CommunityForm, ReferencesForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.shortcuts import Http404, HttpResponse
from django.http import HttpResponseRedirect
from account.models import Account, Token
from dal import autocomplete
from account.api.form import MobileForm, OtpForm
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from utilities.imsearch import colordescriptor, searcher, createdataset
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from rest_framework.response import Response
import cv2
import logging
from personal.utils import get_token_from_cookie, get_opencv_img_from_buffer, get_image_search_results
from account.permissions import IsStaff, IsManager, IsAdministrator

logger = logging.getLogger(__name__)


def stafflogin_view(request):
    context = {}
    context['mobileForm'] = MobileForm
    context['otpForm'] = OtpForm
    return render(request, 'staffapplication/login.html', context)


@api_view(["GET"])
@permission_classes([IsStaff])
def staffhome_view(request):
    context = {}
    context['response'] = _("response.success")
    return render(request, "staffapplication/home.html", context)


@api_view(["GET"])
@permission_classes([IsStaff])
def blog_manager_view(request):
    context = {}
    logger.info(request.query_params)
    logger.info(request.GET)
    context['response'] = _("response.success")
    context['blogForm'] = form.BlogForm
    # for session storage based back button
    if request.GET.get('back', False):
        context['back'] = True
    return render(request, "staffapplication/pages/managers/blog-manager.html", context)


@api_view(["GET"])
@permission_classes([IsStaff])
def staff_manager_view(request):
    context = {}
    logger.info(request.query_params)
    logger.info(request.GET)
    context['response'] = _("response.success")
    context['staffCreateForm'] = form.StaffCreateForm(initial={'is_staff':True})
    # for session storage based back button
    if request.GET.get('back', False):
        context['back'] = True
    return render(request, "staffapplication/pages/managers/staff-manager.html", context)


@api_view(["GET"])
@permission_classes([IsStaff])
def community_manager_view(request):
    context = {}
    context['response'] = _("response.success")
    context['communityForm'] = form.CommunityForm
    # for session storage based back button
    if request.GET.get('back', False):
        context['back'] = True
    return render(request, "staffapplication/pages/managers/community-manager.html", context)


@api_view(["GET"])
@permission_classes([IsStaff])
def reference_manager_view(request):
    context = {}
    context['response'] = _("response.success")
    context['referenceForm'] = form.ReferencesForm
    # for session storage based back button
    if request.GET.get('back', False):
        context['back'] = True
    return render(request, "staffapplication/pages/managers/reference-manager.html", context)


class BlogHistoryView(generic.ListView, APIView):
    permission_classes = [IsStaff]
    model = Blog
    template_name = "staffapplication/pages/managers/update-job/content-history.html"
    context_object_name = "changeCollection"
    paginate_by = 10

    def get_queryset(self):
        history = BlogHistory.objects.filter(blogid=self.kwargs['slug'])
        return history

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogback'] = True
        return context


class BlogUpdateView(generic.UpdateView):
    permission_classes = [IsStaff]
    model = Blog
    # fields = ['title', 'references', 'description', 'body', 'image', 'community']
    template_name = "staffapplication/pages/managers/update-job/update-form.html"
    success_url = reverse_lazy('personal:blog_manager')
    form_class = BlogForm

    def post(self, request, *args, **kwargs):
        token = get_token_from_cookie(request)
        try:
            token = Token.objects.get(key=token)
            request.user = token.user
            return super(BlogUpdateView, self).post(request, **kwargs)
        except Token.DoesNotExist:
            return HttpResponse("response.401", status=401)

    def form_valid(self, form):
        self.object = form.save()
        BlogHistory(blogid=self.object.slug, user=self.request.user, job='U').save()
        messages.add_message(self.request, messages.SUCCESS, "Blog Updated Successfuly")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogback'] = True
        return context


class BlogDeleteView(generic.DeleteView, APIView):
    permission_classes = [IsStaff]
    model = Blog
    success_url = reverse_lazy('personal:blog_manager')
    template_name = "staffapplication/pages/managers/update-job/confirm-delete.html"

    def delete(self, request, *args, **kwargs):
        # self.object = form.save()
        self.object = self.get_object()
        success_url = self.get_success_url()
        BlogHistory(blogid=self.object.slug, user=self.request.user, job='D').save()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogback'] = True
        return context


class CommunityHistoryView(generic.ListView, APIView):
    permission_classes = [IsStaff]
    model = Communities
    template_name = "staffapplication/pages/managers/update-job/content-history.html"
    context_object_name = "changeCollection"
    paginate_by = 10

    def get_queryset(self):
        history = CommunityHistory.objects.filter(communityid=self.kwargs['slug'])
        return history

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['communityback'] = True
        return context


class CommunityUpdateView(generic.UpdateView):
    permission_classes = [IsStaff]
    model = Communities
    # fields = ['title', 'references', 'description', 'body', 'image', 'community']
    template_name = "staffapplication/pages/managers/update-job/update-form.html"
    success_url = reverse_lazy('personal:community_manager')
    form_class = CommunityForm

    def post(self, request, *args, **kwargs):
        token = get_token_from_cookie(request)
        try:
            token = Token.objects.get(key=token)
            request.user = token.user
            return super(CommunityUpdateView, self).post(request, **kwargs)
        except Token.DoesNotExist:
            return HttpResponse("response.401", status=401)

    def form_valid(self, form):
        self.object = form.save()
        CommunityHistory(communityid=self.object.slug, user=self.request.user, job='U').save()
        messages.add_message(self.request, messages.SUCCESS, "Community Updated Successfuly")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['communityback'] = True
        return context


class CommunityDeleteView(generic.DeleteView, APIView):
    permission_classes = [IsStaff]
    model = Communities
    success_url = reverse_lazy('personal:community_manager')
    template_name = "staffapplication/pages/managers/update-job/confirm-delete.html"

    def delete(self, request, *args, **kwargs):
        # self.object = form.save()
        self.object = self.get_object()
        success_url = self.get_success_url()
        CommunityHistory(communityid=self.object.slug, user=self.request.user, job='D').save()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['communityback'] = True
        return context


class ReferenceHistoryView(generic.ListView, APIView):
    permission_classes = [IsStaff]
    model = References
    template_name = "staffapplication/pages/managers/update-job/content-history.html"
    context_object_name = "changeCollection"
    paginate_by = 10

    def get_queryset(self):
        history = ReferenceHistory.objects.filter(referenceid=self.kwargs['pk'])
        return history

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referenceback'] = True
        return context


class ReferenceUpdateView(generic.UpdateView):
    permission_classes = [IsStaff]
    model = References
    # fields = ['title', 'references', 'description', 'body', 'image', 'community']
    template_name = "staffapplication/pages/managers/update-job/update-form.html"
    success_url = reverse_lazy('personal:reference_manager')
    form_class = ReferencesForm

    def post(self, request, *args, **kwargs):
        token = get_token_from_cookie(request)
        try:
            token = Token.objects.get(key=token)
            request.user = token.user
            return super(ReferenceUpdateView, self).post(request, **kwargs)
        except Token.DoesNotExist:
            return HttpResponse("response.401", status=401)

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, "Reference Updated Successfuly")
        ReferenceHistory(referenceid=self.object.pk, user=self.request.user, job='U').save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referenceback'] = True
        return context


class ReferenceDeleteView(generic.DeleteView, APIView):
    permission_classes = [IsStaff]
    model = References
    success_url = reverse_lazy('personal:reference_manager')
    template_name = "staffapplication/pages/managers/update-job/confirm-delete.html"

    def delete(self, request, *args, **kwargs):
        # self.object = form.save()
        self.object = self.get_object()
        success_url = self.get_success_url()
        ReferenceHistory(referenceid=self.object.pk, user=self.request.user, job='D').save()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referenceback'] = True
        return context


class UserListView(generic.ListView, APIView):
    permission_classes = [IsStaff]
    model = Account
    template_name = "staffapplication/pages/managers/user-manager.html"
    context_object_name = "accountCollection"
    paginate_by = 10
    queryset = Account.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    # def get(self, request):
    #     queryset = Account.objects.all()
    #     return Response({'accountCollection': queryset, 'userForm': form.UserForm})
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response'] = _("response.success")
        context['userForm'] = form.UserForm
        return context


class ReferencesAutocomplete(autocomplete.Select2QuerySetView, APIView):
    permission_classes = [IsStaff]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return References.objects.none()

        qs = References.objects.all()
        if self.q:
            qs = qs.filter(refers__istartswith=self.q)
        return qs


class UsersAutocomplete(autocomplete.Select2QuerySetView, APIView):
    permission_classes = [IsStaff]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return References.objects.none()

        qs = Account.objects.all()
        if self.q:
            qs = qs.filter(mobile_number__istartswith=self.q)
            # qs = qs.filter(Q(mobile_number__istartswith=self.q) | Q(first_name__istartswith=self.q) | Q(last_name__istartswith=self.q))
        return qs


@api_view(['POST'])
@permission_classes([IsStaff])
def uploadblog(request):
    print(request.FILES)
    blog_form = BlogForm(request.POST, request.FILES)
    if blog_form.is_valid():
        blog = blog_form.save()
        BlogHistory(blogid=blog.slug, user=request.user, job="C").save()
        messages.add_message(request, messages.SUCCESS, "Blog Added Successfuly")
        return redirect(reverse("personal:blog_manager"))
    print(blog_form.errors)
    return HttpResponse(_("msg.upload.error"))


@api_view(['POST'])
@permission_classes([IsStaff])
def uploadreferences(request):
    reference_form = form.ReferencesForm(request.POST)
    if reference_form.is_valid():
        reference = reference_form.save()
        # reference = References.objects.get_or_create(**reference_form.cleaned_data)
        ReferenceHistory(referenceid=reference.pk, user=request.user, job="C").save()
        messages.add_message(request, messages.SUCCESS, "References Added Successfuly")
        return redirect(reverse("personal:reference_manager"))
    logger.error(reference_form.errors)
    return HttpResponse(_("msg.upload.error"))


@api_view(['POST'])
@permission_classes([IsStaff])
def uploadcommunity(request):
    community_form = CommunityForm(request.POST, request.FILES)
    if community_form.is_valid():
        community = community_form.save()
        CommunityHistory(communityid=community.slug, user=request.user, job="C").save()
        messages.add_message(request, messages.SUCCESS, "Community Added Successfuly")
        return redirect(reverse("personal:community_manager"))
    return HttpResponse(_("msg.upload.error"))


@api_view(['POST'])
@permission_classes([IsStaff])
def addstaff(request):
    user_create_form = form.StaffCreateForm(request.POST, request.FILES)
    if user_create_form.is_valid():
        user_create_form.save()
        messages.add_message(request, messages.SUCCESS, "Staff Added Successfuly")
        # CommunityHistory(communityid=community.slug, user=request.user, job="C").save()
        return redirect(reverse("personal:staff_manager"))
    return HttpResponse(_("msg.upload.error"))


@api_view(['GET'])
@permission_classes([IsStaff])
def stafflogout(request):
    request.auth.delete()
    response = redirect(reverse("personal:staff_login"))
    path = reverse("personal:staff_login")
    # Resolve Cookie Delete for User - Current issue is cross domain, make domain dynamic, check in Production
    path = path[:-1]  # To remove last '/' from 'api/personal/' for cookie path
    domain = str.split(request.get_host(), ':')[0]
    logger.info("Logging out, Cookie Domain is " + domain)
    logger.info("Logging out, Cookie Path is " + path)
    response.delete_cookie("Authorization", domain=domain, path=path)
    response.delete_cookie("User", domain=domain, path=path)
    return response


@api_view(['GET'])
@permission_classes([IsStaff])
def fakenews_home(request):
    context = {}
    context['response'] = _("response.success")
    context['imageForm'] = form.ImageSearchForm
    return render(request, 'staffapplication/pages/faketools/fake-image-search.html', context)


@api_view(['POST'])
@permission_classes([IsStaff])
def fakenews_image_search(request):
    context = {}
    image_form = form.ImageSearchForm(request.POST, request.FILES)
    if image_form.is_valid():
        logger.info("Form Valid")
        # context = {}
        logger.info(request.FILES.get('image'))
        image = get_opencv_img_from_buffer(request.FILES.get('image'))
        context = get_image_search_results(image)
        # cd = colordescriptor.ColorDescriptor((8, 12, 3))
        # features = cd.describe(image)
        # results = searcher.Searcher().search(features, 3)
        # if len(results) != 0:
        #     context['response'] = _("response.success")
        #     context['results'] = results
        # else:
        #     context['response'] = _("response.error")
        #     context['error_message'] = _('msg.personal.fake.imagesearch.not.found')
    else:
        logger.warning("Form Invalid")

    context['imageForm'] = form.ImageSearchForm
    return render(request, 'staffapplication/pages/faketools/fake-image-search.html', context)


@api_view(['GET'])
@permission_classes([IsStaff])
def fakenews_image_dataset(request):
    context = {}
    logger.info("Starting dataset creation ...")
    context['imageForm'] = form.ImageSearchForm

    try:
        createdataset.create_with_db()
        return render(request, 'staffapplication/pages/faketools/fake-image-search.html', context)
    # Need to correct for specific exceptions problem with opencv Python
    except Exception as e:
        logger.exception(e)
        context['error_message'] = _('msg.personal.fake.imagesearch.dataset.error')
        return render(request, 'staffapplication/pages/faketools/fake-image-search.html', context)


# error views
def error_500(request, template_name="staffapplication/pages/errors/error.html"):
    data = {}
    data['error_code'] = '500'
    data['error_message'] = _('msg.error.500')
    return render(request, template_name, data)


def error_400(request, exception, template_name="staffapplication/pages/errors/error.html"):
    data = {}
    data['error_code'] = '400'
    data['error_message'] = _('msg.error.400')
    return render(request, template_name, data)


def error_403(request, exception, template_name="staffapplication/pages/errors/error.html"):
    data = {}
    data['error_code'] = '403'
    data['error_message'] = _('msg.error.403')
    return render(request, template_name, data)


def error_404(request, exception, template_name="staffapplication/pages/errors/error.html"):
    data = {}
    data['error_code'] = '404'
    data['error_message'] = _('msg.error.404')
    return render(request, template_name, data)


def error_401(request, exception, template_name="staffapplication/pages/errors/error.html"):
    data = {}
    data['error_code'] = '401'
    data['error_message'] = _('msg.error.401')
    return render(request, template_name, data)

# Utility Functions
# def get_opencv_img_from_buffer(buffer, flags=-1):
#     bytes_as_np_array = np.frombuffer(buffer.read(), dtype=np.uint8)
#     return cv2.imdecode(bytes_as_np_array, flags)
#
#
# def get_token_from_cookie(request):
#     token = request.COOKIES.get("Authorization")
#     if token:
#         token = token.replace("Token%20", "")
#     return token


# error views
# def error_500(request, template_name="staffapplication/pages/errors/error.html"):
#     data = {}
#     data['error_code'] = '500'
#     data['error_message'] = 'We are currently unable to handle your request. You can try reloading or come back later.'
#     return render(request, template_name, data)
#
#
# def error_400(request, exception, template_name="staffapplication/pages/errors/error.html"):
#     data = {}
#     data['error_code'] = '400'
#     data['error_message'] = 'Bad Request'
#     return render(request, template_name, data)
#
#
# def error_403(request, exception, template_name="staffapplication/pages/errors/error.html"):
#     data = {}
#     data['error_code'] = '403'
#     data['error_message'] = 'Forbidden'
#     return render(request, template_name, data)
#
#
# def error_404(request, exception, template_name="staffapplication/pages/errors/error.html"):
#     data = {}
#     data['error_code'] = '404'
#     data['error_message'] = 'The page you’re looking for was not found.'
#     return render(request, template_name, data)
#
#
# def error_401(request, exception, template_name="staffapplication/pages/errors/error.html"):
#     data = {}
#     data['error_code'] = '401'
#     data['error_message'] = 'Unauthorized'
#     return render(request, template_name, data)
