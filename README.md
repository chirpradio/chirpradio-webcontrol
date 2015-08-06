# CHIRPRADIO-WEBCONTROL

***

**WARNING**: This app is no longer supported. It has been superceded by
[chirpradio-manager](https://github.com/chirpradio/chirpradio-manager).


***

This is a web interface for running CLI scripts as detached subprocesses at the click of a button.

It uses the [EmberJS](http://emberjs.com/) framework on the client and the [Flask](http://flask.pocoo.org/) python web server to launch and moniter processes via [desub](http://desub.readthedocs.org/en/latest/index.html).

## Installation

- Create or activate a chirpradio-webcontrol virtualenv
- Make sure that you have [chirpradio-machine](https://github.com/chirpradio/chirpradio-machine)
  configured properly; install it into the virtualenv with
  `python setup.py develop`
- From the chirpradio-webcontrol directory, do `$ pip install -r requirements.txt`
- copy `settings_local-dist.py` to `settings_local.py`. Add any custom
  settings to it.

## Local Configuration

In `settings_local.py` you'll find the following options:

- LIVE_RUN_IS_AVAILABLE
	- Setting this to `True` allows the client to run scripts with side effects. If `False`, the client will only be offered read only processes. See the [Router](https://github.com/chirpradio/chirpradio-webcontrol/blob/develop/static/js/app.js#L119) for more info.
- DEBUG
	- Setting this to `True` enables pretty stack traces to result from server errors and causes the application router to log its activity in the browser console.
- TRAKTOR_PATH
	- The Traktor directory in your local environment; used when updating the traktor `.nml` file.

## Running WebControl

From the chirpradio-webcontrol directory, with the chirpradio-machine virtualenv activated, do

```
python server.py
```

## Understanding EmberJS

Ember is a relatively young JS MVC framework. It's tremendously powerful, concise, and convention-driven. But it also can be kind of hard to wrap your head around
how it works at first. And the official documentation isn't great yet (but it's getting better all the time!). So, if you want to read up on it, by far
the most useful resource I've encountered concerning Ember is Trek's [Advice on & Instruction in the Use Of Ember.js](http://trek.github.com/).
