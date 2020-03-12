from django.db import models
from django.core.exceptions import ValidationError
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel



class ServiceListingPage(Page):

    subtitle = models.TextField(
        blank=True,
        max_length=500,
    )

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['services'] = ServicePage.objects.live().public()
        return context


class ServicePage(Page):

    description = models.CharField(
        blank='True',
        max_length=500,
    )
    internal_page = models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text="select a page",
        on_delete=models.SET_NULL,
    )
    external_page = models.URLField(
        blank=True,
    )
    button_text = models.CharField(
        blank=True,
        max_length=50,
    )
    service_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='This image will be used on the service page.',
        related_name='+',
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        PageChooserPanel('internal_page'),
        FieldPanel('external_page'),
        FieldPanel('button_text'),
        ImageChooserPanel('service_image'),
    ]

    def clean(self):
        super().clean()

        if self.internal_page and self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("please only select a page OR enter an external URL"),
                'external_page': ValidationError("please only select a page OR enter an external URL"),
            })

        if not self.external_page and not self.internal_page:
            raise ValidationError({
                'internal_page': ValidationError("please select a page or external URL"),
                'external_page': ValidationError("please select a page or external URL"),
            })
