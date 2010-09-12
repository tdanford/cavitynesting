from django.db import models
from cavitynesting.cavitydata.utils import *
import datetime

def clear_if_null(dict, key):
	if key in dict and (dict[key] == None or dict[key] == 'None'):
		del dict[key]

## HELPER MODELS #############################################

## The "helper" models are just simple little models which are used
## by lots of the models later on, and which are used to tie different
## elements of those model classes together.  The most commonly used 
## helper model class is TreeSpecies.  Some of them (like the NestFate
## and NestStatus models) I had considered making into hard-coded lists
## originally, but I was told that they might be shared by other models
## in the future so I put them into their own tables for more flexibility
## down the line.  


## These hardcoded lists are only used once (potentially), when we create a 
## new database, so that the tables are all populated by their initial values.
## Mainly, they are used during development, but I left them in for future use
## if necessary.
DEFAULT_NEST_FATES = [ 'Unsuccessful', 'Successful', 'Unsure' ]
DEFAULT_NEST_STATUS = [ 'Unknown/Unsure', 'Excavation/Nest-building', 'Laying', 'Incubation', 'Nestling', 'Fledgling' ]
DEFAULT_NEST_STAGE = [ 'Sample1', 'Sample2' ] 
DEFAULT_NEST_FIND_METHODS = [ 'Luck', 'Parental Behavior', 'Behavioral Cue', 'Previous Year\'s Nest', 'Young Behavior' ] 
DEFAULT_CAVITY_LOCATIONS = [ 'Trunk', 'Branch' ] 
DEFAULT_DECAY_CLASS = [ 'Stage 1', 'Stage 2', 'Stage 3', 'Stage 4', 'Stage 5', 'Stage 6'  ] 

DEFAULT_TREE_SPECIES = ['White Pine', 'Sugar Maple', 'Red Maple', 'Red Oak', 'Birch']
DEFAULT_BIRD_SPECIES = [ 'NOFL', 'DOWO', 'WBNU' ]

def model_id(model,attr):
	try:
		if model==None:
			return None
		else:
			return getattr(model, attr).id 
	except: return None

def zint(value):
	if value == None: 
		return 0
	else:
		return value

class NestFate(models.Model):
	name=models.CharField(max_length=100)
	class Admin:
		pass
	def input_defaults(self, lst=DEFAULT_NEST_FATES):
		for n in lst:
			v = NestFate(name=n)
			v.save()
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name

class NestStatus(models.Model):
	name=models.CharField(max_length=100)
	def input_defaults(self, lst=DEFAULT_NEST_STATUS):
		for n in lst:
			v = NestStatus(name=n)
			v.save()
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name

class NestStage(models.Model):
	name=models.CharField(max_length=100)
	def input_defaults(self, lst=DEFAULT_NEST_STAGE):
		for n in lst:
			v = NestStage(name=n)
			v.save()
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name

class NestFindMethods(models.Model):
	name=models.CharField(max_length=100)
	def input_defaults(self, lst=DEFAULT_NEST_FIND_METHODS):
		for n in lst:
			v = NestFindMethods(name=n)
			v.save()
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name

class CavityLocations(models.Model):
	name=models.CharField(max_length=30)
	def input_defaults(self, lst=DEFAULT_CAVITY_LOCATIONS):
		for n in lst:
			v = CavityLocations(name=n)
			v.save()
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name
	class Admin:
		pass

class DecayClass(models.Model):
	name=models.CharField(max_length=40)
	def input_defaults(self, lst=DEFAULT_DECAY_CLASS):
		for n in lst:
			v = DecayClass(name=n)
			v.save()
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name

class TreeSpecies(models.Model):
	name=models.CharField(max_length=50)
	treeorder=models.IntegerField(null=True)
	def input_defaults(self, lst=DEFAULT_TREE_SPECIES):
		for n in lst:
			v = TreeSpecies(name=n)
			v.save()
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name

class BirdSpecies(models.Model):
	name=models.CharField(max_length=50)
	def input_defaults(self, lst=DEFAULT_BIRD_SPECIES):
		for n in lst:
			v = BirdSpecies(name=n)
			v.save()
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.name


