from django.http import *
from django.shortcuts import render_to_response
from django.template import Context,loader

from cavitynesting.cavitydata.models import *
from cavitynesting.cavitydata.utils import *
from forms import *

import random

def top_level(request):
	c = Context({})
	t = loader.get_template('top_level.html')
	response = HttpResponse(t.render(c))
	return response

## the updates.html page is the separate page where I put 
## specific notes about updates I've made to the system as 
## it's running. 

def updates_view(request):
	c = Context({})
	t = loader.get_template('updates.html')
	response = HttpResponse(t.render(c))
	return response

def input_all_defaults():
	NestFate().input_defaults()
	NestStatus().input_defaults()
	NestStage().input_defaults()
	NestFindMethods().input_defaults()
	CavityLocations().input_defaults()
	DecayClass().input_defaults()
	TreeSpecies().input_defaults()
	BirdSpecies().input_defaults()

def input_defaults_handler(request):
	input_all_defaults()
	return HttpResponseRedirect('/cavitynesting/')

random_choices = ['http://www.surveymonkey.com/s.aspx?sm=TySc2_2bXASSEVqZXjwEb6wA_3d_3d', 'http://www.surveymonkey.com/s.aspx?sm=ELe7mdPzJ0kYJuaHfE856g_3d_3d']

def tree_survey_view(request):
	idx = random.choice(range(len(random_choices)))
	dict = {}
	dict['href'] = random_choices[idx]
	c = Context(dict)
	t = loader.get_template('survey.html')
	response = HttpResponse(t.render(c))
	return response

def random_view(request):
	idx = random.choice(range(len(random_choices)))
	return HttpResponseRedirect(random_choices[idx])	

## General Purpose Helper Methods #########################################

# should work for Tree, RandomTree, and TransectTree instances.
def tree_hazard_value(tree):
	pt = tree.hazard_probtarget
	ds = tree.hazard_defectivesize
	pf = tree.hazard_probfail
	sr = tree.hazard_speciesrating
	if not pt: pt = 0
	if not ds: ds = 0
	if not pf: pf = 0
	if not sr: sr = 0
	return pt + ds + pf + sr

def next_transectnumber(plot_id):
	transects = [t for t in Transect.objects.filter(plot=plot_id)]
	if len(transects) == 0: 
		return 1
	return max([t.transectnumber for t in transects]) + 1

def next_transecttreeid():
	tts = TransectTree.objects.all()
	num = len(tts) + 1
	treeid = '#%03d' % num
	while len(TransectTree.objects.filter(treeid=treeid)) > 0:
		num += 1
		treeid = '#%d' % num
	return treeid

## Index Handlers ########################################################

## These handlers are used to set up the "index" views, which list 
## *all* the values in a given model/table.  
## They also handle output in alternate formats, i.e., CSV tables.  

def generic_index(request,objclass,index_stub,orderfield):
	if request.method == 'GET':
		if orderfield != None:
			all_values = objclass.objects.all().order_by(orderfield)
		else:
			all_values = objclass.objects.all()
		c = Context({ 'all_values' : all_values })
		index_page = '%s.html' % index_stub
		headers = {}
		if 'type' in request.GET and request.GET['type'] == 'csv':
			index_page = '%s.csv' % index_stub
			headers['Content-Type'] = 'text/plain'
		t = loader.get_template(index_page)
		response = HttpResponse(t.render(c))

		for k in headers.keys(): response[k] = headers[k]

		return response
	else:
		return HttpResponseRedirect('/cavitynesting/')

def plot_nest_view(request):
	if request.method != 'GET': return HttpResponseRedirect('/cavitynesting/')
	plots = Plot.objects.all().order_by('plotid')
	nest_counts = []
	for p in plots: 
		nc = 0
		for t in p.tree_set.all():
			cs = t.cavity_set.all()
			for c in cs:
				nc += len(c.nest_set.all())
		nest_counts.append([p, nc])
	params = {}
	params['plot_counts'] = nest_counts
	c = Context(params)
	index_page = 'plot_nest_counts.html'
	t = loader.get_template(index_page)
	response = HttpResponse(t.render(c))
	return response

