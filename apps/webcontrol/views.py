from utils.render import render_to_response
from django.http import HttpResponse
import subprocess

from django.conf import settings

def run_machine_command(command):
    # Command is a list
    p = subprocess.Popen([settings.CHIRPMACHINE_VIRTUALENV_COMMAND] + command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd = settings.CHIRPMACHINE_BIN_DIR)
    out, err = p.communicate()

    if len(out) == 0 and len(err) == 0:
        out = 'No output'

    return out + err

def run_command(command, cwd = None):
    if not cwd:
        cwd = settings.CHIRPMACHINE_DIR
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd = cwd)
    out, err = p.communicate()

    if len(out) == 0 and len(err) == 0:
        out = 'No output'

    return out + err

def control_panel(request):
    return render_to_response('webcontrol/control-panel.html', locals())

def do_dump_new_artists_in_dropbox(request):
    if request.method == 'POST':
        out = run_machine_command(['do_dump_new_artists_in_dropbox', '--rewrite'])
        rewrote = True
    else:
        out = run_machine_command(['do_dump_new_artists_in_dropbox'])

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
    raise NotImplementedError

def do_backup(request):
    raise NotImplementedError

def generate_collection(request):
    raise NotImplementedError

def push_artists(request):
    raise NotImplementedError