## Two Helper Methods: 
## form_set() takes an object, a form, and a name of a field,
## and does:
## 
## object.fieldname = form.cleandata['fieldname']
## 
## (possibly transforming the value from the cleandata dictionary
##  through a tranforming function, first, if given.)
def form_set(obj,form,fieldname,transformer=None):
	value = form.cleaned_data[fieldname]
	if transformer != None: value = transformer(value)
	setattr(obj,fieldname,value)

## Does pretty much the same thing as form_set, except that it 
## assumes that the value given by form.cleandata['fieldname'] 
## is the *id* of a value from the appropriate class (a new 
## argument to this method), and so it does the requisite 
## id=value lookup before setting object.fieldname
def form_set_ref(obj,form,fieldname,refclass,transformer=None):
	key = form.cleaned_data[fieldname]
	if transformer != None: key = transformer(key)
	value = refclass.objects.get(id=key)
	setattr(obj, fieldname, value)


## PRIMARY MODELS #############################################

## The primary arrangement here is that, at the "top level", are 
## Plots.  Plots contain Trees, which contain Cavities, which 
## contain Nests.  Nests are visited multiple times, and so are 
## referenced by the Visit model.  

## That was the original setup. Later, several new models were added.
## First was the RandomTree model, which contains almost all fo the 
## same fields as the original Tree (i.e., "Nest Tree") model, except 
## that a RandomTree is associated with a particular Tree model, and 
## not directly with a Plot model.

## After that, the transect system was added.  Transects are associated
## with Plots, and then there are TransectTree models which are 
## associated with the Transects.  So it all got kinda complicated 
## after the original database creation.

## Furthermore, the "hazard_" fields were welded onto all the *Tree
## models after their original creation, so that's why that appears
## so unwieldy.  FYI.

def count_dict(lst):
	d = {}
	for l in lst:
		if not l in d: d[l] = 0
		d[l] += 1
	return d

class Plot(models.Model):
	plotid=models.CharField(max_length=50)
	gps=models.CharField(max_length=50)
	address=models.CharField(max_length=100)
	observerinitials=models.CharField(max_length=20)
	notes=models.TextField()
	def csvnotes(self):
		return csv_string(str(self.notes))
	def displaynotes(self,width=50):
		return shorten_string(self.notes,width)
	def htmlnotes(self):
		return htmlify_string(self.notes)
	def bird_species_count(self):
		bird_species_list = [n.species for n in Nest.objects.filter(cavity__tree__plot=self)]
		return count_dict(bird_species_list)
	def as_dict(self):
		dict = {}
		dict['plotid'] = str(self.plotid)
		dict['gps'] = self.gps
		dict['address'] = self.address
		dict['observerinitials'] = self.observerinitials
		dict['notes'] = self.notes
		return dict
	def set_from_form(self,form):
		form_set(self,form,'plotid')
		form_set(self,form,'gps')
		form_set(self,form,'address')
		form_set(self,form,'observerinitials')
		form_set(self,form,'notes')
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.plotid

