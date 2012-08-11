This is a web frontend to manage [CHIRP Radio's](http://chirpradio.org/)
digital music library. The backend is in
[chirpradio-machine](https://github.com/chirpradio/chirpradio-machine/).

CHIRP's digital music library is the heart and soul of the radio station
as it is used by live on-air DJs. The Music Dept will use this web frontend
to import new music.

# Install

Make sure you have [Python](http://python.org/) 2.6 or greater (excluding 3.x)
and [git](http://git-scm.com/).
The following instructions are for a Linux like OS, including Mac OS X.
On mac, we recommend the brew package manager, available at
[Homebrew](http://mxcl.github.com/homebrew/).

Install Python:

* Ubuntu: `apt-get install python`
* Mac: `brew install python`

Clone the chirpradio-webcontrol source and *all* its submodules:

    git clone --recursive git://github.com/chirpradio/chirpradio-webcontrol.git

Install the pip package manager for Python packages:

* Ubuntu: `apt-get install python-pip`
* Mac: `easy_install pip`

Install the virtualenv wrapper for convenience:

    pip install virtualenvwrapper

Create yourself a virtualenv to develop in:

    mkvirtualenv chirpradio-webcontrol

Once this is created you can activate it with:

    workon chirpradio-webcontrol

From within the virtualenv cd into the chirpradio-webcontrol source code
you cloned earlier. Install all dependencies like this:

    pip install -r requirements/project.txt

# The Machine

The [chirpradio-machine](https://github.com/chirpradio/chirpradio-machine)
is the source for all the command line utilities that handle music imports.
For convenience, this is included as a git submodule but you need to
install it into your virtualenv.

    pushd ./machine
    pip install -r requirements.txt
    python setup.py develop
    cp settings_local.py-dist settings_local.py
    popd

See
[chirpradio-machine docs](https://github.com/chirpradio/chirpradio-machine#readme)
for details on the installation / configuration process.
You'll need to edit some paths in settings_local.py to get it working.

To test that you have it installed right, run this in your virtualenv:

    which do_dump_new_artists_in_dropbox

That should print a path to the executable.

# Configuration

For customization, you can set
the following variables in settings/local_settings.py:

    CHIRPMACHINE = '/other/chirpmachine'
    CHIRPMACHINE_LIBRARY_DATA = '/other/chirpmachine/chirp/library/data'
    TRAKTOR_PATH = '/where/collection.nml/should/be/saved'

# Development

Now you can start up a development server:

    ./devserver

Visit the URL [http://0:8000/webcontrol/](http://0:8000/webcontrol/) and,
huzzah, you should see the music upload control panel.
