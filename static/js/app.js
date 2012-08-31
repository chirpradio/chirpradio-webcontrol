App = Em.Application.create();

App.Process = Em.Object.extend({
        name: null,
        out: null,
        err: null,
        message: null,
        done: false,

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
                this.set('out', response.out);
                this.set('err', response.err);
        }
});

App.ApplicationController = Em.ObjectController.extend({
        live_run_available: false
});

App.ApplicationView = Em.View.extend({
        classNames: ['wrapper'],
        templateName: 'app'
});

App.SplashView = Em.View.extend({
        templateName: 'splash'
});

App.MainController = Em.ObjectController.extend({
        // set by router
        content: null,
        processes: null,

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

        // methods
        step_is_available: function(step) {
                return this.get('processes').indexOf(step) < this.get('current_step_index');
        }
});

App.MainView = Em.View.extend({
        templateName: 'main'
});

var router = Em.Router.create({
        enableLogging: true,

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
                                return { step: context.get('name') };
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
                                                        context.context.set('message', response.message);
                                                        router.send('poll', context.context);
                                        });

                                }
                        }),

                        polling: Em.Route.extend({
                                route: '/polling',

                                poll: function(router, context) {
                                        $.get(context.get('polling_path'), function(response) {
                                                context.parse_response(response);
                                                if (response.is_done) {
                                                        context.set('done', true);
                                                        router.transitionTo('completed');
                                                } else {
                                                        router.send('poll', context);
                                                }
                                        });
                                },

                                complete_process: Em.Route.transitionTo('completed')
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