## aka. "Nest" Trees.
class Tree(models.Model):
	plot=models.ForeignKey(Plot)
	treeid=models.CharField(max_length=50)
	species=models.ForeignKey(TreeSpecies,related_name='nest_trees')

	canopyheight=models.CharField(max_length=20,null=True)
	height=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	gps=models.CharField(max_length=50,null=True)

	crowndimensionEW=models.CharField(max_length=20,null=True)
	crowndimensionNS=models.CharField(max_length=20,null=True)

	pctdead=models.IntegerField(null=True)
	dbh=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	smalldeadbranches=models.CharField(null=True,max_length=50)
	mediumdeadbranches=models.CharField(null=True,max_length=50)
	largedeadbranches=models.CharField(null=True,max_length=50)
	slopeaspect=models.CharField(max_length=20,null=True)
	positionslope=models.CharField(max_length=20,null=True)
	observerinitials=models.CharField(max_length=20)
	notes=models.TextField(null=True)

	# added:
	address=models.CharField(max_length=100,null=True)
	tag=models.IntegerField(null=True)
	numcavities=models.IntegerField(null=True)
	date=models.DateField(null=True)
	decayclass=models.ForeignKey(DecayClass,null=True)

	## new hazard fields:
	hazard_species=models.ForeignKey(TreeSpecies,related_name='hazard_nest_trees')
	hazard_dbh=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	hazard_probtarget=models.IntegerField(null=True)
	hazard_defectivesize=models.IntegerField(null=True)
	hazard_probfail=models.IntegerField(null=True)
	hazard_speciesrating=models.IntegerField(null=True)
	hazard_observer=models.CharField(null=True,max_length=20)
	hazard_action=models.TextField(null=True)
	hazard_date=models.DateField(null=True)
	hazard_notes=models.TextField(null=True)

	def displayhazardnotes(self,width=50):
		return shorten_string(self.hazard_notes,width)
	def htmlhazardnotes(self):
		return htmlify_string(self.hazard_notes)
	class Admin:
		pass
	def csvhazardaction(self):
		return csv_string(self.hazard_action)
	def csvhazardnotes(self):
		return csv_string(self.hazard_notes)
	def csvgps(self):
		return csv_string(self.gps)
	def csvnotes(self):
		return csv_string(self.notes)
	def displaynotes(self,width=50):
		return shorten_string(self.notes,width)
	def htmlnotes(self):
		return htmlify_string(self.notes)
	def htmlaction(self):
		return htmlify_string(self.hazard_action)
	def hazard_score(self):
		return zint(self.hazard_probtarget) + zint(self.hazard_defectivesize) + zint(self.hazard_speciesrating) + zint(self.hazard_probfail)
	def as_dict(self):
		dict = {}
		dict['plot'] = self.plot.id
		dict['treeid'] = self.treeid
		dict['species'] = model_id(self, "species")
		dict['canopyheight'] = self.canopyheight
		dict['height'] = self.height
		dict['gps'] = self.gps
		dict['crowndimensionEW'] = self.crowndimensionEW
		dict['crowndimensionNS'] = self.crowndimensionNS
		dict['pctdead'] = self.pctdead
		dict['dbh'] = self.dbh
		dict['smalldeadbranches'] = self.smalldeadbranches
		dict['mediumdeadbranches'] = self.mediumdeadbranches
		dict['largedeadbranches'] = self.largedeadbranches
		dict['slopeaspect'] = self.slopeaspect
		dict['positionslope'] = self.positionslope
		dict['observerinitials'] = self.observerinitials
		dict['notes'] = self.notes

		dict['tag'] = self.tag
		dict['address'] = self.address
		dict['numcavities'] = self.numcavities
		dict['date'] = str(self.date)
		dict['decayclass'] = model_id(self, "decayclass")

		dict['hazard_species'] = model_id(self, "hazard_species")
		dict['hazard_dbh'] = self.hazard_dbh
		dict['hazard_probtarget'] = str(self.hazard_probtarget)
		dict['hazard_defectivesize'] = str(self.hazard_defectivesize)
		dict['hazard_probfail'] = str(self.hazard_probfail)
		dict['hazard_speciesrating'] = str(self.hazard_speciesrating)
		dict['hazard_action'] = self.hazard_action
		dict['hazard_observer'] = self.hazard_observer
		dict['hazard_date'] = str(self.hazard_date)
		dict['hazard_notes'] = self.hazard_notes

		clear_if_null(dict, 'tag')
		clear_if_null(dict, 'numcavities')
		clear_if_null(dict, 'hazard_defectivesize')
		clear_if_null(dict, 'hazard_probfail')
		clear_if_null(dict, 'hazard_speciesrating')
		clear_if_null(dict, 'hazard_probtarget')
		clear_if_null(dict, 'hazard_notes')
		clear_if_null(dict, 'date')
		clear_if_null(dict, 'hazard_date')

		return dict
	def set_from_form(self,form):
		form_set_ref(self,form,'plot',Plot)	
		form_set(self,form,'treeid')
		form_set(self,form,'species')
		form_set(self,form,'canopyheight')
		form_set(self,form,'height', float_clean) # str_to_float
		form_set(self,form,'gps')
		form_set(self,form,'crowndimensionEW')
		form_set(self,form,'crowndimensionNS')
		form_set(self,form,'pctdead',str_to_int)
		form_set(self,form,'dbh', float_clean)  # str_to_float
		form_set(self,form,'smalldeadbranches')
		form_set(self,form,'mediumdeadbranches')
		form_set(self,form,'largedeadbranches')
		form_set(self,form,'slopeaspect')
		form_set(self,form,'positionslope')
		form_set(self,form,'observerinitials')
		form_set(self,form,'notes')
		form_set(self,form,'address')
		form_set(self,form,'tag')
		form_set(self,form,'numcavities')
		form_set(self,form,'date')
		form_set(self,form,'decayclass')
		form_set(self,form,'hazard_date')
		form_set(self,form,'hazard_species')
		form_set(self,form,'hazard_dbh', float_clean) # str_to_float
		form_set(self,form,'hazard_probtarget')
		form_set(self,form,'hazard_defectivesize')
		form_set(self,form,'hazard_probfail')
		form_set(self,form,'hazard_speciesrating')
		form_set(self,form,'hazard_action')
		form_set(self,form,'hazard_observer')
		form_set(self,form,'hazard_notes')
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.treeid