def new_plot_nest_view(request):
	if request.method != 'GET': return HttpResponseRedirect('/cavitynesting/')
	nest_counts = plot_nest_query()
	params = {}
	params['plot_counts'] = nest_counts
	c = Context(params)
	index_page = 'plot_nest_counts.html'
	t = loader.get_template(index_page)
	response = HttpResponse(t.render(c))
	return response

def plot_nest_query():
	from django.db import connection
	cursor = connection.cursor()
	cursor.execute('select p.id, p.plotid, count(*) from cavitydata_plot p, cavitydata_tree t, cavitydata_cavity c, cavitydata_nest n where t.plot_id=p.id and c.tree_id=t.id and n.cavity_id=c.id group by p.plotid order by p.plotid', [])
	values = cursor.fetchall()
	return values

def global_index(request):
	if request.method == 'GET':
		ntrees = Tree.objects.all().order_by('treeid')
		random_trees = RandomTree.objects.all().order_by('treeid')
		transect_trees = TransectTree.objects.all().order_by('treeid')
		nest_trees = []
		for t in ntrees:
			cs = t.cavity_set.all()
			if len(cs) == 0:
				nest_trees.append({ 't' : t, 'c' : None, 'n' : None })
			else:
				for c in cs: 
					ns = c.nest_set.all()
					if len(ns) == 0:
						nest_trees.append({'t' : t, 'c' : c, 'n' : None})
					else:
						for n in ns: 
							nest_trees.append({'t' : t, 'c' : c, 'n' : n})
		params = {}
		params['nest_trees'] = nest_trees
		params['random_trees'] = random_trees
		params['transect_trees'] = transect_trees
		c = Context(params)

		index_page = 'global_index.csv'
		headers = {}
		headers['Content-Type'] = 'text/plain'
		t = loader.get_template(index_page)
		response = HttpResponse(t.render(c))
		for k in headers.keys(): response[k] = headers[k]
		return response
	else:
		return HttpResponseRedirect('/cavitynesting/')

def plot_bird_species_table(request):
	if request.method == 'GET':
		all_plots = Plot.objects.all().order_by('plotid')
		all_species = BirdSpecies.objects.all().order_by('name')
		value_list = []
		for p in all_plots:
			pcounts = p.bird_species_count()
			counts = [] 
			for s in all_species:
				if pcounts.has_key(s):
					counts.append(pcounts[s])
				else:
					counts.append(0)
			value_list.append({ 'plot' : p, 'counts' : counts })
		d = { 'species' : [s for s in all_species], 'plots' : value_list }
		c = Context(d)

		index_stub = 'plot_bird_species_table'
		index_page = '%s.html' % index_stub
		headers = {}
		if 'type' in request.GET and request.GET['type'] == 'csv':
			index_page = '%s.csv' % index_stub
			headers['Content-Type'] = 'text/plain'
		t = loader.get_template(index_page)
		response = HttpResponse(t.render(c))
		for k in headers.keys(): response[k] = headers[k]
		return response
	else:	
		return HttpResponseRedirect('/cavitynesting/')

def tree_species_index(request):
	if request.method == 'GET':
		all_species = TreeSpecies.objects.all().order_by('name')
		all_values = []
		for species in all_species:
			nests = Tree.objects.filter(species=species.id).count()
			randoms = RandomTree.objects.filter(species=species.id).count()
			transects = TransectTree.objects.filter(species=species.id).count()
			all_values.append({'id':species.id, 'name' : species.name, 'nests' : nests, 'randoms' : randoms, 'transects':transects })
		value_dict = { 'all_values' : all_values } 
		c = Context(value_dict)
		index_page = '%s.html' % 'tree_species_index'
		t = loader.get_template(index_page)
		return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect('/cavitynesting/')

def transect_tree_index(request):
	if request.method == 'GET':
		all_values = TransectTree.objects.all().order_by('treeid', 'treeorder')
		c = Context({ 'all_values' : all_values })
		index_page = '%s.html' % 'transect_tree_index'
		headers = {}
		if 'type' in request.GET and request.GET['type'] == 'csv':
			index_page = '%s.csv' % 'transect_tree_index'
			headers['Content-Type'] = 'text/plain'
		t = loader.get_template(index_page)
		response = HttpResponse(t.render(c))
		for k in headers.keys(): response[k] = headers[k]
		return response
	else:
		return HttpResponseRedirect('/cavitynesting/')

