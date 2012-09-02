App = Em.Application.create();

App.DEBUG = ($('span').data('debug') === 'True') ? true : false;
App.LIVE_MODE_AVAILABLE = ($('span').data('live') === 'True') ? true : false;

App.Process = Em.Object.extend({
  name  : null,
  out   : null,
  err   : null,
  polling: false,
  done  : false,

  ready: function() { return !this.get('polling'); }.property('polling'),

  has_output: function() {
    return (this.get('out') || this.get('err')) ? true : false;
  }.property('out', 'err'),

  space_separated: function() {
    return this.get('name').replace(/-/g, ' ');
  }.property('name'),

  path: function() {
    return '/' + this.get('name');
  }.property('name'),

  polling_path: function() {
    return '/polling' + this.get('path');
  }.property('path'),

  parse_response: function(response) {
    (function(p, ctx) { return p ? null : ctx.set('polling', true); } )(this.get('polling'), this);
    this.set('out', response.out);
    this.set('err', response.err);
  },

  finished: function() {
    this.set('done', true);
    this.set('polling', false);
  }
});

App.ApplicationController = Em.ObjectController.extend({
  // Change this setting to enable the live run option.
  live_run_available: App.LIVE_MODE_AVAILABLE
});

App.ApplicationView = Em.View.extend({
  classNames  : ['wrapper'],
  templateName: 'app'
});

App.SplashView = Em.View.extend({
  classNames: 'splash',
  templateName: 'splash'
});

App.MainController = Em.ObjectController.extend({
  // set by router
  content   : null,
  processes : null,

  history: Em.View.extend({
    classNames: ['history'],
    templateName: 'history'
  }),

  start_button: Em.View.extend({
    templateName: 'start_button'
  }),

  messages: {
    'dump-new-artists-in-dropbox' :  'Carefully proofread the list of new artists. If they are all correct, proceed.',
    'do-periodic-import'          :  "Do not proceed if there are errors. If you can't resolve them, just move the culprit album aside temporarily.",
    'actually-do-periodic-import' :  'After you have completed this step, you can clean out the dropbox. Refer to the documentation.',
    'install-collection-nml'      :  'After this step has been completed, Traktor can be switched over to the new collection: Shut down Traktor, rename new-collection.nml to collection.nml and restart Traktor.'
  },

  // computed properties
  current_step_index: function() {
    return this.get('processes').indexOf(this.get('content.name'));
  }.property('content', 'processes'),

  next_step_name: function() {
    return this.get('processes')[this.get('current_step_index') + 1];
  }.property('processes', 'current_step_index'),

  available_steps: function() {
    var procs = this.get('processes').copy().splice(0, this.get('current_step_index'));
    return procs.map(function(name) { return App.Process.create({name: name}); });
  }.property('processes', 'current_step_index'),

  is_not_last: function() {
    return (this.get('current_step_index') !== this.get('processes').length - 1);
  }.property('current_step_index', 'processes'),

  message: function() {
    return this.get('messages')[this.get('content.name')] || false;
  }.property('content.name'),

  // methods
  step_is_available: function(step) {
    return this.get('processes').indexOf(step) < this.get('current_step_index');
  }
});

App.MainView = Em.View.extend({
  templateName: 'main'
});

var router = Em.Router.create({
  enableLogging: App.DEBUG,

  root: Em.Route.extend({

    splash: Em.Route.extend({
      route: '/',

      do_live: function(router) {
        var context = App.Process.create({name: 'dump-new-artists-in-dropbox'});
        router.get('mainController').set('processes', [
          "dump-new-artists-in-dropbox",
          "actually-dump-new-artists-in-dropbox",
          "diff-artist-whitelist",
          "commit-artist-whitelist",
          "push-artist-whitelist",
          "do-periodic-import",
          "actually-do-periodic-import",
          "generate-collection-nml",
          "install-collection-nml",
          "push-artists-to-chirpradio",
          "push-albums-and-tracks-to-chirpradio"
        ]);
        router.transitionTo('main', context);
      },

      serialize: function() {
        return '';
      },

      do_read_only: function(router) {
        var context = App.Process.create({name: 'dump-new-artists-in-dropbox'});
        router.get('mainController').set('processes', [
                "dump-new-artists-in-dropbox",
                "do-periodic-import"
        ]);
        router.transitionTo('main', context);
      },

      connectOutlets: function(router) {
        router.get('applicationController').connectOutlet('splash');
      }
    }),

    main: Em.Route.extend({
      route: '/:step',

      go_to_step: function(router, context) {
        router.transitionTo('main', App.Process.create({name: context.context}));
      },

      connectOutlets: function(router, context) {
        if (!router.get('mainController.processes')) {
          return router.transitionTo('splash');
        }
        router.get('applicationController').connectOutlet('main', context);
      },

      serialize: function(router, context) {
        if (context) {
          return { step: context.get('name') };
        }
      },

      deserialize: function(router, params) {
        return App.Process.create({ name: params.step });
      },

      // child states
      initialState: 'ready',

      ready: Em.Route.extend({
        route: '/',

        start_process: function(router, context) {
          router.transitionTo('polling');
          $.get(context.context.get('path'), function(response) {
            if (!response.started) context.context.set('err', response.err);
            router.send('poll', context.context);
          })
          .error(function(err) {
            if (App.DEBUG) {
              return $('html').html(err.responseText);
            }
            context.context.set('err', $(err.responseText).text());
          });
        }
      }),

      polling: Em.Route.extend({
        route: '/polling',

        poll: function(router, context) {
          $.get(context.get('polling_path'), function(response) {
            if (response.hasOwnProperty('server_error')) {
              context.set('err', response.server_error);
              context.finished();
              router.transitionTo('completed');
              return;
            }
            context.parse_response(response);
            if (response.is_done) {
              context.finished();
              router.transitionTo('completed');
            } else {
              router.send('poll', context);
            }
          })
          .error(function(err) {
            if (App.DEBUG) {
              return $('html').html(err.responseText);
            }
            context.set('err', $(err.responseText).text());
          });
        }
      }),

      completed: Em.Route.extend({
        route: '/done',

        start_process: function(router, context) {
          router.transitionTo('ready');
          router.send('start_process', context);
        },

        go_to_next_step: function(router) {
          var context = App.Process.create({name: router.get('mainController.next_step_name')});
          router.transitionTo('main', context);
        }
      })
    })
  })
});

App.initialize(router);
