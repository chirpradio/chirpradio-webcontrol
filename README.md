# CHIRPRADIO-WEBCONTROL

This is a web interface for running CLI scripts as detached subprocesses at the click of a button.

It uses the EmberJS framework on the client and the Flask python web server.

Alpha version.

## Installation

- Create or activate a chirpradio-webcontrol virtualenv
- Make sure that you have [chirpradio-machine](https://github.com/chirpradio/chirpradio-machine)
  configured properly; install it into the virtualenv with
  `python setup.py develop`
- From the chirpradio-webcontrol directory, do `$ pip install -r requirements.txt`
- copy `settings_local-dist.py` to `settings_local.py`. Add any custom
  settings to it.

## Running WebControl

From the chirpradio-webcontrol directory, with the chirpradio-machine virtualenv activated, do

```
python server.py
```

## Understanding EmberJS

Ember is a relatively young JS MVC framework. It's tremendously powerful, concise, and convention-driven. But it also can be kind of hard to wrap your head around
how it works at first. And the official documentation isn't great yet (but it's getting better all the time!). So, if you want to read up on it, by far
the most useful resource I've encountered concerning Ember is Trek's [Advice on & Instruction in the Use Of Ember.js](http://trek.github.com/).
