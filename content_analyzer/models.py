from django.db import models
from django.contrib.postgres.fields import ArrayField

class ContentSource(models.Model):
    url = models.URLField(max_length=2000)
    type = models.CharField(max_length=20, choices=[
        ('website', 'Website'),
        ('video', 'Video'),
        ('article', 'Article'),
    ])
    last_crawled = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('error', 'Error'),
        ('archived', 'Archived'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.url}"

class ContentItem(models.Model):
    source = models.ForeignKey(ContentSource, on_delete=models.CASCADE, related_name='content_items')
    content_type = models.CharField(max_length=20, choices=[
        ('text', 'Text'),
        ('transcript', 'Transcript'),
        ('metadata', 'Metadata'),
    ])
    raw_content = models.TextField()
    processed_content = models.TextField(blank=True)
    extracted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content_type} from {self.source.url}"

class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    keywords = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name