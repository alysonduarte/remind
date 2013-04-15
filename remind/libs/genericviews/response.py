# coding : UTF-8

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateResponseMixin
from django.utils.simplejson import dumps
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext


class SaveTemplateResponse(object):
    """
    Custom config for template response.
    """
    custom_url_args = {}
    save_response_prefix = 'edit'
    add_response_prefix = 'save'
    delete_response_prefix = 'delete'
    char_join_url = '-'
    url_name_attr = 'pk'

    def get_url_kwargs(self, type):
        """
            generate kwargs with
            custom args
        """
        object_args = {}

        if not type == 'save':
            try:
                if 'slug' in self.kwargs:
                    self.url_name_attr = 'slug'

                object_args[self.url_name_attr] = getattr(
                    self.object, self.url_name_attr)
            except:
                raise Exception("%s does not contain attribute %s" % (
                    self.object._meta.object_name.lower(), self.url_name_attr))

        #' self.kwargs
        kwargs = self.kwargs
        if 'pk' in kwargs:
            del kwargs['pk']
        if 'slug' in kwargs:
            del kwargs['slug']

        if type in self.custom_url_args and self.custom_url_args[type]:
            if self.custom_url_args[type] in kwargs:
                del kwargs[self.custom_url_args[type]]

            kwargs.update(self.custom_url_args[type])
        return dict(kwargs.items() + object_args.items())

    def get_action_url(self, type):
        """
            reverse url with your kwargs

            :Parameters:
                `type`: string
                    types: save, delete and add
            :Returns: string
                reversing url
        """
        app = self.model._meta.app_label.lower()
        model = self.model._meta.object_name.lower()

        if type == 'edit':
            url = "%s:%s" % (app, "%s%s%s" % (
                self.save_response_prefix, self.char_join_url, model))
        elif type == 'save':
            url = "%s:%s" % (app, "%s%s%s" % (
                self.add_response_prefix, self.char_join_url, model))
        elif type == 'delete':
            url = "%s:%s" % (app, "%s%s%s" % (
                self.delete_response_prefix, self.char_join_url, model))
        else:
            raise Exception('Invalid action %s' % type)

        kwargs = self.get_url_kwargs(type)

        if kwargs:
            url = reverse(url, kwargs=kwargs)
        else:
            url = reverse(url)

        return url


class SaveTemplateResponseMixin(TemplateResponseMixin, SaveTemplateResponse):
    """
    Mixim for template response.
    """
    pass


class SaveAjaxTemplateResponseMixin(TemplateResponseMixin,
                                    SaveTemplateResponse):
    """
    Mixin for template response in ajax call.
    """
    form_template_name = None

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request.
        Must return a list. May not be called
        if render_to_response is overridden.
        If the request is a post, return form_template_name
        """
        if self.request.POST and not self.form_template_name is None:
            return [self.form_template_name]
        else:
            return super(SaveAjaxTemplateResponseMixin,
                         self).get_template_names()

    def render_to_response(self, context):
        """
        Returns the HttpResponse based in context.
        """
        return render_to_response(self.get_template_names(),
                                  RequestContext(self.request, context))

    def render_to_response_json(self, context):
        """
        Returns a response with a context json rendered.
        """
        return HttpResponse(dumps(context), mimetype="application/json")