class Transect(models.Model):
	plot=models.ForeignKey(Plot)
	transectnumber=models.IntegerField()  ## determined in ascending order.
	date=models.DateField(null=True)
	observerinitials=models.CharField(null=True,max_length=20)
	startpoint=models.CharField(null=True,max_length=100)
	endpoint=models.CharField(null=True,max_length=100)
	numsnags=models.IntegerField(null=True)
	dominantspecies = models.CharField(null=True, max_length=100)
	notes=models.TextField(null=True)
	class Admin:
		pass
	def htmlnotes(self):
		return htmlify_string(self.notes)
	def displaynotes(self,width=50):
		return shorten_string(self.notes, width)
	def __repr__(self):
		return 'Transect #%d (Plot %s)' % (self.transectnumber, self.plot.plotid)
	def set_from_form(self,form):
		form_set_ref(self,form,'plot',Plot)	
		form_set(self,form,'transectnumber')
		form_set(self,form,'date')
		form_set(self,form,'observerinitials')
		form_set(self,form,'startpoint')
		form_set(self,form,'endpoint')
		form_set(self,form,'numsnags')
		form_set(self,form,'dominantspecies')
		form_set(self,form,'notes')
	def as_dict(self):
		dict = {}
		dict['plot'] = self.plot.id
		dict['transectnumber'] = self.transectnumber
		dict['date'] = self.date
		dict['observerinitials'] = self.observerinitials
		dict['startpoint'] = self.startpoint
		dict['endpoint'] = self.endpoint
		dict['numsnags'] = self.numsnags
		dict['dominantspecies'] = self.dominantspecies
		dict['notes'] = self.notes
		return dict

