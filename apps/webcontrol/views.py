from utils.render import render_to_response

def control_panel(request):
    return render_to_response('webcontrol/control-panel.html', locals())

def do_dump_new_artists_in_dropbox(request):
    raise NotImplementedError

def diff_whitelist(request):
    raise NotImplementedError

def commit_whitelist(request):
    raise NotImplementedError

def do_import(request):
    raise NotImplementedError

def do_backup(request):
    raise NotImplementedError

def generate_collection(request):
    raise NotImplementedError

def push_artists(request):
    raise NotImplementedError