def plot_index(request):
	return generic_index(request,Plot,'plot_index','plotid')

def transect_index(request):
	return generic_index(request,Transect,'transect_index','plot')

def tree_index(request):
	return generic_index(request,Tree,'tree_index','treeid')

def random_tree_index(request):
	return generic_index(request,RandomTree,'random_tree_index','treeid')

def cavity_index(request):
	return generic_index(request,Cavity,'cavity_index','cavityid')

def nest_index(request):
	return generic_index(request,Nest,'nest_index','nestid')

def visit_index(request):
	return generic_index(request,Visit,'visit_index','date')

## Entry Handlers ################################################################

## These handlers control the creation of, and the handling of the POST-values 
## from, the forms which are used to create an entirely new entity.  
## The equivalent forms, but for the *modification* of existing entries, are 
## handled in the "View and Modification Handlers" section below.

def entry_handler(request,formclass,formtitle,urlstub,parentkey=None):
	if request.method=='POST':
		form=formclass(request.POST)
		if form.is_valid():
			value=form.create_value()			
			value.save()
			url = '/cavitynesting/%s/%s/' % (urlstub, value.id)
			return HttpResponseRedirect(url)
	elif request.method == 'GET' and (parentkey == None or parentkey in request.GET):
		initial_dict = {}
		if parentkey != None: 
			debug('Parent Key: %s' % str(request.GET[parentkey]))
			parentvalue = request.GET[parentkey]
			initial_dict = { parentkey : int(parentvalue) } 
		else: 
			debug('No parent key: %s' % formtitle)
			parentvalue = None
		debug('Initial Values: %s' % initial_dict)
		form = formclass(initial_dict)
	else:
		return HttpResponseRedirect('/cavitynesting/')
	dict = { 'formtitle' : formtitle, 'form' : form, 'buttontitle' : 'Add' } 
	return render_to_response('form_template.html', dict)

# We're not using the generic template here, because transects have to be ordered
# with Transect Number in a certain way.  

#def transect_entry(request):
	#return entry_handler(request,TransectForm,'Transect','transect', 'plot')

def transect_entry(request):
	preamble = ''
	if request.method=='POST':
		form=TransectForm(request.POST)
		if form.is_valid():
			value=form.create_value()			
			value.save()
			url = '/cavitynesting/%s/%s/' % ('transect', value.id)
			return HttpResponseRedirect(url)
	elif request.method == 'GET' and ('plot' in request.GET):
		parentvalue = int(request.GET['plot'])
		debug('parentvalue: %d' % parentvalue)
		next_num = next_transectnumber(parentvalue)
		preamble = '''
		<tr>
		<th><b>Transect Number</b>:</th>
		<td>%d</td>
		</tr> 
		'''
		preamble = preamble % next_num
		initial_dict = { 'plot' : parentvalue, 'transectnumber' : next_num } 
		debug('Initial Values: %s' % initial_dict)
		form = TransectForm(initial_dict)
	else:
		return HttpResponseRedirect('/cavitynesting/')
	dict = { 'formtitle' : 'Transect', 'form' : form, 'buttontitle' : 'Add', 'preamble' : preamble } 
	return render_to_response('form_template.html', dict)

def random_tree_entry(request):
	preamble = ''
	if request.method=='POST':
		form=RandomTreeForm(request.POST)
		if form.is_valid():
			value=form.create_value()			
			value.save()
			url = '/cavitynesting/%s/%s/' % ('randomtree', value.id)
			return HttpResponseRedirect(url)
	elif request.method == 'GET' and ('tree' in request.GET):
		parentvalue = int(request.GET['tree'])
		debug('parentvalue: %d' % parentvalue)
		parent_tree = Tree.objects.get(id=parentvalue)
		random_treeid = '%sR' % parent_tree.treeid
		preamble = '''
		<tr>
		<th>Tree ID:</th>
		<td>%s</td>
		</tr> 
		'''
		preamble = preamble % random_treeid
		initial_dict = { 'plot' : parentvalue, 'treeid' : random_treeid, 'tree' : parentvalue } 
		debug('Initial Values: %s' % initial_dict)
		form = RandomTreeForm(initial_dict)
	else:
		return HttpResponseRedirect('/cavitynesting/')
	dict = { 'formtitle' : 'Random Tree', 'form' : form, 'buttontitle' : 'Add', 'preamble' : preamble } 
	return render_to_response('form_template.html', dict)