class TransectTree(models.Model):
	transect=models.ForeignKey(Transect)
	treeid=models.CharField(max_length=50)  ## needs to be computer generated.
	species=models.ForeignKey(TreeSpecies,related_name='transect_trees')
	height=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	canopyheight=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	crowndimensionEW=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	crowndimensionNS=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	pctdead=models.IntegerField(null=True)
	dbh=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	smalldeadbranches=models.CharField(null=True,max_length=50)
	mediumdeadbranches=models.CharField(null=True,max_length=50)
	largedeadbranches=models.CharField(null=True,max_length=50)
	observerinitials=models.CharField(max_length=20)
	notes=models.TextField(null=True)

	## New fields in TransectTree (compared to 'Tree')
	decayclass=models.ForeignKey(DecayClass,null=True)
	treeorder=models.IntegerField(null=True)  ## always 1-10
	tag=models.IntegerField(null=True)
	numcavities=models.IntegerField(null=True)
	date=models.DateField(null=True)

	hazard_species=models.ForeignKey(TreeSpecies,related_name='hazard_transect_trees')
	hazard_dbh=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	hazard_probtarget=models.IntegerField(null=True)
	hazard_defectivesize=models.IntegerField(null=True)
	hazard_probfail=models.IntegerField(null=True)
	hazard_speciesrating=models.IntegerField(null=True)
	hazard_observer=models.CharField(null=True,max_length=20)
	hazard_action=models.TextField(null=True)
	hazard_date=models.DateField(null=True)
	hazard_notes=models.TextField(null=True)

	def displayhazardnotes(self,width=50):
		return shorten_string(self.hazard_notes,width)
	def htmlhazardnotes(self):
		return htmlify_string(self.hazard_notes)
	class Admin:
		pass
	def csvhazardaction(self):
		return csv_string(self.hazard_action)
	def csvhazardnotes(self):
		return csv_string(self.hazard_notes)
	def csvnotes(self):
		return csv_string(self.notes)
	def csvgps(self):
		return csv_string(self.gps)
	def displaynotes(self,width=50):
		return shorten_string(self.notes,width)
	def hazard_score(self):
		return zint(self.hazard_probtarget) + zint(self.hazard_defectivesize) + zint(self.hazard_speciesrating) + zint(self.hazard_probfail)
	def htmlnotes(self):
		return htmlify_string(self.notes)
	def htmlaction(self):
		return htmlify_string(self.hazard_action)
	def as_dict(self):
		dict = {}
		dict['transect'] = self.transect.id
		dict['treeid'] = self.treeid
		dict['species'] = model_id(self, "species")
		dict['height'] = self.height
		dict['canopyheight'] = self.canopyheight
		dict['crowndimensionEW'] = self.crowndimensionEW
		dict['crowndimensionNS'] = self.crowndimensionNS
		dict['pctdead'] = self.pctdead
		dict['dbh'] = self.dbh
		dict['smalldeadbranches'] = self.smalldeadbranches
		dict['mediumdeadbranches'] = self.mediumdeadbranches
		dict['largedeadbranches'] = self.largedeadbranches
		dict['observerinitials'] = self.observerinitials
		dict['notes'] = self.notes

		dict['tag'] = str(self.tag)
		dict['treeorder'] = str(self.treeorder)
		dict['numcavities'] = str(self.numcavities)
		dict['decayclass'] = model_id(self, "decayclass")
		dict['date'] = str(self.date)

		dict['hazard_species'] = model_id(self, "hazard_species")
		dict['hazard_dbh'] = str(self.hazard_dbh)
		dict['hazard_probtarget'] = str(self.hazard_probtarget)
		dict['hazard_defectivesize'] = str(self.hazard_defectivesize)
		dict['hazard_probfail'] = str(self.hazard_probfail)
		dict['hazard_speciesrating'] = str(self.hazard_speciesrating)
		dict['hazard_action'] = self.hazard_action
		dict['hazard_observer'] = self.hazard_observer
		dict['hazard_date'] = str(self.hazard_date)
		dict['hazard_notes'] = self.hazard_notes

		clear_if_null(dict, 'tag')
		clear_if_null(dict, 'numcavities')
		clear_if_null(dict, 'date')
		clear_if_null(dict, 'hazard_date')
		clear_if_null(dict, 'hazard_defectivesize')
		clear_if_null(dict, 'hazard_probfail')
		clear_if_null(dict, 'hazard_speciesrating')
		clear_if_null(dict, 'hazard_probtarget')
		clear_if_null(dict, 'hazard_notes')

		return dict
	def set_from_form(self,form):
		form_set_ref(self,form,'transect',Transect)
		form_set(self,form,'treeid')
		form_set(self,form,'species')
		form_set(self,form,'height') # str_to_float
		form_set(self,form,'canopyheight') # str_to_float
		form_set(self,form,'crowndimensionEW') # str_to_float
		form_set(self,form,'crowndimensionNS') # str_to_float
		form_set(self,form,'pctdead',str_to_int)
		form_set(self,form,'dbh') # str_to_float
		form_set(self,form,'smalldeadbranches')
		form_set(self,form,'mediumdeadbranches')
		form_set(self,form,'largedeadbranches')
		form_set(self,form,'observerinitials')
		form_set(self,form,'notes')

		form_set(self,form,'tag',str_to_int)
		form_set(self,form,'treeorder',str_to_int)
		form_set(self,form,'numcavities',str_to_int)
		form_set(self,form,'decayclass')

		form_set(self,form,'date')
		form_set(self,form,'hazard_date')

		form_set(self,form,'hazard_species')
		form_set(self,form,'hazard_dbh') # str_to_float
		form_set(self,form,'hazard_probtarget',str_to_int)
		form_set(self,form,'hazard_defectivesize',str_to_int)
		form_set(self,form,'hazard_probfail',str_to_int)
		form_set(self,form,'hazard_speciesrating',str_to_int)
		form_set(self,form,'hazard_action')
		form_set(self,form,'hazard_observer')
		form_set(self,form,'hazard_notes')
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.treeid

