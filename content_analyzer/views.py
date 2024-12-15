from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from .models import ContentSource
from .services.crawler import WebCrawler

class SubmitURLView(CreateView):
    model = ContentSource
    fields = ['url', 'type']
    template_name = 'content_analyzer/submit_url.html'
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Trigger crawling (Note: In production, this should be handled by Celery)
        crawler = WebCrawler()
        if crawler.crawl_url(self.object):
            messages.success(self.request, "URL successfully processed")
        else:
            messages.error(self.request, "Error processing URL")
            
        return response