def transect_tree_entry(request):
	preamble = ''
	if request.method=='POST':
		form=TransectTreeForm(request.POST)
		if form.is_valid():
			value=form.create_value()			
			value.save()
			url = '/cavitynesting/%s/%s/' % ('transecttree', value.id)
			return HttpResponseRedirect(url)
	elif request.method == 'GET' and ('transect' in request.GET):
		parentvalue = int(request.GET['transect'])
		next_treeid = next_transecttreeid()
		preamble = '''
		<tr>
		<th>Transect Tree ID:</th>
		<td>%s</td>
		</tr> 
		'''
		preamble = preamble % next_treeid
		initial_dict = { 'transect' : parentvalue, 'treeid' : next_treeid } 
		debug('Initial Values: %s' % initial_dict)
		form = TransectTreeForm(initial_dict)
	else:
		return HttpResponseRedirect('/cavitynesting/')
	dict = { 'formtitle' : 'Transect Tree', 'form' : form, 'buttontitle' : 'Add', 'preamble' : preamble } 
	return render_to_response('form_template.html', dict)

def plot_entry(request):
	return entry_handler(request,PlotForm,'Plot','plot', None)

def tree_entry(request):
	return entry_handler(request,TreeForm,'Tree','tree', 'plot')

#def random_tree_entry(request):
	#return entry_handler(request,RandomTreeForm,'Random Tree','randomtree', 'tree')

#def transect_tree_entry(request):
	#return entry_handler(request,TransectTreeForm,'Transect Tree','transecttree', 'transect')

def cavity_entry(request):
	return entry_handler(request,CavityForm,'Cavity','cavity', 'tree')

def nest_entry(request):
	return entry_handler(request,NestForm,'Nest','nest','cavity')

def visit_entry(request):
	return entry_handler(request,VisitForm,'Visit','visit','nest')


## View and Modification Handlers ################################################

## I really would like to generalize some of these functions into a "generic" 
## handler method, as I have with the handlers above, but there are still enough
## model-specific details in some of these handlers that I haven't gotten up the 
## courage to go ahead and make the switch.  As a result, all of these handlers have
## a common structure and a lot of shared code...

def plot_handler(request,id):
	if request.method=='POST':
		form=PlotForm(request.POST)
		value=Plot.objects.get(id=id)
		if value != None and form.is_valid():
			value.set_from_form(form)
			value.save()
			url = '/cavitynesting/plot/%s/' % value.id 
			return HttpResponseRedirect(url)
	elif request.method == 'GET':
		if 'edit' in request.GET and request.GET['edit'] == 'true':
			value = Plot.objects.get(id=id)
			initial_dict = value.as_dict()
			form = PlotForm(initial_dict)
			resp_dict = { 'formtitle' : 'Plot', 'form' : form, 'buttontitle' : 'Update' } 
			return render_to_response('form_template.html', resp_dict)
		elif 'delete' in request.GET and request.GET['delete'] == 'true':
			value = Plot.objects.get(id=id)
			deps = Tree.objects.filter(plot=id)
			deps2 = Transect.objects.filter(plot=id)
			if len(deps) == 0 and len(deps2) == 0:
				value.delete()
				return HttpResponseRedirect('/cavitynesting/plots/')
			else:
				t = value
				clist = deps
				tlist = deps2
				error = 'Cannot delete Plot that still has Trees or Transects.'
				c = Context({ 'plot_id' : id, 'plot' : t, 'treelist' : clist, 'transectlist' : tlist, 'errormsg' : error })
				t = loader.get_template('plot_view.html')
				return HttpResponse(t.render(c))
		else:
			t = Plot.objects.get(id=id)
			tlist = Transect.objects.filter(plot=id)
			clist = Tree.objects.filter(plot=id)
			c = Context({ 'plot_id' : id, 'plot' : t, 'transectlist' : tlist, 'treelist' : clist })
			t = loader.get_template('plot_view.html')
			return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect('/cavitynesting/plots')

