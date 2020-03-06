from django.views import generic
from personal.api import form
from blog.models import Blog, References
from django.views.decorators.http import require_POST, require_GET
from django.utils.decorators import method_decorator
from .form import BlogForm, CommunityForm, ReferencesModelFormset
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.shortcuts import Http404, HttpResponse
from account.models import Account, Token
from dal import autocomplete
# from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from account.api.form import MobileForm, OtpForm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def staffhome(request):
    context = {}
    # token = get_token_from_cookie(request)

    # try:
    #     Token.objects.get(key=token)
    context['blogForm'] = form.BlogForm
    context['referencesFormset'] = form.ReferencesModelFormset(queryset=References.objects.none())
    context['communityForm'] = form.CommunityForm
    context['referencesForm'] = form.ReferencesForm
    return render(request, "home.html", context)
    # except Token.DoesNotExist:
    #     return HttpResponse("<h1>401</h1>Unauthorized", status=401)


# class StaffCreateView(generic.ListView, APIView):
#     permission_classes = []
#     model = References
#     template_name = "home.html"
#     context_object_name = "references"
#     paginate_by = 10
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['blogForm'] = form.BlogForm
#         # context['referencesFormset'] = form.ReferencesModelFormset(queryset=References.objects.none())
#         context['communityForm'] = form.CommunityForm
#         context['referencesForm'] = form.ReferencesForm
#         return context


class BlogHomeView(generic.ListView, APIView):
    permission_classes = [IsAuthenticated]
    model = Blog
    template_name = "blogdisplay.html"
    context_object_name = "blogCollection"
    paginate_by = 10
    queryset = Blog.objects.all()


class BlogUpdateView(generic.UpdateView):
    # permission_classes = []
    model = Blog
    # fields = ['title', 'references', 'description', 'body', 'image', 'community']
    template_name = "blog_update_form.html"
    success_url = reverse_lazy('personal:show_blog')
    form_class = BlogForm

    def post(self, request, *args, **kwargs):
        token = get_token_from_cookie(request)
        print(token)
        try:
            Token.objects.get(key=token)
            return super(BlogUpdateView, self).post(request, **kwargs)
        except Token.DoesNotExist:
            return HttpResponse("<h1>401</h1>Unauthorized", status=401)


class BlogDeleteView(generic.DeleteView, APIView):
    permission_classes = [IsAuthenticated]
    model = Blog
    success_url = reverse_lazy('personal:show_blog')
    template_name = "confirm_blog_delete.html"


class UserListView(generic.ListView, APIView):

    permission_classes = [IsAuthenticated]
    model = Account
    template_name = "showaccount.html"
    context_object_name = "accountCollection"
    paginate_by = 10
    queryset = Account.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    # def get(self, request):
    #     queryset = Account.objects.all()
    #     return Response({'accountCollection': queryset, 'userForm': form.UserForm})
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userForm'] = form.UserForm
        return context


class ReferencesAutocomplete(autocomplete.Select2QuerySetView, APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return References.objects.none()

        qs = References.objects.all()
        if self.q:
            qs = qs.filter(refers__istartswith=self.q)
        return qs


class UsersAutocomplete(autocomplete.Select2QuerySetView, APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return References.objects.none()

        qs = Account.objects.all()
        if self.q:
            qs = qs.filter(mobile_number__istartswith=self.q)
            # qs = qs.filter(Q(mobile_number__istartswith=self.q) | Q(first_name__istartswith=self.q) | Q(last_name__istartswith=self.q))
        return qs


def stafflogin(request):
    context = {}
    context['mobileform'] = MobileForm
    context['otpform'] = OtpForm
    return render(request, 'stafflogin.html', context)


# @require_POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadblog(request):
    blog_form = BlogForm(request.POST, request.FILES)

    if blog_form.is_valid():
        blog_form.save()
        return redirect(reverse("personal:staff_home"))

    print(blog_form.errors)
    return HttpResponse("Some Error Occured")


# @require_POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadreferences(request):
    reference_form = form.ReferencesForm(request.POST)
    if reference_form.is_valid():
        References.objects.get_or_create(**reference_form.cleaned_data)
        return redirect(reverse("personal:staff_home"))
    return HttpResponse("Reference Already Exists")


# @require_POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadcommunity(request):
    community_form = CommunityForm(request.POST, request.FILES)
    if community_form.is_valid():
        community_form.save()
        return redirect(reverse("personal:staff_home"))
    return HttpResponse("Some Error Occured")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stafflogout(request):

    request.auth.delete()

    return redirect(reverse("personal:staff_login"))


def get_token_from_cookie(request):
    token = request.COOKIES.get("Authorization")
    # print(token)
    if token:
        token = token.replace("Token%20", "")
    # print(token)
    return token
