from flask import Flask, redirect, url_for, jsonify
from werkzeug import SharedDataMiddleware
import sys
import datetime
import desub
import os

# equivalent to `$ which python` in the chirpradio-machine dir on your machine
CHIRPMACHINE_VIRTUALENV_COMMAND = '/Users/trevorborg/workspace/chirp/chirpradio-machine/ENV-machine/bin/python'
# [path/to/chirpradio-machine]/chirp/library
CHIRPMACHINE_BIN_DIR = '/Users/trevorborg/workspace/chirp/CHIRP-ENV/bin/'
CHIRPMACHINE_LIBRARY_DATA = '~/workspace/chirp/chirpradio-machine/chirp/library/data/'
TRAKTOR_PATH = '/Users/trevorborg/fake-traktor'

PROCESS_ARGUMENTS = {
    # Truth in the value tuple signifies that this is a chirpmachine script
    "dump-new-artists-in-dropbox": (['do_dump_new_artists_in_dropbox'], True),
    "actually-dump-new-artists-in-dropbox": (['do_dump_new_artists_in_dropbox', '--rewrite'], True),
    "do-periodic-import": (['do_periodic_import'], True),
    "actually-do-periodic-import": (['do_periodic_import', '--actually-do-import'], True),
    "generate-collection-nml": (['do_generate_collection_nml'], True),
    "push-artists-to-chirpradio": (['do_push_artists_to_chirpradio'], True),
    "push-albums-and-tracks-to-chirpradio": (['do_push_to_chirpradio.py'], True),
    "diff-artist-whitelist": (['git', 'diff', 'artist-whitelist'], False),
    "commit-artist-whitelist": (['git', 'commit', 'artist-whitelist', 'm', 'Adding new artists'], False),
    "push-artist-whitelist": (['git', 'push'], False),
    "install-collection-nml": (['install', '-m', '0775', '-g', 'traktor', 'output.nml', TRAKTOR_PATH + '/new-collection.nml'], False)
}

PROCESS_MESSAGES = {
    # process-specific commentary you may want to share with the user goes here
    'dump-new-artists-in-dropbox': 'Carefully proofread the list of new artists. If they are all correct, proceed.',
    'do-periodic-import': "Do not proceed if there are errors. If you can't resolve them, just move the culprit album aside temporarily.",
    'actually-do-periodic-import': 'After you have completed this step, you can clean out the dropbox. Refer to the documentation.',
    'install-collection-nml': 'After this step has been completed, Traktor can be switched over to the new collection: Shut down Traktor, rename new-collection.nml to collection.nml and restart Traktor.'
}

app = Flask(__name__)

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/': os.path.join(os.path.dirname(__file__), 'static')
})


@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))


@app.route('/<process_name>')
def start_process(process_name):
    args, is_machine_cmd = PROCESS_ARGUMENTS.get(process_name, (False, False))
    message = PROCESS_MESSAGES.get(process_name, False)
    if args:
        if is_machine_cmd:
            if process_name == 'push-albums-and-tracks-to-chirpradio':
                # this is the only case that requires a run-time variable
                timestamp = ''.join(datetime.date.today().isoformat().split('-')) + '-000000'
                args.append('--start-at=' + timestamp)
            proc = desub.join(args, cwd=CHIRPMACHINE_BIN_DIR)
        else:
            if process_name == 'install-collection-nml':
                proc = desub.join(args, cwd=CHIRPMACHINE_BIN_DIR)
            else:
                proc = desub.join(args, cwd=CHIRPMACHINE_LIBRARY_DATA)
        if proc.is_running():
            return jsonify({'started': False, 'error': 'process is already running'})
        else:
            proc.start()
            return jsonify({'started': True, 'message': message})
    else:
        return jsonify({'started': False, 'error': 'unrecognized process name: ' + process_name})


@app.route('/polling/<process_name>')
def poll(process_name):
    args, is_machine_cmd = PROCESS_ARGUMENTS.get(process_name, (False, False))
    if args:
        if is_machine_cmd:
            if process_name == 'push-albums-and-tracks-to-chirpradio':
                # this could potentially backfire if you happen to start the process in
                # the moments before midnight. I would be open to a better way.
                timestamp = ''.join(datetime.date.today().isoformat().split('-')) + '-000000'
                args.append('--start-at=' + timestamp)
            proc = desub.join(args, cwd=CHIRPMACHINE_BIN_DIR)
        else:
            if process_name == 'install-collection-nml':
                proc = desub.join(args, cwd=CHIRPMACHINE_BIN_DIR)
            else:
                proc = desub.join(args, cwd=CHIRPMACHINE_LIBRARY_DATA)
        if proc.is_running():
            return jsonify({'err': proc.stderr.read(), 'out': proc.stdout.read(), 'is_done': False})
        else:
            return jsonify({'err': proc.stderr.read(), 'out': proc.stdout.read(), 'is_done': True})
    else:
        return jsonify({'started': False, 'error': 'unrecognized process name: ' + process_name})

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            app.run(debug=True)
    else:
        app.run()
