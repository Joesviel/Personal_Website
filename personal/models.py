from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

# Create your models here.

class Post(models.Model):
    """
    Model for the Post. It represents a post in the blog application.

    ...

    Attributes
    title:
        the title of the post.
    author:
        the author of the post (an user).
    date:
        assign current date and time by default.
    favorites:
        the "likes" a post has.
    body:
        the body of the blogpost.

    Methods
    -------
    save(self, *args, **kwargs)
        Each time a new post is posted, this function sends a mail
        to all the SubscribedUsers with a plan for each new post.
    """

    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    favorites = models.IntegerField(default=0)
    body = models.TextField()

    def __str__(self):
        return self.title + ' | ' + str(self.author) + ' | ' + self.date.strftime('%d/%m/%Y') + ' | ' + str(self.favorites)
    
    def save(self, *args, **kwargs):
        """
        Sends a mail to all subscribed users each time a new post
        is uploaded. The user most be subscribed with the plan that
        sends a mail for each new post.
        
        Parameters
        ----------
        args: tuple
            django internal data.
        kwargs: dict
            django internal data.
        """

        super().save(*args, **kwargs)
        # Send email to "For each post" subscribers
        subscribers = SubscribedUsers.objects.filter(sub_plan="For each post")
        for subscriber in subscribers:
            send_mail(
                'New Blog Post: ' + self.title,
                self.body,
                'josephnew20022016@gmail.com',
                [subscriber.email],
                fail_silently=False,
            )

class Comment(models.Model):
    """
    Model for a Comment. It represents a comment about a blogpost.

    ...

    Attributes
    user:
        the user author of the comment.
    post:
        the blog post the comment references.
    date:
        assign current date and time by default.
    likes:
        the likes if a comment.
    body:
        the body of the comment.
    parent:
        if the comment is a reply to another comment, this attribute
        is used instead of post. It references the comment it replies.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, null=True, blank=True, related_name= "comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=user.name)
    date = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    body = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    class Meta:
        """
        Implements a custom permisson for the Comment model.
        This permission allowes the user to only have the option
        to delete their own comments.

        ...

        Attributes
        permissions: list
            contains a tuple with the custom permission and its
            description.
        """
        permissions = [
            ("delete_own_comment", "can delete only own comments"),
        ]
    
    def __str__(self):
        return '%s' % (self.name)

class SubscribedUsers(models.Model):
    """
    Model that implements the users subscribed to the
    blog application.

    ...

    Attributes
    name:
        the name of the subscribed user.
    email:
        the email of the subscribed user.
    created_date:
        assign current date and time by default.
    sub_plan:
        two options: recieves a monthly mail with new posts
        or one for each new post.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)
    sub_plan = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Bitacora(models.Model):
    """
    Model that implements binnacle entry. It saves
    the user (if authenticated) and the action it
    does.

    ...

    Attributes
    user:
        the user who made the action.
    action:
        the action made by the user
    created:
        assign current date and time by default.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action = models.CharField(max_length=255)
    created = models.DateTimeField('Date Created', default=timezone.now)

    def store_user_action(user=None, action=''):
        """
        Saves a new entry in the binnacle. It's used in the views.
        
        Parameters
        ----------
        user: User
            the user who made the action.
        action: string
            the described action made by the user.
        """

        if user is None:
            entry = Bitacora(action=action)
        else:
            entry = Bitacora(user=user, action=action)
        entry.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When a new user is authenticated, this procedure automatically
    assign the role 'BlogSubscriber' to them."
    """
    if created:
        instance.groups.add(Group.objects.get(name='BlogSubscriber'))