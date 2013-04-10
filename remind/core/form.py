# coding: UTF-8

from django import forms
from remindcalendar.core.models import RecipeEvent

class EventForm(forms.ModelForm):
    
    rec_type = dict()
    
    def __init__(self, id, data, *args, **kwargs):
        datas = dict()
        for key, value in data.items():
            datas.update({key.replace(id + "_", ""): value})
        kwargs['data'] = datas
        super(EventForm, self).__init__(*args, **kwargs)
        
        if "rec_type" in self.data:
            self.rec_type = self._meta.model.decode_rec(self.data['rec_type'])
    
    def clean_type(self):
        return self.rec_type['type'] if self.rec_type.has_key("type") else None
    
    def clean_count(self):
        return int(self.rec_type['count']) if self.rec_type['count'] != '' else None \
            if self.rec_type.has_key("count") else None
    
    def clean_day(self):
        return int(self.rec_type['day']) if self.rec_type['day'] != '' else None \
            if self.rec_type.has_key("day") else None
    
    def clean_count2(self):
        return int(self.rec_type['count2']) if self.rec_type['count2'] != '' else None \
            if self.rec_type.has_key("count2") else None
    
    def clean_days(self):
        return self.rec_type['days'] if self.rec_type.has_key("days") else None
    
    def clean_extra(self):
        return self.rec_type['extra'] if self.rec_type.has_key("extra") else None
        
    class Meta:
        model = RecipeEvent
    