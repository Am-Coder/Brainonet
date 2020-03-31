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
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from utilities.imsearch import colordescriptor, searcher, createdataset
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
import cv2
import logging
import numpy as np

logger = logging.getLogger(__name__)


def stafflogin_view(request):
    context = {}
    context['mobileForm'] = MobileForm
    context['otpForm'] = OtpForm
    return render(request, 'adminapp/login.html', context)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def staffhome_view(request):
    context = {}
    context['response'] = _("response.success")
    return render(request, "adminapp/home.html", context)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def blog_manager_view(request):
    context = {}
    context['response'] = _("response.success")
    context['blogForm'] = form.BlogForm
    return render(request, "adminapp/pages/managers/blog-manager.html", context)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def community_manager_view(request):
    context = {}
    context['response'] = _("response.success")
    context['communityForm'] = form.CommunityForm
    return render(request, "adminapp/pages/managers/community-manager.html", context)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reference_manager_view(request):
    context = {}
    context['response'] = _("response.success")
    context['referenceForm'] = form.ReferencesForm
    return render(request, "adminapp/pages/managers/reference-manager.html", context)


class BlogHomeView(generic.ListView, APIView):
    permission_classes = [IsAuthenticated]
    model = Blog
    template_name = "adminapp/pages/managers/update-job/blog-update.html"
    context_object_name = "blogCollection"
    paginate_by = 10
    # queryset = Blog.objects.all()

    def get_queryset(self):
        if self.request.GET.get('filter_title'):
            title = self.request.GET.get('filter_title')
            blog = Blog.objects.filter(title__contains=title)
        else:
            blog = Blog.objects.all()
        return blog


class BlogUpdateView(generic.UpdateView):
    permission_classes = [IsAuthenticated]
    model = Blog
    # fields = ['title', 'references', 'description', 'body', 'image', 'community']
    template_name = "adminapp/pages/managers/update-job/update-form.html"
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
        BlogHistory(blogid=self.object.pk, user=self.request.user, job='U').save()
        return HttpResponseRedirect(self.get_success_url())


class BlogDeleteView(generic.DeleteView, APIView):
    permission_classes = [IsAuthenticated]
    model = Blog
    success_url = reverse_lazy('personal:blog_manager')
    template_name = "adminapp/pages/managers/update-job/confirm-delete.html"

    def delete(self, request, *args, **kwargs):
        # self.object = form.save()
        self.object = self.get_object()
        success_url = self.get_success_url()
        BlogHistory(blogid=self.object.pk, user=self.request.user, job='D').save()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class CommunityHomeView(generic.ListView, APIView):
    permission_classes = [IsAuthenticated]
    model = Communities
    template_name = "adminapp/pages/managers/update-job/community-update.html"
    context_object_name = "communityCollection"
    paginate_by = 10
    # queryset = Blog.objects.all()

    def get_queryset(self):
        if self.request.GET.get('filter_name'):
            name = self.request.GET.get('filter_name')
            community = Communities.objects.filter(name__contains=name)
        else:
            community = Communities.objects.all()
        return community


class CommunityUpdateView(generic.UpdateView):
    permission_classes = [IsAuthenticated]
    model = Communities
    # fields = ['title', 'references', 'description', 'body', 'image', 'community']
    template_name = "adminapp/pages/managers/update-job/update-form.html"
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
        CommunityHistory(communityid=self.object.pk, user=self.request.user, job='U').save()
        return HttpResponseRedirect(self.get_success_url())


class CommunityDeleteView(generic.DeleteView, APIView):
    permission_classes = [IsAuthenticated]
    model = Communities
    success_url = reverse_lazy('personal:community_manager')
    template_name = "adminapp/pages/managers/update-job/confirm-delete.html"

    def delete(self, request, *args, **kwargs):
        # self.object = form.save()
        self.object = self.get_object()
        success_url = self.get_success_url()
        CommunityHistory(communityid=self.object.pk, user=self.request.user, job='D').save()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class ReferenceUpdateView(generic.UpdateView):
    permission_classes = [IsAuthenticated]
    model = References
    # fields = ['title', 'references', 'description', 'body', 'image', 'community']
    template_name = "adminapp/pages/managers/update-job/update-form.html"
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
        ReferenceHistory(referenceid=self.object.pk, user=self.request.user, job='U').save()
        return HttpResponseRedirect(self.get_success_url())


