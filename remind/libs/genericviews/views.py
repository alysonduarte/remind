# coding: UTF-8
from response import SaveTemplateResponseMixin, SaveAjaxTemplateResponseMixin
from form import SaveModelFormMixim, SaveAjaxModelFormMixim
from django.views.generic.base import View


class BaseSaveView(SaveModelFormMixim, View):
    """
    Base view for updating an existing object or a create a new object.
    Using this base class requires subclassing to provide a response mixin.
    """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object() if 'pk' in kwargs  \
            or 'slug' in kwargs else None
        action = self.get_action_url('edit' if self.object else 'save')
        form_class = self.get_form_class()
        kwargs = {'form': self.get_form(form_class),
                  'action': action}
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() \
            if 'pk' in kwargs or 'slug' in kwargs else None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseSaveAjaxView(SaveAjaxModelFormMixim, View):
    """
    Base view for updating an existing object or a create a new object.
    Using this base class requires subclassing to provide a response mixin.
    """
    def get(self, request, *args, **kwargs):
        self.object = self.get_object() if 'pk' in kwargs \
            or 'slug' in kwargs else None
        action = self.get_action_url('edit' if self.object else 'save')
        form_class = self.get_form_class()
        kwargs = {'form': self.get_form(form_class),
                  'action': action}
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() if 'pk' in kwargs \
            or 'slug' in kwargs else None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class SaveView(SaveTemplateResponseMixin, BaseSaveView):
    """
    View for updating an object,
    with a response rendered by template.
    """
    template_name_suffix = '_form'


class SaveAjaxView(SaveAjaxTemplateResponseMixin, BaseSaveAjaxView):
    """
    View for updating an object,
    with a response rendered by json.
    """
    template_name_suffix = '_form'
