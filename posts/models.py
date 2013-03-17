from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import permalink
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    STATUS = ( (u'DRAFT', u'DRAFT'),
               (u'PUBLISHED', u'PUBLISHED'))
    title = models.CharField(max_length=200)
    pub_date = models.DateField()
    text = models.TextField()
    slug = models.SlugField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS)

    def __unicode__(self):
        return u'%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('view_post', (), {
        'slug' : self.slug
        })

class Tag(models.Model):
    post = models.ManyToManyField(Post)
    tag = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' % str(self.tag)

class Comment(models.Model):
    STATUS = ((u'A', u'ACCEPTED'),
              (u'D', u'DENIED'),
              (u'P', u'PENDING'))
    
    post = models.ForeignKey(Post)
    author = models.CharField(max_length=50, blank=True)
    comment = models.TextField()
    status = models.CharField(max_length=2, choices=STATUS, default='P')

    def __unicode__(self):
        if not self.author:
            return u'%s' % self.comment
        return u'%s %s' % (self.author, self.comment)

@receiver(pre_save, sender=Post)
def slugifyMyPost(sender, **kargs):
    from django.template.defaultfilters import slugify
    import datetime
    post = kargs['instance']
    post.slug = slugify(post.title)

@receiver(pre_save, sender=Comment)
def set_comment_author_to_anonymous(sender, **kargs):
    comment = kargs['instance']
    if comment.author == '':
        comment.author = 'Anonymous'