def transect_handler(request,id):
	if request.method=='POST':
		form=TransectForm(request.POST)
		value=Transect.objects.get(id=id)
		if value != None and form.is_valid():
			value.set_from_form(form)
			value.save()
			url = '/cavitynesting/transect/%s/' % value.id 
			return HttpResponseRedirect(url)
	elif request.method == 'GET':
		if 'edit' in request.GET and request.GET['edit'] == 'true':
			value = Transect.objects.get(id=id)
			preamble = '''
			<tr><th align=center>Transect Number:</th>
			<td>%d</td>
			'''  
			preamble = preamble % value.transectnumber
			initial_dict = value.as_dict()
			form = TransectForm(initial_dict)
			resp_dict = { 'formtitle' : 'Transect', 'form' : form, 'buttontitle' : 'Update', 'preamble' : preamble } 
			return render_to_response('form_template.html', resp_dict)
		elif 'delete' in request.GET and request.GET['delete'] == 'true':
			value = Transect.objects.get(id=id)
			deps = TransectTree.objects.filter(transect=id)
			if len(deps) == 0:
				value.delete()
				return HttpResponseRedirect('/cavitynesting/transects/')
			else:
				t = value
				clist = deps
				error = 'Cannot delete Transect that still has Trees.'
				c = Context({ 'transect_id' : id, 'transect' : t, 'treelist' : clist, 'errormsg' : error })
				t = loader.get_template('transect_view.html')
				return HttpResponse(t.render(c))
		else:
			t = Transect.objects.get(id=id)
			clist = TransectTree.objects.filter(transect=id).order_by('treeorder')
			c = Context({ 'transect_id' : id, 'transect' : t, 'treelist' : clist })
			t = loader.get_template('transect_view.html')
			return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect('/cavitynesting/transects')

def transect_tree_handler(request,id):
	if request.method=='POST':
		form=TransectTreeForm(request.POST)
		value=TransectTree.objects.get(id=id)
		if value != None and form.is_valid():
			value.set_from_form(form)
			value.save()
			url = '/cavitynesting/transecttree/%s/' % value.id 
			return HttpResponseRedirect(url)
	elif request.method == 'GET':
		if 'edit' in request.GET and request.GET['edit'] == 'true':
			value = TransectTree.objects.get(id=id)
			initial_dict = value.as_dict()
			preamble = '''
			<tr>
			<th>Transect Tree ID:</th>
			<td>%s</td>
			</tr> 

			'''
			preamble = preamble % value.treeid
			form = TransectTreeForm(initial_dict)
			resp_dict = { 'formtitle' : 'Transect Tree', 'form' : form, 'buttontitle' : 'Update', 'preamble' : preamble } 
			return render_to_response('form_template.html', resp_dict)
		elif 'delete' in request.GET and request.GET['delete'] == 'true':
			value = TransectTree.objects.get(id=id)
			value.delete()
			return HttpResponseRedirect('/cavitynesting/transecttrees/')
		else:
			t = TransectTree.objects.get(id=id)
			hazard_rating = tree_hazard_value(t)
			c = Context({ 'tree_id' : id, 'tree' : t, 'hazard_rating' : hazard_rating })
			t = loader.get_template('transect_tree_view.html')
			return HttpResponse(t.render(c))
	return HttpResponseRedirect('/cavitynesting/transecttrees/')

