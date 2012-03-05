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

* Ubuntu: `apt-get install virtualenvwrapper`
* Mac: follow the [instructions here](http://www.doughellmann.com/docs/virtualenvwrapper/)

Create yourself a virtualenv to develop in:

    mkvirtualenv chirpradio-webcontrol

Once this is created you can activate it with:

    workon chirpradio-webcontrol

From within the virtualenv cd into the chirpradio-webcontrol source code
you cloned earlier. Install all dependencies like this:

    pip install -r requirements/project.txt

Now you can start up a development server:

    ./devserver

Visit the URL [http://0:8000/webcontrol/](http://0:8000/webcontrol/) and,
huzzah, you should see the music upload control panel.
