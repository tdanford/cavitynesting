from django.http import *
from django.shortcuts import render_to_response
from django.template import Context,loader

from cavitynesting.cavitydata.models import *
from cavitynesting.cavitydata.utils import *
from forms import *

from rdflib.Graph import Graph
from rdflib import *

import string

def top_level(request):
	c = Context({})
	t = loader.get_template('top_level.html')
	response = HttpResponse(t.render(c))
	return response

def tree_rdf(request,id):
	t = Tree.objects.get(id=id)
	store = ConjunctiveGraph()
	nanog = Namespace("http://nanog.csail.mit.edu/cavitynesting/rdf/")
	tree = URIRef(nanog['tree/%d' % string.atoi(id)])
	store.add((tree, RDF.type, nanog['tree']))
	serialized = store.serialize(format='nt')	
	response = HttpResponse(serialized)
	response.headers['Content-Type'] = 'text/plain'
	return response