class RandomTree(models.Model):
	tree=models.ForeignKey(Tree,related_name='random_trees')
	treeid=models.CharField(max_length=50) # computer-generated: add an 'R' to the end of tree.treeid

	species=models.ForeignKey(TreeSpecies,related_name='random_trees')

	#canopyheight=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	canopyheight=models.CharField(max_length=20,null=True)

	height=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	gps=models.CharField(max_length=50,null=True)

	#crowndimensionEW=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	#crowndimensionNS=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	crowndimensionEW=models.CharField(max_length=20,null=True)
	crowndimensionNS=models.CharField(max_length=20,null=True)

	pctdead=models.IntegerField(null=True)
	dbh=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	smalldeadbranches=models.CharField(null=True,max_length=50)
	mediumdeadbranches=models.CharField(null=True,max_length=50)
	largedeadbranches=models.CharField(null=True,max_length=50)
	slopeaspect=models.CharField(max_length=20,null=True)
	positionslope=models.CharField(max_length=20,null=True)
	observerinitials=models.CharField(max_length=20)
	notes=models.TextField(null=True)

	# added: 
	decayclass=models.ForeignKey(DecayClass,null=True)
	address=models.CharField(null=True,max_length=100)
	date=models.DateField(null=True)
	tag=models.IntegerField(null=True)
	numcavities=models.IntegerField(null=True)

	hazard_species=models.ForeignKey(TreeSpecies,related_name='hazard_random_trees')
	hazard_dbh=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	hazard_probtarget=models.IntegerField(null=True)
	hazard_defectivesize=models.IntegerField(null=True)
	hazard_probfail=models.IntegerField(null=True)
	hazard_speciesrating=models.IntegerField(null=True)
	hazard_observer=models.CharField(null=True,max_length=20)
	hazard_action=models.TextField(null=True)
	hazard_date=models.DateField(null=True)
	hazard_notes=models.TextField(null=True)

	def displayhazardnotes(self,width=50):
		return shorten_string(self.hazard_notes,width)
	def htmlhazardnotes(self):
		return htmlify_string(self.hazard_notes)

	class Admin:
		pass
	def csvhazardaction(self):
		return csv_string(self.hazard_action)
	def csvhazardnotes(self):
		return csv_string(self.hazard_notes)
	def csvnotes(self):
		return csv_string(self.notes)
	def csvgps(self):
		return csv_string(self.gps)
	def displaynotes(self,width=50):
		return shorten_string(self.notes,width)
	def hazard_score(self):
		return zint(self.hazard_probtarget) + zint(self.hazard_defectivesize) + zint(self.hazard_speciesrating) + zint(self.hazard_probfail)
	def htmlnotes(self):
		return htmlify_string(self.notes)
	def htmlaction(self):
		return htmlify_string(self.hazard_action)
	def as_dict(self):
		dict = {}
		dict['tree'] = self.tree.id
		dict['treeid'] = self.treeid
		dict['species'] = model_id(self, "species")
		dict['canopyheight'] = self.canopyheight
		dict['height'] = self.height
		dict['gps'] = self.gps
		dict['crowndimensionEW'] = self.crowndimensionEW
		dict['crowndimensionNS'] = self.crowndimensionNS
		dict['pctdead'] = self.pctdead
		dict['dbh'] = str(self.dbh)
		dict['smalldeadbranches'] = self.smalldeadbranches
		dict['mediumdeadbranches'] = self.mediumdeadbranches
		dict['largedeadbranches'] = self.largedeadbranches
		dict['slopeaspect'] = self.slopeaspect
		dict['positionslope'] = self.positionslope
		dict['observerinitials'] = self.observerinitials
		dict['notes'] = self.notes

		dict['decayclass'] = model_id(self, "decayclass")
		dict['address'] = self.address
		dict['date'] = str(self.date)
		dict['tag'] = str(self.tag)
		dict['numcavities'] = str(self.numcavities)

		dict['hazard_species'] = model_id(self, "hazard_species")
		dict['hazard_dbh'] = self.hazard_dbh
		dict['hazard_probtarget'] = str(self.hazard_probtarget)
		dict['hazard_defectivesize'] = str(self.hazard_defectivesize)
		dict['hazard_probfail'] = str(self.hazard_probfail)
		dict['hazard_speciesrating'] = str(self.hazard_speciesrating)
		dict['hazard_action'] = self.hazard_action
		dict['hazard_observer'] = self.hazard_observer
		dict['hazard_date'] = str(self.hazard_date)
		dict['hazard_notes'] = self.hazard_notes

		clear_if_null(dict, 'hazard_date')
		clear_if_null(dict, 'date')
		clear_if_null(dict, 'tag')
		clear_if_null(dict, 'numcavities')
		clear_if_null(dict, 'hazard_defectivesize')
		clear_if_null(dict, 'hazard_probfail')
		clear_if_null(dict, 'hazard_speciesrating')
		clear_if_null(dict, 'hazard_probtarget')
		clear_if_null(dict, 'hazard_notes')

		return dict
	def set_from_form(self,form):
		form_set_ref(self,form,'tree',Tree)	
		form_set(self,form,'treeid')
		form_set(self,form,'species')
		form_set(self,form,'canopyheight')
		form_set(self,form,'height', float_clean)    # str_to_float
		form_set(self,form,'gps')
		form_set(self,form,'crowndimensionEW')
		form_set(self,form,'crowndimensionNS')
		form_set(self,form,'pctdead',str_to_int)
		form_set(self,form,'dbh', float_clean)    # str_to_float
		form_set(self,form,'smalldeadbranches')
		form_set(self,form,'mediumdeadbranches')
		form_set(self,form,'largedeadbranches')
		form_set(self,form,'slopeaspect')
		form_set(self,form,'positionslope')
		form_set(self,form,'observerinitials')
		form_set(self,form,'notes')

		form_set(self,form,'decayclass')
		form_set(self,form,'address')
		form_set(self,form,'date')
		form_set(self,form,'tag')
		form_set(self,form,'numcavities')

		form_set(self,form,'hazard_species')
		form_set(self,form,'hazard_dbh', float_clean)    # str_to_float
		form_set(self,form,'hazard_probtarget',str_to_int)
		form_set(self,form,'hazard_defectivesize',str_to_int)
		form_set(self,form,'hazard_probfail',str_to_int)
		form_set(self,form,'hazard_speciesrating',str_to_int)
		form_set(self,form,'hazard_action')
		form_set(self,form,'hazard_date')
		form_set(self,form,'hazard_observer')
		form_set(self,form,'hazard_notes')
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.treeid

