from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

import time

# Create your views here.

def index(request):
	# DEBUG return HttpResponse("Index page <p>{% print(1) %}</p>")
	# DEBUG2 output = " | ".join(x*x for x in [1,2,3])
	# DEBUG2 return HttpResponse(output)

	timetemp = time.asctime(time.localtime())
	other_data = [timetemp]
	ticker_data = [["AAPL",39.91,67,33], ["GOOG",154.12,43.1,56.9], ["Third", 31.18, 90, 10]]

	template = loader.get_template('displaytable/index.html')
	context = {"other_data":other_data, "ticker_data":ticker_data}
	return HttpResponse(template.render(context, request))
