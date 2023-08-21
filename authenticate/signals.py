from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver
import logging
from post.models import Post

logger = logging.getLogger('django')
User = get_user_model()


# from .utils import calculate_incomes

@receiver(
    signals.post_save,
    sender=User)
def add_logs(sender, instance: User, **kwargs):

    logger.info(f'User Registered(id: {instance.id} - username: {instance.username})')


