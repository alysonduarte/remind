from django.template import RequestContext
from django.shortcuts import render_to_response
from remind.core.models import Event
from django.views.decorators.csrf import csrf_exempt
from remind.libs.dateutil.rrule import *

@csrf_exempt
def eventsXML(request):
    """
    For now, return the whole event DB.
    """
    eventList = Event.objects.all()

    return render_to_response('core/events.xml',
                              {'eventList' : eventList,},
                                mimetype="application/xhtml+xml")
@csrf_exempt
def dataprocessorXML(request):
    """
    QueryDict data format:
    <QueryDict:{
    u'ids': [u'1295982759946'],
    u'1295982759946_id': [u'1295982759946'],
    u'1295982759946_end_date': [u'2011-01-11 00:05'],
    u'1295982759946_text': [u'New event'],
    u'1295982759946_start_date': [u'2011-01-11 00:00'],
    u'1295982759946_!nativeeditor_status': [u'inserted']
    }>

    Response Data format:

    <data>
       <action type="some" sid="r2" tid="r2" />
       <action type="some" sid="r3" tid="r3" />
    </data>


    type
    the type of the operation (update, insert, delete, invalid, error);
    sid
    the original row ID (the same as gr_id);
    tid
    the ID of the row after the operation (may be the same as gr_id,
    or some different one - it can be used during a new row adding,
    when a temporary ID, created on the client-side, is replaced with the ID,
    taken from the DB or by any other business rule).

    """
    responseList = []
    
    if request.method == 'POST':

        idList = request.POST['ids'].split(',')
        
        for id in idList:
            command = request.POST[id + '_!nativeeditor_status']
            if command == 'inserted':
                e = Event()
                e.start_date = request.POST[id + '_start_date']
                e.end_date = request.POST[id + '_end_date']
                e.text = request.POST[id + '_text']
                e.details = 'Bogus for now'
                e.save()
                response = {'type' : 'insert',
                            'sid': request.POST[id + '_id'],
                            'tid' : e.id}

            elif command == 'updated':
                e = Event(pk=request.POST[id + '_id'])
                e.start_date = request.POST[id + '_start_date']
                e.end_date = request.POST[id + '_end_date']
                e.text = request.POST[id + '_text']
                e.details = 'Bogus for now'
                e.save()
                response = {'type' : 'update',
                            'sid': e.id,
                            'tid' : e.id}

                
            elif command == 'deleted':
                e = Event(pk=request.POST[id + '_id'])
                e.delete()
                response = {'type' : 'delete',
                            'sid': request.POST[id + '_id'],
                            'tid' : '0'}
                
            else:
                response = {'type' : 'error',
                            'sid': request.POST[id + '_id'],
                            'tid' : '0'}
                
            responseList.append(response)
            
    return render_to_response('core/dataprocessor.xml',
                              {"responseList": responseList}, 
                              mimetype="application/xhtml+xml")

@csrf_exempt
def calendar(request):
    return render_to_response('core/calendar.html', context_instance=RequestContext(request))