class Cavity(models.Model):
	tree=models.ForeignKey(Tree)
	cavityid=models.CharField(max_length=40,null=True)
	observerinitials=models.CharField(max_length=20,null=True)
	location=models.ForeignKey(CavityLocations,null=True)

	#heightfromground=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	#distfromtrunk=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	#disttobranchend=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	#cavitydiam=models.DecimalField(decimal_places=2,max_digits=5,null=True)
	#branchdiam=models.DecimalField(decimal_places=2,max_digits=5,null=True)

	heightfromground=models.CharField(max_length=20,null=True)
	distfromtrunk=models.CharField(max_length=20,null=True)
	disttobranchend=models.CharField(max_length=20,null=True)
	cavitydiam=models.CharField(max_length=20,null=True)
	branchdiam=models.CharField(max_length=20,null=True)

	orientation=models.CharField(max_length=10,null=True)
	#decayclass=models.ForeignKey(DecayClass,null=True)
	notes=models.TextField(null=True)
	def as_dict(self):
		dict = {}
		dict['tree'] = self.tree.id
		dict['cavityid'] = self.cavityid
		dict['observerinitials'] = self.observerinitials
		dict['location'] = model_id(self, "location")
		dict['heightfromground'] = self.heightfromground
		dict['distfromtrunk'] = self.distfromtrunk
		dict['disttobranchend'] = self.disttobranchend
		dict['cavitydiam'] = self.cavitydiam
		dict['branchdiam'] = self.branchdiam
		dict['orientation'] = self.orientation
		#dict['decayclass'] = model_id(self, "decayclass")
		dict['notes'] = self.notes
		return dict
	def set_from_form(self,form):
		form_set_ref(self,form,'tree',Tree)
		form_set(self,form,'cavityid')
		form_set(self,form,'observerinitials')
		form_set(self,form,'location')
		form_set(self,form,'heightfromground')
		form_set(self,form,'distfromtrunk')
		form_set(self,form,'disttobranchend')
		form_set(self,form,'cavitydiam')
		form_set(self,form,'branchdiam')
		form_set(self,form,'orientation')
		#form_set(self,form,'decayclass')
		form_set(self,form,'notes')
	def csvnotes(self):
		return csv_string(self.notes)
	def displaynotes(self,width=50):
		return shorten_string(self.notes,width)
	def htmlnotes(self):
		return htmlify_string(self.notes)
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.cavityid

