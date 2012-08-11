import datetime
import os
import subprocess

from django.conf import settings
from django.http import HttpResponse

from utils.render import render_to_response


def cmd_exists(name):
    """
    Return the actual path to a named command.

    The first one on $PATH wins. If it's not on $PATH, None is returned.
    """
    for pt in os.environ.get('PATH', '').split(':'):
        candidate = os.path.join(pt, name)
        if os.path.exists(candidate):
            return candidate


def run_machine_command(command):
    # Command is a list
    if not cmd_exists(command[0]):
        raise EnvironmentError('The executable for %r does not exist. '
                               'Have you installed chirpradio-machine in your '
                               'virtualenv?' % command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()

    if len(out) == 0 and len(err) == 0:
        out = 'No output'

    return out + err


def run_command(command, cwd=None):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
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
    if request.method == 'POST':
        out = run_machine_command(['do_periodic_import', '--actually-do-import'])
        imported = True
    else:
        out = run_machine_command(["do_periodic_import"])
        checked = True

    return render_to_response('webcontrol/do_import.html', locals())


def do_backup(request):
    raise NotImplementedError


def generate_collection(request):
    if request.method == 'GET':
        out = run_machine_command(['do_generate_collection_nml'])
        out += run_command(['install', '-m', '0775', '-g', 'traktor', 'output.nml', settings.TRAKTOR_PATH + '/new-collection.nml'],
            cwd=settings.CHIRPMACHINE_BIN_DIR)

    return render_to_response('webcontrol/generate_collection.html', locals())


def push_artists(request):
    if request.method == 'POST':
        out = run_machine_command(['do_push_artists_to_chirpradio'])
        artists_pushed = True
    else:
        timestamp = ''.join(datetime.date.today().isoformat().split('-')) + '-000000'
        out = run_machine_command(['do_push_to_chirpradio', '--start-at=' + timestamp])
        finished = True
    return render_to_response('webcontrol/push_artists.html', locals())
