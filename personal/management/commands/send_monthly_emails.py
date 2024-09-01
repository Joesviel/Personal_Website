"""This script implements the functionality of a subscription plan
that monthly sends to all subscribed users all the new posts
during that month. The idea was for this to be used in pythoneverywhere."""

__author__ = "Joseph Fernando Núñez Solano"
__version__ = "1.0.1"
__maintainer__ = "Joseph Fernando Núñez Solano"
__email__ = "joseph.nunezsolano@ucr.ac.cr"
__status__ = "Production"


from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from personal.models import SubscribedUsers, Post

class Command(BaseCommand):
    """
    Class that sends all the new post for each month to all
    subscribed users with said plan.
    """

    help = 'Send monthly email summaries to subscribers'

    def handle(self, *args, **kwargs):
        """
        Handles the mail sending.
        """
        today = timezone.now()
        start_date = (today - timedelta(days=today.day)).replace(day=1)
        end_date = today.replace(day=1)
        
        posts = Post.objects.filter(date__range=[start_date, end_date])
        if posts.exists():
            post_list = "\n\n".join([f"{post.title}\n{post.body}" for post in posts])
            subscribers = SubscribedUsers.objects.filter(sub_plan="Monthly")
            
            for subscriber in subscribers:
                send_mail(
                    'Monthly Blog Post Summary',
                    post_list,
                    'josephnew20022016@gmail.com',  # Replace with your email
                    [subscriber.email],
                    fail_silently=False,
                )
            self.stdout.write(self.style.SUCCESS('Successfully sent monthly email summaries'))
        else:
            self.stdout.write(self.style.SUCCESS('No posts found for the past month'))