from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
# from django.utils.translation import ugettext as _ # Translation

from uuslug import uuslug
import moneyed
from djmoney.models.fields import MoneyField
from sorl.thumbnail import ImageField
from unidecode import unidecode


class CustomUser(AbstractUser):

    # Mobile number
    phone = models.CharField('phone', max_length=30, null=True, blank=True)
    subscription = models.BooleanField('subscription', default=True, db_index=True)

    def allow_add_post(self):
            # TODO check if the user is in ban list
            if self.post_set.count() > settings.CORE['POST_PER_USER_LIMIT']:
                return False
            else:
                return True

    def count(self):
            return Post.objects.filter(user=self).count()

    def get_full_name(self):
        return u'%s %s ' % (self.first_name, self.last_name)


# Section houses Group
class Section(models.Model):

    title = models.CharField(max_length=100)

    def count(self):
        return Post.objects.filter(is_active=True).filter(group__section=self).count()

    def __str__(self):
        return self.title


# Group houses Post
class Group(models.Model):

    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(max_length=100)
    section = models.ForeignKey('Section')

    def count(self):
        return self.post_set.filter(is_active=True).count()

    def get_absolute_url(self):
        return reverse('group', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_title(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['section__title', 'title', ]


class Post(models.Model):

    slug = models.SlugField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    group = models.ForeignKey(Group, verbose_name="group")

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='MYR')
    phone = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True, db_index=True)

    updated = models.DateTimeField(blank=True, null=True)
    posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_title(self):
        return u'%s' % self.title

    def get_description(self):
        return u'%s' % self.description[:155]

    def get_keywords(self):
        return ",".join(set(self.description.split()))

    def get_related(self):
        return Post.objects.exclude(pk=self.pk)[:settings.CORE['RELATED_LIMIT']]

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-updated', )


class Image(models.Model):

    post = models.ForeignKey(Post)
    file = ImageField(upload_to='images')
