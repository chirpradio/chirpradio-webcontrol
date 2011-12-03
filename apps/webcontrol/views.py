from utils.render import render_to_response

def control_panel(request):
    return render_to_response('two-column.html', locals())
