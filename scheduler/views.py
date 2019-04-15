"""Views gathering point"""
import os.path
import datetime
import pandas as pd
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import default_storage
from django.template import loader
import scheduler.import_handlers as imp
from .forms import SelectAuditoriumForm
from django.contrib import messages
import scheduler.conflicts as conflicts
from scheduler.models import Auditorium, Lesson, Professor, Group


def index(_request: HttpRequest) -> HttpResponse:
    """Render the main page"""
    return render(_request, 'index.html')


def upload(request: HttpRequest) -> HttpResponse:
    """Render file upload page"""
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        if isinstance(myfile.name, str):
            ext = os.path.splitext(myfile.name)[1]
            if ext == '.csv':
                filename = default_storage.save(myfile.name, myfile)
                data = pd.read_csv(myfile.name)
                default_storage.delete(filename)
            elif ext == '.xlsx':
                filename = default_storage.save(myfile.name, myfile)
                data = pd.read_excel(myfile.name)
                default_storage.delete(filename)
            else:
                return render(request, "upload.html", {'error': "Extension not supported"})
            added_lessons, incorrect, duplicate = imp.parse_data(data, ext)
            data_html = data.to_html(classes=["table-bordered", "table-striped", "table-hover"],
                                     justify='center')
            context = {'loaded_data': data_html, 'added': added_lessons,
                       'incorrect': incorrect, 'duplicate': duplicate}
            return render(request, "upload.html", context)
    return render(request, "upload.html")


def show_rooms_schedule(request: HttpRequest) -> HttpResponse:
    """Render the auditorium schedule page"""
    rooms = Auditorium.objects.all()
    if_chosen = False
    room_number = None
    if request.method == 'POST':
        form = SelectAuditoriumForm(request.POST)
        if form.is_valid():
            room_number = form.cleaned_data['auditorium']
            messages.success(request, 'Communicate successfully sent!')
            if_chosen = True
        else:
            return HttpResponse("WHAT ARE YOU DOING?")
    else:
        form = SelectAuditoriumForm()
    context = {
        'range': range(len(rooms)),
        'form': form,
        'flag': if_chosen,
        'room_no': room_number,
        'lessons': Lesson.objects.all()
    }
    return render(request, "room_schedule.html", context)


def confs(request: HttpRequest) -> HttpResponse:
    """Render the conflicts page"""
    template = loader.get_template('conflicts.html')
    conflicts_list = conflicts.db_conflicts()
    color = ''
    context = {
        'conflicts': conflicts_list,
        'color': color,
    }
    return HttpResponse(template.render(context, request))


def show_proferssors_schedule(request: HttpRequest) -> HttpResponse:
    professor_id = Professor.objects.filter(name="Sergiusz", surname="Orlowski")

    professors_lessons_query = Lesson.objects.filter(professor__in=professor_id).order_by('start_time')
    professors_lessons_list = [(q.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                                q.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                                q.name,
                                Auditorium.objects.filter(id=q.auditorium_id)[:1].get().number,
                                Group.objects.filter(id=q.group_id)[:1].get().number)
                               for q in professors_lessons_query]

    start_date = datetime.datetime.now()
    for d in professors_lessons_query:
        if (d.start_time > start_date):
            start_date = d.start_time
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%S")
    print(start_date_str)
    context = {
        'professor': 'Sergiusz Orlowski',
        'events': professors_lessons_list,
        'start_date': start_date_str
    }
    return render(request, "professors_scheduler.html", context)
