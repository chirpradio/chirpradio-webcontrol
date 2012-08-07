from utils.render import render_to_response
from django.http import HttpResponse
import subprocess
import datetime

from django.conf import settings


def run_machine_command(command):
    # Command is a list
    p = subprocess.Popen([settings.CHIRPMACHINE_VIRTUALENV_COMMAND] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=settings.CHIRPMACHINE_BIN_DIR)
    out, err = p.communicate()

    if len(out) == 0 and len(err) == 0:
        out = 'No output'

    return out + err


def run_command(command, cwd=None):
    if not cwd:
        cwd = settings.CHIRPMACHINE_DIR
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = p.communicate()

    if len(out) == 0 and len(err) == 0:
        out = 'No output'

    return out + err


def control_panel(request):
    return render_to_response('webcontrol/control-panel.html', locals())


def do_dump_new_artists_in_dropbox(request):
    if request.method == 'POST':
        out = run_machine_command(['do_dump_new_artists_in_dropbox.py', '--rewrite'])
        rewrote = True
    else:
        out = run_machine_command(['do_dump_new_artists_in_dropbox.py'])

    return render_to_response('webcontrol/do_dump.html', locals())


def diff_whitelist(request):
    if request.method == 'POST':
        out = run_command(['git', 'commit', 'artist-whitelist', '-m', 'Adding new artists'], cwd = settings.CHIRPMACHINE_LIBRARY_DATA)
        if not settings.DEBUG:
            out += run_command(['git', 'push'], cwd = settings.CHIRPMACHINE_LIBRARY_DATA)
        pushed = True
    else:
        out = run_command(['git', 'diff', 'artist-whitelist'], cwd = settings.CHIRPMACHINE_LIBRARY_DATA)

    return render_to_response('webcontrol/diff_whitelist.html', locals())


def do_import(request):
    if request.method == 'POST':
        out = run_machine_command(['do_periodic_import.py', '--actually-do-import'])
        imported = True
    else:
        out = run_machine_command(["do_periodic_import.py", "2>&1"])
        checked = True

    return render_to_response('webcontrol/do_import.html', locals())


def do_backup(request):
    raise NotImplementedError


def generate_collection(request):
    if request.method == 'GET':
        out = run_machine_command(['do_generate_collection_nml.py'])
        out += run_command(['install', '-m', '0775', '-g', 'traktor', 'output.nml', settings.TRAKTOR_PATH + '/new-collection.nml'],
            cwd=settings.CHIRPMACHINE_BIN_DIR)

    return render_to_response('webcontrol/generate_collection.html', locals())


def push_artists(request):
    if request.method == 'POST':
        out = run_machine_command(['do_push_artists_to_chirpradio.py'])
        artists_pushed = True
    else:
        timestamp = ''.join(datetime.date.today().isoformat().split('-')) + '-000000'
        out = run_machine_command(['do_push_to_chirpradio.py', '--start-at=' + timestamp])
        finished = True
    return render_to_response('webcontrol/push_artists.html', locals())