class Nest(models.Model):	
	cavity=models.ForeignKey(Cavity)
	nestid=models.CharField(max_length=40,null=True)
	observerinitials=models.CharField(max_length=20,null=True)
	findmethod=models.ForeignKey(NestFindMethods,null=True)
	species=models.ForeignKey(BirdSpecies,null=True)
	nestfate=models.ForeignKey(NestFate,null=True)
	notes=models.TextField(null=True)
	def set_from_form(self,form):
		form_set_ref(self,form,'cavity',Cavity)
		form_set(self,form,'nestid')
		form_set(self,form,'observerinitials')
		form_set(self,form,'findmethod')
		form_set(self,form,'species')
		form_set(self,form,'nestfate')
		form_set(self,form,'notes')
	def as_dict(self):
		dict = {}
		dict['cavity'] = self.cavity.id
		dict['nestid'] = self.nestid
		dict['observerinitials'] = self.observerinitials
		dict['findmethod'] = model_id(self, "findmethod")
		dict['species'] = model_id(self, "species")
		dict['nestfate'] = model_id(self, "nestfate")
		dict['notes'] = self.notes
		return dict
	def csvnotes(self):
		return csv_string(self.notes)
	def displaynotes(self,width=50):
		return shorten_string(self.notes,width)
	def htmlnotes(self):
		return htmlify_string(self.notes)
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return self.nestid

## The funkiness in dealing with date/time *separately* in the form, but 
## stored together in the model, is kinda killing me...

class Visit(models.Model):
	nest=models.ForeignKey(Nest)
	date=models.DateTimeField(null=True)
	observerinitials=models.CharField(null=True,max_length=20)
	eggs=models.CharField(max_length=20,null=True)
	nestlings=models.CharField(max_length=20,null=True)
	fledglings=models.CharField(max_length=20,null=True)
	fledgedcertainty=models.CharField(max_length=20,null=True)
	status=models.ForeignKey(NestStatus,null=True)
	stage=models.ForeignKey(NestStage,null=True)
	notes=models.TextField(null=True)
	def set_from_form(self,form):
		form_set_ref(self,form,'nest',Nest)

		dv = form.cleaned_data['date']
		tv = form.cleaned_data['time']
		dt = datetime.datetime(dv.year,dv.month,dv.day,tv.hour,tv.minute,tv.second)
		self.date=dt

		form_set(self,form,'observerinitials')
		form_set(self,form,'eggs')
		form_set(self,form,'nestlings')
		form_set(self,form,'fledglings')
		form_set(self,form,'fledgedcertainty')
		form_set(self,form,'status')
		form_set(self,form,'stage')
		form_set(self,form,'notes')
	def as_dict(self):
		dict = {}
		dict['nest'] = self.nest.id
		dict['eggs'] = str(self.eggs)
		dict['observerinitials'] = self.observerinitials
		dict['nestlings'] = str(self.nestlings)
		dict['fledglings'] = str(self.fledglings)
		dict['fledgedcertainty'] = self.fledgedcertainty
		dict['status'] = model_id(self, "status")
		dict['stage'] = model_id(self, "stage")
		dict['notes'] = self.notes

		dict['date'] = None
		dict['time'] = None
		if self.date != None:
			dict['date'] = datetime.date(self.date.year, self.date.month, self.date.day)
			try:
				dict['time'] = datetime.time(self.date.hour, self.date.minute)
			except AttributeError:
				dict['time'] = datetime.time(12, 0, 0)

		return dict
	def csvnotes(self):
		return csv_string(self.notes)
	def time_only(self):
		if self.date != None:
			return datetime.time(self.date.hour, self.date.minute)	
		else:
			return None
	def date_only(self):
		if self.date != None:
			return datetime.date(self.date.year, self.date.month, self.date.day)	
		else:
			return None
	def displaynotes(self,width=50):
		return shorten_string(self.notes,width)
	def htmlnotes(self):
		return htmlify_string(self.notes)
	class Admin:
		pass
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		return '%s @ %s' % (self.nest.nestid, self.date.__str__())