def random_tree_handler(request,id):
	if request.method=='POST':
		form=RandomTreeForm(request.POST)
		value=RandomTree.objects.get(id=id)
		if value != None and form.is_valid():
			value.set_from_form(form)
			value.save()
			url = '/cavitynesting/randomtree/%s/' % value.id 
			return HttpResponseRedirect(url)
		else:
			resp_dict = { 'formtitle' : 'Random Tree', 'form' : form, 'buttontitle' : 'Update' } 
			return render_to_response('form_template.html', resp_dict)
	elif request.method == 'GET':
		if 'edit' in request.GET and request.GET['edit'] == 'true':
			value = RandomTree.objects.get(id=id)
			initial_dict = value.as_dict()
			form = RandomTreeForm(initial_dict)
			resp_dict = { 'formtitle' : 'Random Tree', 'form' : form, 'buttontitle' : 'Update' } 
			return render_to_response('form_template.html', resp_dict)
		elif 'delete' in request.GET and request.GET['delete'] == 'true':
			value = RandomTree.objects.get(id=id)
			value.delete()
			return HttpResponseRedirect('/cavitynesting/randomtrees/')
		else:
			t = RandomTree.objects.get(id=id)
			hazard_rating = tree_hazard_value(t)
			c = Context({ 'tree_id' : id, 'tree' : t, 'hazard_rating' : hazard_rating })
			t = loader.get_template('random_tree_view.html')
			return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect('/cavitynesting/randomtrees/')

def tree_handler(request,id):
	if request.method=='POST':
		form=TreeForm(request.POST)
		value=Tree.objects.get(id=id)
		if value != None and form.is_valid():
			value.set_from_form(form)
			value.save()
			url = '/cavitynesting/tree/%s/' % value.id 
			return HttpResponseRedirect(url)
	elif request.method == 'GET':
		if 'edit' in request.GET and request.GET['edit'] == 'true':
			value = Tree.objects.get(id=id)
			initial_dict = value.as_dict()
			form = TreeForm(initial_dict)
			resp_dict = { 'formtitle' : 'Tree', 'form' : form, 'buttontitle' : 'Update' } 
			return render_to_response('form_template.html', resp_dict)
		elif 'delete' in request.GET and request.GET['delete'] == 'true':
			value = Tree.objects.get(id=id)
			hazard_rating = tree_hazard_value(value)
			deps = Cavity.objects.filter(tree=id)
			deps2 = RandomTree.objects.filter(tree=id)
			if len(deps) == 0 and len(deps2) == 0:
				value.delete()
				return HttpResponseRedirect('/cavitynesting/trees/')
			else:
				t = value
				clist = deps
				rlist = deps2
				error = 'Cannot delete Tree that still has Cavities or Random Trees.'
				c = Context({ 'tree_id' : id, 'hazard_rating' : hazard_rating, 'tree' : t, 'cavitylist' : clist, 'randomtrees' : rlist, 'errormsg' : error })
				t = loader.get_template('tree_view.html')
				return HttpResponse(t.render(c))
		else:
			t = Tree.objects.get(id=id)
			hazard_rating = tree_hazard_value(t)
			clist = Cavity.objects.filter(tree=id)
			rlist = RandomTree.objects.filter(tree=id)
			c = Context({ 'tree_id' : id, 'tree' : t, 'cavitylist' : clist, 'hazard_rating' : hazard_rating, 'randomtrees' : rlist })
			t = loader.get_template('tree_view.html')
			return HttpResponse(t.render(c))
	return HttpResponseRedirect('/cavitynesting/trees')

def cavity_handler(request,id):
	if request.method=='POST':
		form=CavityForm(request.POST)
		value=Cavity.objects.get(id=id)
		if value != None and form.is_valid():
			value.set_from_form(form)
			value.save()
			url = '/cavitynesting/cavity/%s/' % value.id 
			return HttpResponseRedirect(url)
	elif request.method == 'GET':
		if 'edit' in request.GET and request.GET['edit'] == 'true':
			value = Cavity.objects.get(id=id)
			initial_dict = value.as_dict()
			form = CavityForm(initial_dict)
			resp_dict = { 'formtitle' : 'Cavity', 'form' : form, 'buttontitle' : 'Update' } 
			return render_to_response('form_template.html', resp_dict)
		elif 'delete' in request.GET and request.GET['delete'] == 'true':
			value = Cavity.objects.get(id=id)
			deps = Nest.objects.filter(cavity=id)
			if len(deps) == 0:
				value.delete()
				return HttpResponseRedirect('/cavitynesting/cavities/')
			else:
				t = value
				clist = deps
				error = 'Cannot delete Cavity that still has Nests.'
				c = Context({ 'cavity_id' : id, 'cavity' : t, 'nestlist' : clist, 'errormsg' : error })
				t = loader.get_template('cavity_view.html')
				return HttpResponse(t.render(c))
		else:
			t = Cavity.objects.get(id=id)
			clist = Nest.objects.filter(cavity=id)
			c = Context({ 'cavity_id' : id, 'cavity' : t, 'nestlist' : clist })
			t = loader.get_template('cavity_view.html')
			return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect('/cavitynesting/cavities')

