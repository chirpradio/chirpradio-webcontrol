from django import template

register = template.Library()

@register.inclusion_tag('webcontrol/sidemenu.html', takes_context = True)
def artist_import_menu(context):
    request = context['request']

    def step(view_name):
        if view_name == 'control_panel':
            return 0
        if view_name == 'do_dump_new_artists_in_dropbox':
            return 1
        if view_name == 'diff_whitelist':
            return 2
        if view_name == 'commit_whitelist':
            return 3
        if view_name == 'do_import':
            return 4
        if view_name == 'do_backup':
            return 5
        if view_name == 'generate_collection':
            return 6
        if view_name == 'push_artists':
            return 7

        raise ValueError, 'View name %s is unknown' %(view_name)

    return {'step':step(request.view_name.split('.')[-1])}
