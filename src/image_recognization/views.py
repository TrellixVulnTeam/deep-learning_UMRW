from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from .mnist.cnn import test_cnn as cnn
from .mnist.logistic_regression import logistic_regression as logistic
from .mnist.multilayer import multilayer as mlp
import re, base64
from io import BytesIO

# Create your views here.

from .models import UploadDigitForm, UploadDigit
from .forms import Digit
# Create your views here.

def home(request):
    template_name = "home.html"
    context = {}
    return render(request, template_name, context)

def digit(request):
    if request.method == "POST":
        img = Digit(request.POST, request.FILES)
        if img.is_valid():
            type = request.POST.get('type')
            if type=='cnn':
                number = cnn.check_digit_cnn(request.FILES['pic'])
            elif type=='mlp':
                number = mlp.check_digit_mlp(request.FILES['pic'])
            else :
                number = logistic.check_digit_logistic(request.FILES['pic'])
            context = {"number": number[0], "form": img, 'type': type}
            return render(request,'digit/digit.html',context)
    else:
        img=Digit()
        type = request.GET['type']
        print(type,"this")
        context = {"number": "", "form": img, 'type': type}
    return render(request,'digit/digit.html',context)

# Added Function
def draw(request):
    if request.method == "POST":
        image_data = request.POST.get('canvas')
        image_data = re.sub("^data:image/png;base64,", "", image_data)
        image_data = base64.b64decode(image_data)
        image_data = BytesIO(image_data)
        #im = Image.open(image_data)
        type = request.POST.get('type')
        if type=='cnn':
            number = cnn.check_digit_cnn(image_data)
        elif type=='mlp':
            number = mlp.check_digit_mlp(image_data)
        else :
            number = logistic.check_digit_logistic(image_data)
        return render(request, 'digit/draw.html',{"number":number[0], 'type': type})
    else:
        type = request.POST.get('type')
        return render(request, 'digit/draw.html',{"number":"", 'type': type})

def cifar_10(request):
    if request.method == "POST":
        img = Digit(request.POST, request.FILES)
        if img.is_valid():
            #number = tmp.check_digit(request.FILES['pic'])
            #context = {"number": number[0], "form": img}
            return render(request,'image/cifar_10.html',context)
    else:
        img=Digit()
        context = {"image":None , "form": img}
    return render(request,'image/cifar_10.html',context)

def cifar_100(request):
    if request.method == "POST":
        img = Digit(request.POST, request.FILES)
        if img.is_valid():
            #number = tmp.check_digit(request.FILES['pic'])
            #context = {"number": number[0], "form": img}
            return render(request,'image/cifar_100.html',context)
    else:
        img=Digit()
        context = {"image":None , "form": img}
    return render(request,'image/cifar_100.html',context)