# coding:UTF-8
from django.views.generic.edit import ModelFormMixin
from django.core.validators import EMPTY_VALUES
from django.core.exceptions import ImproperlyConfigured


class SaveModelFormMixim(ModelFormMixin):
    """
    Mixin for model form,
    manage the model form statements.
    """
    hidden_control_submit = 'submit'

    def form_valid(self, form):
        """
        If the form is valid, edit the associated model.
        """
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_literal_url(self):
        """
        Returns the url success
        """
        if self.success_url:
            try:
                url = self.success_url % self.object.__dict__
            except:
                url = self.success_url
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def get_success_url(self):
        """
        Manage the success url, genered for submit condition.
        """
        post = self.request.POST

        if self.hidden_control_submit in post:
            if post[self.hidden_control_submit] == 'new':
                url = self.get_action_url('save')
            elif post[self.hidden_control_submit] == 'continue':
                url = self.get_action_url('edit')
            elif post[self.hidden_control_submit] in EMPTY_VALUES:
                url = self.get_success_literal_url()
            else:
                raise Exception('submit argument %s is not valid' %
                               (post[self.hidden_control_submit]))
        else:
            url = self.get_success_literal_url()
        return url


class SaveAjaxModelFormMixim(SaveModelFormMixim):
    """
    Mixin for model form in ajax call,
    manage the model form statements.
    """
    json_context_list = {}

    def get_json_context_list(self):
        return self.json_context_list

    def get_form_kwargs(self, edit=True):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT') and edit:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        if edit:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_form(self, form_class, edit=True):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs(edit))

    def form_valid(self, form):
        """
        If the form is valid, edit the associated model.
        """
        self.object = form.save()

        # render to response
        return self.render_to_response_json(context=self.get_context_json())

    def get_context_json(self):
        """
        Returns specific json context for ajax call.
        """
        post = self.request.POST
        form_class = self.get_form_class()
        context = {}

        if self.hidden_control_submit in post:
            if post[self.hidden_control_submit] == 'new':
                # form instance
                form = self.get_form(form_class=form_class, edit=False)
                # rederized form
                context['form'] = self.render_to_response(
                    self.get_context_data(form=form,
                                          action=self.get_action_url('save')
                                          )).content
            elif post[self.hidden_control_submit] == 'continue':
                # form instance
                form = self.get_form(form_class)
                # renderized form
                context['form'] = self.render_to_response(
                    self.get_context_data(form=form,
                                          action=self.get_action_url('edit')
                                          )).content
            elif post[self.hidden_control_submit] in EMPTY_VALUES:
                # render true success
                context['status'] = True
            else:
                # raise Exception error
                raise Exception('submit argument %s is not valid' %
                                (post[self.hidden_control_submit]))
        else:
            # render true success
            context['status'] = True

        reloads = self.get_json_context_list()
        if reloads:
            context['reloads'] = reloads

        return context

    def form_invalid(self, form):
        """
        If is invalid form returns errors.
        """
        context = self.get_context_data(form=form)
        form = self.render_to_response(context).content

        return self.render_to_response_json(
            context={'form': form,
                     'status': False})
