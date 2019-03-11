from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True,)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True) #unique -- для унікальності імені
    body = models.TextField(max_length=250, db_index=True, blank=True) # db_index -- для швидкого пошуку по змісту
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_pub']

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    #для передачі параметку слаг в шаблонах вю
    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return '{}'.format(self.title)

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})