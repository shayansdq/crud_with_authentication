from django.db.models import signals
from django.dispatch import receiver
import logging
from post.models import Post

logger = logging.getLogger('django')


# from .utils import calculate_incomes

@receiver([
    signals.post_save,
    signals.post_delete
],
    sender=Post)
def add_logs(sender, instance: Post, **kwargs):
    """
        This Function gets a signal after creating a new instance of
        IncomeShift children model to modify Daily and Weekly Income Automatically
    """
    save = kwargs.get('created')
    if save:
        logger.info(f'User(id: {instance.user.id}) Created a new Post (id: {instance.id})')
    else:
        logger.info(f'User(id: {instance.user.id} Deleted a Post (id: {instance.id})')

