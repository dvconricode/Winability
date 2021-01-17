from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import time

from .forms import TickerForm

# Create your views here. 

##############

##############

timetemp = time.asctime(time.localtime())  # updates every refresh
other_data = [timetemp]
ticker_data = [["AAPL",39.91,67,33], ["GOOG",154.12,43.1,56.9], ["Third", 31.18, 90, 10]]

def index(request):
	# DEBUG return HttpResponse("Index page <p>{% print(1) %}</p>")
	# DEBUG2 output = " | ".join(x*x for x in [1,2,3])
	# DEBUG2 return HttpResponse(output)

	template = loader.get_template('displaytable/index.html')
	context = {"other_data":other_data, "ticker_data":ticker_data}
	return HttpResponse(template.render(context, request))



def get_ticker(request):
		if request.method == 'POST':
			form = TickerForm(request.POST)
			if True:
				template = loader.get_template('displaytable/search.html')
				context = {'ticker': request.POST['ticker']} #gotta get the ticker from the form
				my_search = context['ticker']  # the ticker we search for
				results_list = []
				for each_list in ticker_data:
					if my_search in each_list[0]:
						results_list.append(each_list)
				if results_list != []:  # 
					context.update({"ticker_data":results_list})
				return HttpResponse(template.render(context, request))
			#print(form.errors)
			#return HttpResponse('test')