class ReferenceDeleteView(generic.DeleteView, APIView):
    permission_classes = [IsAuthenticated]
    model = References
    success_url = reverse_lazy('personal:reference_manager')
    template_name = "adminapp/pages/managers/update-job/confirm-delete.html"

    def delete(self, request, *args, **kwargs):
        # self.object = form.save()
        self.object = self.get_object()
        success_url = self.get_success_url()
        ReferenceHistory(referenceid=self.object.pk, user=self.request.user, job='D').save()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class UserListView(generic.ListView, APIView):

    permission_classes = [IsAuthenticated]
    model = Account
    template_name = "adminapp/pages/managers/user-manager.html"
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return References.objects.none()

        qs = References.objects.all()
        if self.q:
            qs = qs.filter(refers__istartswith=self.q)
        return qs


class UsersAutocomplete(autocomplete.Select2QuerySetView, APIView):
    permission_classes = [IsAuthenticated]
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
@permission_classes([IsAuthenticated])
def uploadblog(request):
    print(request.FILES)
    blog_form = BlogForm(request.POST, request.FILES)
    if blog_form.is_valid():
        blog = blog_form.save()
        BlogHistory(blogid=blog.pk, user=request.user, job="C").save()
        return redirect(reverse("personal:staff_home"))
    print(blog_form.errors)
    return HttpResponse(_("msg.upload.error"))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadreferences(request):
    reference_form = form.ReferencesForm(request.POST)
    if reference_form.is_valid():
        reference = reference_form.save()
        # reference = References.objects.get_or_create(**reference_form.cleaned_data)
        ReferenceHistory(referenceid=reference.pk, user=request.user, job="C").save()
        return redirect(reverse("personal:staff_home"))
    logger.error(reference_form.errors)
    return HttpResponse(_("msg.upload.error"))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadcommunity(request):
    community_form = CommunityForm(request.POST, request.FILES)
    if community_form.is_valid():
        community = community_form.save()
        CommunityHistory(communityid=community.pk, user=request.user, job="C").save()
        return redirect(reverse("personal:staff_home"))
    return HttpResponse(_("msg.upload.error"))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stafflogout(request):
    request.auth.delete()
    response = redirect(reverse("personal:staff_login"))
    path = reverse("personal:staff_login")
    # Resolve Cookie Delete for User - Current issue is cross domain, make domain dynamic, check in Production
    path = path[:-1]    # To remove last '/' from 'api/personal/' for cookie path
    domain = str.split(request.get_host(), ':')[0]
    logger.info("Logging out, Cookie Domain is " + domain)
    logger.info("Logging out, Cookie Path is " + path)
    response.delete_cookie("Authorization", domain=domain, path=path)
    response.delete_cookie("User", domain=domain, path=path)
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fakenews_home(request):
    context = {}
    context['response'] = _("response.success")
    context['imageForm'] = form.ImageSearchForm
    return render(request, 'adminapp/pages/faketools/fake-image-search.html', context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fakenews_image_search(request):
    context = {}
    image_form = form.ImageSearchForm(request.POST, request.FILES)
    if image_form.is_valid():
        logger.info("Form Valid")
        context = {}
        logger.info(request.FILES.get('image'))
        image = get_opencv_img_from_buffer(request.FILES.get('image'))
        cd = colordescriptor.ColorDescriptor((8, 12, 3))
        features = cd.describe(image)
        results = searcher.Searcher().search(features, 3)
        if len(results) != 0:
            context['response'] = _("response.success")
            context['results'] = results
        else:
            context['response'] = _("response.error")
            context['error_message'] = _('msg.personal.fake.imagesearch.not.found')
    else:
        logger.warning("Form Invalid")

    context['imageForm'] = form.ImageSearchForm
    return render(request, 'adminapp/pages/faketools/fake-image-search.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fakenews_image_dataset(request):
    context = {}
    logger.info("Starting dataset creation ...")
    context['imageForm'] = form.ImageSearchForm

    try:
        createdataset.create_with_db()
        return render(request, 'adminapp/pages/faketools/fake-image-search.html', context)
    # Need to correct for specific exceptions problem with opencv Python
    except Exception as e:
        logger.exception(e)
        context['error_message'] = _('msg.personal.fake.imagesearch.dataset.error')
        return render(request, 'adminapp/pages/faketools/fake-image-search.html', context)


# Utility Functions
def get_opencv_img_from_buffer(buffer, flags=-1):
    bytes_as_np_array = np.frombuffer(buffer.read(), dtype=np.uint8)
    return cv2.imdecode(bytes_as_np_array, flags)


def get_token_from_cookie(request):
    token = request.COOKIES.get("Authorization")
    if token:
        token = token.replace("Token%20", "")
    return token