def nest_handler(request,id):
	if request.method=='POST':
		form=NestForm(request.POST)
		value=Nest.objects.get(id=id)
		if value != None and form.is_valid():
			value.set_from_form(form)
			value.save()
			url = '/cavitynesting/nest/%s/' % value.id 
			return HttpResponseRedirect(url)
	elif request.method == 'GET':
		if 'edit' in request.GET and request.GET['edit'] == 'true':
			value = Nest.objects.get(id=id)
			initial_dict = value.as_dict()
			form = NestForm(initial_dict)
			resp_dict = { 'formtitle' : 'Nest', 'form' : form, 'buttontitle' : 'Update' } 
			return render_to_response('form_template.html', resp_dict)
		elif 'delete' in request.GET and request.GET['delete'] == 'true':
			value = Nest.objects.get(id=id)
			deps = Visit.objects.filter(nest=id).order_by('date')
			if len(deps) == 0:
				value.delete()
				return HttpResponseRedirect('/cavitynesting/visits/')
			else:
				t = value
				clist = deps
				error = 'Cannot delete Nest that still has Visits.'
				c = Context({ 'nest_id' : id, 'nest' : t, 'visitlist' : clist, 'errormsg' : error })
				t = loader.get_template('nest_view.html')
				return HttpResponse(t.render(c))
		else:
			t = Nest.objects.get(id=id)
			clist = Visit.objects.filter(nest=id).order_by('date')
			c = Context({ 'nest_id' : id, 'nest' : t, 'visitlist' : clist })
			t = loader.get_template('nest_view.html')
			return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect('/cavitynesting/nests')

def visit_handler(request,id):
	if request.method=='POST':
		form=VisitForm(request.POST)
		value=Visit.objects.get(id=id)
		if value != None and form.is_valid():
			value.set_from_form(form)
			value.save()
			url = '/cavitynesting/visit/%s/' % value.id 
			return HttpResponseRedirect(url)
	elif request.method == 'GET':
		if 'edit' in request.GET and request.GET['edit'] == 'true':
			value = Visit.objects.get(id=id)
			initial_dict = value.as_dict()
			form = VisitForm(initial_dict)
			resp_dict = { 'formtitle' : 'Visit', 'form' : form, 'buttontitle' : 'Update' } 
			return render_to_response('form_template.html', resp_dict)
		elif 'delete' in request.GET and request.GET['delete'] == 'true':
			value = Visit.objects.get(id=id)
			value.delete()
			return HttpResponseRedirect('/cavitynesting/visits/')
		else:
			t = Visit.objects.get(id=id)
			c = Context({ 'visit_id' : id, 'visit' : t })
			t = loader.get_template('visit_view.html')
			return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect('/cavitynesting/visits')

def tree_species_handler(request,id):
	if request.method=='GET':
		tree_species = TreeSpecies.objects.get(id=id)
		if tree_species==None:
			return HttpResponseRedirect('/cavitynesting/treespecies/')
		else:
			nest_trees = Tree.objects.filter(species=id)
			transect_trees = TransectTree.objects.filter(species=id)
			random_trees = RandomTree.objects.filter(species=id)
			dict = { 'nest_trees' : nest_trees, 'transect_trees' : transect_trees, 'random_trees' : random_trees }
			dict['tree_species'] = tree_species
			c = Context(dict)
			t = loader.get_template('tree_species_view.html')
			return HttpResponse(t.render(c))
	else:
		return HttpResponseRedirect('/cavitynesting/')

