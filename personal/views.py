from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, SubscribedUsers, Bitacora
from .forms import CommentForm

# Create your views here.

def land_page_view(request):
    """
    View of the landpage. Only loads the HTML.
    """
    print(request.headers)
    return render(request, "HTML/LandPage.html", {})

# def blog_page_view(request):
    # print(request.headers)
    # return render(request, "HTML/BlogPage.html", {})

def resume_page_view(request):
    """
    View of the resume page. Only loads the HTML.
    """
    print(request.headers)
    return render(request, "HTML/ResumePage.html", {})

def about_me_page_view(request):
    """
    View of the About Me page. Only loads the HTML.
    """
    print(request.headers)
    return render(request, "HTML/AboutMePage.html", {})

def subscribe_page_view(request):
    """
    View of the Blog Subscription page. Only loads the HTML.
    """
    print(request.headers)
    return render(request, "HTML/SubscribePage.html", {})

def subscribe(request):
    """
    This procedure takes the contents from the procedure
    filled in the Blog Subscription page by the user,
    makes sure everything its filled and valid and creates
    the new SubscribedUsers instance.
    """
    
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        sub_plan = request.POST.get('sub_plan', None)

        if not name or not email or not sub_plan:
            messages.error(request, "You must provide a valid name, email, and subscription plan to subscribe to the newsletter.")
            return redirect("/")

        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        
        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"{email} email address is already subscribed.")
            return redirect(request.META.get("HTTP_REFERER", "/"))  

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        # Create and save the new subscribed user
        subscribe_model_instance = SubscribedUsers(
            name=name,
            email=email,
            sub_plan=sub_plan
        )
        subscribe_model_instance.save()

        send_mail(
            'Subscription Confirmation',
            f'Thank you for subscribing to our newsletter with the "{sub_plan}" plan!',
            'josephnew20022016@gmail.com',  # Replace with your email
            [email],
            fail_silently=False,
        )

        if request.user.is_authenticated:
            Bitacora.store_user_action(request.user, 'Subscribed to the blog.')
        else:
            Bitacora.store_user_action(None, 'A user subscribed to the blog.')
        
        messages.success(request, f'{email} was successfully subscribed to our newsletter with the "{sub_plan}" plan!')
        return redirect(request.META.get("HTTP_REFERER", "/"))
    
def home(request):
    """
    Procedure that sends the user from the Land Page to the
    HTML used to log the user using google auth.
    """

    print(request.headers)
    if request.user.is_authenticated:
        Bitacora.store_user_action(request.user, 'user logged.')
    else:
        Bitacora.store_user_action(None, 'user logged.')
    return render(request, "HTML/GoogleSignIn.html")

def logout_view(request):
    """
    Procedure that logouts the user authenticated with Google.
    """

    if request.user.is_authenticated:
        Bitacora.store_user_action(request.user, 'user unlogged.')
    else:
        Bitacora.store_user_action(None, 'user unlogged.')
    logout(request)
    return redirect('/')

def increment_favorites(request, pk):
    """
    Procedure that increases the favorites of a
    given post.

    Attributes
    pk:
        the primary key used to identify the post.
    """

    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        post.favorites += 1
        post.save()
        Bitacora.store_user_action(request.user, 'favorited post ' + post.title +
            ' of id: ' + str(post.pk))
        return JsonResponse({'favorites': post.favorites})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def increment_likes(request, pk):
    """
    Procedure that increases the likes of a
    given comment.

    Attributes
    pk:
        the primary key used to identify the post.
        Only used by the binnacle.
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(pk=comment_id)
        comment.likes += 1
        comment.save()
        Bitacora.store_user_action(request.user, ' liked comment in post of title ' + 
            post.title + ' of id: ' + str(post.pk))
        return JsonResponse({'likes': comment.likes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def delete_comment(request, pk):
    """
    Procedure that deletes a given comment

    Attributes
    pk:
        the primary key used to identify the post.
        Only used by the binnacle.
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        comment_id = request.POST.get('comment_id')
        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.delete()
            Bitacora.store_user_action(request.user, ' deleted a comment in post of title ' + \
                                    post.title + '. of id: ' + str(post.pk))
            return JsonResponse({'success': True})
        return JsonResponse({'error': 'Comment ID not provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

class blog_page_view(ListView):
    """
    Class view of the blog page. It loads a table
    witha ll the posts. Different options are given.

    Attributes
    ListView:
        Render some list of objects.
    """
    model = Post
    template_name = 'HTML/BlogPage.html'

class blog_post_view(DetailView):
    """
    Class view of a blog post. It displays a given post
    with its comments and replies.

    Attributes
    DetailView:
        Renders a detailed view of the object.
    """

    model = Post
    template_name = 'HTML/BlogPost.html'

class add_comment_view(LoginRequiredMixin, CreateView):
    """
    Class view that adds a new comment to a given post.

    Attributes
    LoginRequiredMixin:
        Makes sure the user is authenticated.
    CreateView:
        View for creating a new object.
    
    Methods
    -------
    form_valid(self, form)
        if the form in the html is valid, checks all the
        needed information and adds a new comment.
    def get_success_url(self):
        if the comment creation was successful, it returns
        the user to the blog post the comment belongs to.
    get_context_data:
        gets relevant data related to the comment that is
        going to be created.
    """

    model = Comment
    form_class = CommentForm
    template_name = 'HTML/CommentPost.html'

    def form_valid(self, form):
        """
        Procedure that deletes a given comment

        Attributes
        form:
            a possibly valid form soon to be checked.
        """

        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        Bitacora.store_user_action(self.request.user, ' made a commentary in the post of title ' \
                           + form.instance.post.title \
                           + ' of id: ' + str(form.instance.post.pk))
        return super().form_valid(form)

    def get_success_url(self):
        """
        if the comment creation was successful, it returns
        the user to the blog post the comment belongs to.
        """
        return reverse_lazy('blogpost', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        """
        gets relevant data related to the comment that is
        going to be created.
        """

        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context
