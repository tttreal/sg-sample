from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):

    def __init__(self):
        self.params = {
            'title':'hello',
            'message':'your data ...',
            #'form':SessionForm(),
            'result':None,
        }

    def get(self, request):
        self.params['result'] = request.session.get('last_msg', 'no message')
        self.params['message'] = ''
        for k in request.session.keys():
            self.params['message'] = self.params['message'] + str(k) + ":" + str(request.session[k]) + "\n"
        return render(request, 'game/index.html', self.params)

    def post(self, request):
        ses = request.POST['session']
        self.params['result'] = 'send: "' + ses + '"'
        request.session['last_msg'] = ses
        #msg = 'you are <b>' + request.POST['name'] + '(' + request.POST['age'] + ')' + '   ' + request.POST['mail']
        #self.params['message'] = msg
        #self.params['form'] = HelloForm(request.POST)
        #self.params['form'] = SessionForm(request.POST)
        return render(request, 'game/index.html', self.params)

def index(request):
    params = {}
    return render(request, 'game/index.html', params)

#def index(request, id, nickname):
def index2(request):
    #if 'msg' in request.GET:
    #    msg = request.GET['msg']
    #else:
    #    msg = "def"

    ##res = "res " + str(id) + " " + nickname
    #res = msg

    #a = 'aa'
    #params = {
    #    'title': "aaa",
    #    a : 32,
    #    'goto' : 'next',
    #    'form': 'form',
    #}

    #return HttpResponse("Hello Django!" + msg)



    params = {
        'title' : 'hello',
        'message' : 'your data:',
        #'form' : HelloForm(),
    }

    if request.method == "POST":
        params['message'] = '名前: ' + request.POST['name'] + \
            ', mail: ' + request.POST['mail'] + \
            ', age: ' + request.POST['age'] 
        #params['forms'] = HelloForm(request.POST)




    return render(request, 'game/index.html', params)
