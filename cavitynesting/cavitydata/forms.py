#from django import newforms as forms
#from django.newforms import extras

from django import forms
from django.forms import extras
from cavitynesting.cavitydata.models import *

from cavitynesting.cavitydata.utils import *

FLEDGED_CHOICES=(
	('sure', 'sure'),
	('probable', 'probable'),
	('unsure', 'unsure'),
	('n/a', 'n/a'),
)

TREE_ORDER_CHOICES=(
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5'),
	(6, '6'),
	(7, '7'),
	(8, '8'),
	(9, '9'),
	(10, '10'),
)

OECERTAINTY_CHOICES=(
	(1, 'unsure'),
	(2, 'sure'),
	(0, 'n/a'),
)

TRANSECT_NUMBER_CHOICES=(
	(1, '1'),
	(2, '2'),
	(3, '3'),
)

PROB_TARGET_CHOICES=(
	(0, '0'),
	(1, '1'),
	(2, '2'),
	(3, '3'),
)
DEFECTIVE_SIZE_CHOICES=(
	(0, '0'),
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
)
PROB_FAIL_CHOICES=(
	(0, '0'),
	(1, '1'),
	(2, '2'),
	(3, '3'),
)
SPECIES_RATING_CHOICES=(
	(0, '0'),
	(1, '1'),
	(2, '2'),
)

date_years=('2008', '2009', '2010')

class PlotForm(forms.Form):
	plotid=forms.CharField(label='Plot ID',required=False)
	gps=forms.CharField(label='GPS',required=False)
	address=forms.CharField(label='Plot Address',required=False)
	observerinitials=forms.CharField(label='Observer Initials',required=False)
	notes=forms.CharField(required=False, widget=forms.Textarea(attrs={'cols':40,'rows':15}))
	def create_value(self):
		a1=self.cleaned_data['plotid']
		a2=self.cleaned_data['gps']
		a3=self.cleaned_data['address']
		a4=self.cleaned_data['observerinitials']
		a6=self.cleaned_data['notes']
		plot=Plot(plotid=a1,gps=a2,address=a3,observerinitials=a4,notes=a6)
		return plot

class TransectForm(forms.Form):
	plot=forms.IntegerField(widget=forms.HiddenInput())

	#transectnumber=forms.ChoiceField(label='Transect Number',required=True,choices=TRANSECT_NUMBER_CHOICES)
	transectnumber=forms.IntegerField(widget=forms.HiddenInput())

	date=forms.DateField(label='Date',required=False)
	observerinitials=forms.CharField(label='Observer Initials',required=False)
	startpoint=forms.CharField(label='Start Point',required=False)
	endpoint=forms.CharField(label='End Point',required=False)
	numsnags=forms.IntegerField(label='# of Snags',required=False)
	dominantspecies=forms.CharField(label='Dominant Tree Species',required=False)
	notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))

	def create_value(self):
		plot_id=self.cleaned_data['plot']
		a0=Plot.objects.get(id=plot_id)
		a1=self.cleaned_data['transectnumber']
		a2=self.cleaned_data['date']
		a3=self.cleaned_data['observerinitials']
		a4=self.cleaned_data['startpoint']
		a5=self.cleaned_data['endpoint']
		a6=self.cleaned_data['numsnags']
		a7=self.cleaned_data['dominantspecies']
		a8=self.cleaned_data['notes']

		transect = Transect(plot=a0,transectnumber=a1,date=a2,observerinitials=a3,startpoint=a4,endpoint=a5,numsnags=a6,dominantspecies=a7,notes=a8)
		return transect

class TreeForm(forms.Form):
	plot=forms.IntegerField(widget=forms.HiddenInput())
	treeid=forms.CharField(label='Tree ID',required=False)
	tag=forms.IntegerField(label='Tag #',required=False)
	observerinitials=forms.CharField(label='Observer Initials',required=False)
	date=forms.DateField(label='Date',required=False)
	species=forms.ModelChoiceField(TreeSpecies.objects.all().order_by('treeorder'),label='Species',required=False)
	canopyheight=forms.CharField(label='Canopy Height',required=False)
	height=forms.DecimalField(label='Height',required=False)
	gps=forms.CharField(label='GPS',required=False)
	crowndimensionEW=forms.CharField(label='Crown Dimension EW',required=False)
	crowndimensionNS=forms.CharField(label='Crown Dimension NS',required=False)
	pctdead=forms.IntegerField(required=False,label='% Dead')
	dbh=forms.DecimalField(label='DBH',required=False)
	smalldeadbranches=forms.CharField(label='Dead Branches (Small)',required=False)
	mediumdeadbranches=forms.CharField(label='Dead Branches (Medium)',required=False)
	largedeadbranches=forms.CharField(label='Dead Branches (Large)',required=False)
	slopeaspect=forms.CharField(label='Slope Aspect',required=False)
	positionslope=forms.CharField(label='Position Slope',required=False)
	numcavities=forms.IntegerField(label='# Cavities',required=False)
	decayclass=forms.ModelChoiceField(DecayClass.objects.all(),required=False)
	notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))

	address=forms.CharField(label='Address',required=False)

	hazard_species=forms.ModelChoiceField(TreeSpecies.objects.all().order_by('treeorder'),label='Hazard Tree Species',required=False)
	hazard_dbh=forms.DecimalField(label='Hazard DBH',required=False)
	hazard_probtarget=forms.ChoiceField(label='Hazard Prob of Target',required=False,choices=PROB_TARGET_CHOICES)
	hazard_defectivesize=forms.ChoiceField(label='Hazard Size of Defective Part',required=False,choices=DEFECTIVE_SIZE_CHOICES)
	hazard_probfail=forms.ChoiceField(label='Hazard Prob of Fail',required=False,choices=PROB_FAIL_CHOICES)
	hazard_speciesrating=forms.ChoiceField(label='Hazard Species Rating',required=False,choices=SPECIES_RATING_CHOICES)

	hazard_action=forms.CharField(label='Hazard Action',required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))
	hazard_observer=forms.CharField(label='Hazard Observer',required=False)
	hazard_date=forms.DateField(label='Hazard Date',required=False)
	hazard_notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))

	def create_value(self):
		plot_id=self.cleaned_data['plot']
		a0=Plot.objects.get(id=plot_id)
		a1=self.cleaned_data['treeid']
		a2=self.cleaned_data['species']
		a3=self.cleaned_data['height']
		a3b=self.cleaned_data['canopyheight']
		a4=self.cleaned_data['gps']
		a6=self.cleaned_data['crowndimensionEW']
		a7=self.cleaned_data['crowndimensionNS']
		a8=self.cleaned_data['pctdead']
		a9=self.cleaned_data['dbh']
		a10=self.cleaned_data['smalldeadbranches']
		a11=self.cleaned_data['mediumdeadbranches']
		a12=self.cleaned_data['largedeadbranches']
		a13=self.cleaned_data['slopeaspect']
		a14=self.cleaned_data['positionslope']
		a15=self.cleaned_data['observerinitials']
		a16=self.cleaned_data['notes']

		b0=self.cleaned_data['tag']
		b1=self.cleaned_data['numcavities']
		b2=self.cleaned_data['address']
		b3=self.cleaned_data['date']
		b4=self.cleaned_data['decayclass']

		h0=self.cleaned_data['hazard_species']
		h1=self.cleaned_data['hazard_dbh']
		h2=self.cleaned_data['hazard_probtarget']
		h2=self.cleaned_data['hazard_probtarget']
		h3=self.cleaned_data['hazard_defectivesize']
		h4=self.cleaned_data['hazard_probfail']
		h5=self.cleaned_data['hazard_speciesrating']
		h6=self.cleaned_data['hazard_action']
		h7=self.cleaned_data['hazard_observer']
		h8=self.cleaned_data['hazard_notes']
		h9=self.cleaned_data['hazard_date']

		tree=Tree(plot=a0,treeid=a1,species=a2,height=a3,canopyheight=a3b,gps=a4,crowndimensionEW=a6,crowndimensionNS=a7,pctdead=a8,dbh=a9,smalldeadbranches=a10,mediumdeadbranches=a11,largedeadbranches=a12,slopeaspect=a13,positionslope=a14,observerinitials=a15,notes=a16,tag=b0,numcavities=b1,address=b2,date=b3,decayclass=b4,hazard_species=h0,hazard_dbh=h1,hazard_probtarget=h2,hazard_defectivesize=h3,hazard_probfail=h4,hazard_speciesrating=h5,hazard_action=h6,hazard_observer=h7,hazard_notes=h8,hazard_date=h9)
		return tree

class TransectTreeForm(forms.Form):
	transect=forms.IntegerField(widget=forms.HiddenInput())
	treeid = forms.CharField(widget=forms.HiddenInput())
	#treeid=forms.CharField(label='Tree ID',required=False)

	tag=forms.IntegerField(label='Tag #',required=False)
	treeorder=forms.ChoiceField(label='Tree Order',required=False,choices=TREE_ORDER_CHOICES)

	observerinitials=forms.CharField(label='Observer Initials',required=False)
	date=forms.DateField(label='Date',required=False)
	species=forms.ModelChoiceField(TreeSpecies.objects.all().order_by('treeorder'),label='Species',required=False)

	canopyheight=forms.DecimalField(label='Canopy Height',required=False)
	height=forms.DecimalField(label='Height',required=False)
	crowndimensionEW=forms.DecimalField(label='Crown Dimension EW',required=False)
	crowndimensionNS=forms.DecimalField(label='Crown Dimension NS',required=False)
	pctdead=forms.CharField(required=False,label='% Dead')
	dbh=forms.DecimalField(label='DBH',required=False)
	smalldeadbranches=forms.CharField(label='Dead Branches (Small)',required=False)
	mediumdeadbranches=forms.CharField(label='Dead Branches (Medium)',required=False)
	largedeadbranches=forms.CharField(label='Dead Branches (Large)',required=False)
	numcavities=forms.IntegerField(label='# Cavities',required=False)
	notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))


	decayclass=forms.ModelChoiceField(DecayClass.objects.all(),label='Decay Class',required=False)

	hazard_species=forms.ModelChoiceField(TreeSpecies.objects.all().order_by('treeorder'),label='Hazard Tree Species',required=False)
	hazard_dbh=forms.DecimalField(label='Hazard DBH',required=False)

	hazard_probtarget=forms.ChoiceField(label='Hazard Prob of Target',required=False,choices=PROB_TARGET_CHOICES)
	hazard_defectivesize=forms.ChoiceField(label='Hazard Size of Defective Part',required=False,choices=DEFECTIVE_SIZE_CHOICES)
	hazard_probfail=forms.ChoiceField(label='Hazard Prob of Fail',required=False,choices=PROB_FAIL_CHOICES)
	hazard_speciesrating=forms.ChoiceField(label='Hazard Species Rating',required=False,choices=SPECIES_RATING_CHOICES)

	hazard_action=forms.CharField(label='Hazard Action',required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))
	hazard_observer=forms.CharField(label='Hazard Observer',required=False)
	hazard_date=forms.DateField(label='Hazard Date',required=False)
	hazard_notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))

	def create_value(self):
		transect_id=self.cleaned_data['transect']
		a0=Transect.objects.get(id=transect_id)
		a1=self.cleaned_data['treeid']
		a2=self.cleaned_data['species']
		a3=self.cleaned_data['height']
		a3b=self.cleaned_data['canopyheight']
		#a6=str_to_float(self.cleaned_data['crowndimensionEW'])
		#a7=str_to_float(self.cleaned_data['crowndimensionNS'])
		a6=self.cleaned_data['crowndimensionEW']
		a7=self.cleaned_data['crowndimensionNS']
		a8=self.cleaned_data['pctdead']
		#a9=str_to_float(self.cleaned_data['dbh'])
		a9=self.cleaned_data['dbh']
		a10=self.cleaned_data['smalldeadbranches']
		a11=self.cleaned_data['mediumdeadbranches']
		a12=self.cleaned_data['largedeadbranches']
		a15=self.cleaned_data['observerinitials']
		a16=self.cleaned_data['notes']

		b0=self.cleaned_data['tag']
		b1=self.cleaned_data['numcavities']
		b2=self.cleaned_data['decayclass']
		b3=self.cleaned_data['treeorder']
		b4=self.cleaned_data['date']

		h0=self.cleaned_data['hazard_species']
		#h1=str_to_float(self.cleaned_data['hazard_dbh'])
		h1=self.cleaned_data['hazard_dbh']
		h2=self.cleaned_data['hazard_probtarget']
		h3=self.cleaned_data['hazard_defectivesize']
		h4=self.cleaned_data['hazard_probfail']
		h5=self.cleaned_data['hazard_speciesrating']
		h6=self.cleaned_data['hazard_action']
		h7=self.cleaned_data['hazard_observer']
		h8=self.cleaned_data['hazard_notes']
		h9=self.cleaned_data['hazard_date']

		tree=TransectTree(transect=a0,treeid=a1,species=a2,height=a3,canopyheight=a3b,crowndimensionEW=a6,crowndimensionNS=a7,pctdead=a8,dbh=a9,smalldeadbranches=a10,mediumdeadbranches=a11,largedeadbranches=a12,observerinitials=a15,notes=a16,tag=b0,numcavities=b1,decayclass=b2,treeorder=b3,date=b4,hazard_species=h0,hazard_dbh=h1,hazard_probtarget=h2,hazard_defectivesize=h3,hazard_probfail=h4,hazard_speciesrating=h5,hazard_action=h6,hazard_observer=h7,hazard_notes=h8,hazard_date=h9)
		return tree

class RandomTreeForm(forms.Form):
	tree=forms.IntegerField(widget=forms.HiddenInput())
	#treeid=forms.CharField(label='Tree ID',required=False)
	treeid = forms.CharField(widget=forms.HiddenInput())
	tag=forms.IntegerField(label='Tag #',required=False)

	observerinitials=forms.CharField(label='Observer Initials',required=False)
	species=forms.ModelChoiceField(TreeSpecies.objects.all().order_by('treeorder'),label='Species',required=False)
	height=forms.CharField(label='Height',required=False)
	canopyheight=forms.CharField(label='Canopy Height',required=False)
	gps=forms.CharField(label='GPS',required=False)
	crowndimensionEW=forms.CharField(label='Crown Dimension EW',required=False)
	crowndimensionNS=forms.CharField(label='Crown Dimension NS',required=False)
	pctdead=forms.CharField(label='% Dead',required=False)
	#dbh=forms.CharField(label='DBH',required=False)
	dbh=forms.DecimalField(label='DBH',required=False)
	smalldeadbranches=forms.CharField(label='Dead Branches (Small)',required=False)
	mediumdeadbranches=forms.CharField(label='Dead Branches (Medium)',required=False)
	largedeadbranches=forms.CharField(label='Dead Branches (Large)',required=False)
	slopeaspect=forms.CharField(label='Slope Aspect',required=False)
	positionslope=forms.CharField(label='Position Slope',required=False)
	numcavities=forms.IntegerField(label='# Cavities',required=False)
	notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))

	decayclass=forms.ModelChoiceField(DecayClass.objects.all(),label='Decay Class',required=False)
	address=forms.CharField(label='Address',required=False)
	date=forms.DateField(label='Date',required=False)

	hazard_species=forms.ModelChoiceField(TreeSpecies.objects.all().order_by('treeorder'),label='Hazard Tree Species',required=False)
	#hazard_dbh=forms.CharField(label='Hazard DBH',required=False)
	hazard_dbh=forms.DecimalField(label='Hazard DBH',required=False)

	hazard_probtarget=forms.ChoiceField(label='Hazard Prob of Target',required=False,choices=PROB_TARGET_CHOICES)
	hazard_defectivesize=forms.ChoiceField(label='Hazard Size of Defective Part',required=False,choices=DEFECTIVE_SIZE_CHOICES)
	hazard_probfail=forms.ChoiceField(label='Hazard Prob of Fail',required=False,choices=PROB_FAIL_CHOICES)
	hazard_speciesrating=forms.ChoiceField(label='Hazard Species Rating',required=False,choices=SPECIES_RATING_CHOICES)

	hazard_action=forms.CharField(label='Hazard Action',required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))
	hazard_observer=forms.CharField(label='Hazard Observer',required=False)
	hazard_date=forms.DateField(label='Hazard Date',required=False)
	hazard_notes=forms.CharField(required=False,widget=forms.Textarea(attrs={'cols':40, 'rows':15}))

	def create_value(self):
		tree_dbid=self.cleaned_data['tree']
		a0=Tree.objects.get(id=tree_dbid)
		a1=self.cleaned_data['treeid']
		a2=self.cleaned_data['species']
		a3=self.cleaned_data['height']
		a3b=self.cleaned_data['canopyheight']
		a4=self.cleaned_data['gps']
		a6=self.cleaned_data['crowndimensionEW']
		a7=self.cleaned_data['crowndimensionNS']
		a8=self.cleaned_data['pctdead']
		a9=self.cleaned_data['dbh']
		a10=self.cleaned_data['smalldeadbranches']
		a11=self.cleaned_data['mediumdeadbranches']
		a12=self.cleaned_data['largedeadbranches']
		a13=self.cleaned_data['slopeaspect']
		a14=self.cleaned_data['positionslope']
		a15=self.cleaned_data['observerinitials']
		a16=self.cleaned_data['notes']

		b0=self.cleaned_data['tag']
		b1=self.cleaned_data['numcavities']
		b2=self.cleaned_data['decayclass']
		b3=self.cleaned_data['address']
		b4=self.cleaned_data['date']

		h0=self.cleaned_data['hazard_species']
		h1=self.cleaned_data['hazard_dbh']
		h2=self.cleaned_data['hazard_probtarget']
		h3=self.cleaned_data['hazard_defectivesize']
		h4=self.cleaned_data['hazard_probfail']
		h5=self.cleaned_data['hazard_speciesrating']
		h6=self.cleaned_data['hazard_action']
		h7=self.cleaned_data['hazard_observer']
		h8=self.cleaned_data['hazard_notes']
		h9=self.cleaned_data['hazard_date']

		tree=RandomTree(tree=a0,treeid=a1,species=a2,height=a3,canopyheight=a3b,gps=a4,crowndimensionEW=a6,crowndimensionNS=a7,pctdead=a8,dbh=a9,smalldeadbranches=a10,mediumdeadbranches=a11,largedeadbranches=a12,slopeaspect=a13,positionslope=a14,observerinitials=a15,notes=a16,tag=b0,numcavities=b1,decayclass=b2,address=b3,date=b4,hazard_species=h0,hazard_dbh=h1,hazard_probtarget=h2,hazard_defectivesize=h3,hazard_probfail=h4,hazard_speciesrating=h5,hazard_action=h6,hazard_observer=h7,hazard_notes=h8,hazard_date=h9)
		return tree

class CavityForm(forms.Form):
	tree=forms.IntegerField(widget=forms.HiddenInput())
	cavityid=forms.CharField(label='Cavity ID',required=False)
	observerinitials=forms.CharField(label='Observer',required=False)
	heightfromground=forms.CharField(label='Height from Ground', required=False)
	location=forms.ModelChoiceField(CavityLocations.objects.all(),required=False)
	distfromtrunk=forms.CharField(required=False)
	disttobranchend=forms.CharField(required=False)
	cavitydiam=forms.CharField(required=False)
	branchdiam=forms.CharField(required=False)
	orientation=forms.CharField(required=False)
	#decayclass=forms.ModelChoiceField(DecayClass.objects.all(),required=False)
	notes=forms.CharField(widget=forms.Textarea(attrs={'cols':40, 'rows':15}),required=False)
	def create_value(self):
		tree_id=self.cleaned_data['tree']
		cav_tree=Tree.objects.get(id=tree_id)
		cav_id=self.cleaned_data['cavityid']
		observerinitials=self.cleaned_data['observerinitials']
		cav_location=self.cleaned_data['location']
		cav_hfg=self.cleaned_data['heightfromground']
		cav_dft=self.cleaned_data['distfromtrunk']
		cav_dtb=self.cleaned_data['disttobranchend']
		cav_diam=self.cleaned_data['cavitydiam']
		cav_branchdiam=self.cleaned_data['branchdiam']
		cav_orientation=self.cleaned_data['orientation']
		#cav_decayclass=self.cleaned_data['decayclass']
		cav_notes=self.cleaned_data['notes']

		cavity = Cavity(cavityid=cav_id,tree=cav_tree,location=cav_location,observerinitials=observerinitials,heightfromground=cav_hfg,distfromtrunk=cav_dft,disttobranchend=cav_dtb,cavitydiam=cav_diam,branchdiam=cav_branchdiam,orientation=cav_orientation,notes=cav_notes)
		return cavity

class NestForm(forms.Form):
	cavity=forms.IntegerField(widget=forms.HiddenInput())
	nestid=forms.CharField(required=False)
	observerinitials=forms.CharField(required=False)
	findmethod=forms.ModelChoiceField(NestFindMethods.objects.all(),required=False)
	species=forms.ModelChoiceField(BirdSpecies.objects.all(),required=False)
	nestfate=forms.ModelChoiceField(NestFate.objects.all(),required=False)
	notes=forms.CharField(widget=forms.Textarea(attrs={'cols':40, 'rows':15}),required=False)
	def create_value(self):
		cavity_id=self.cleaned_data['cavity']
		cavity=Cavity.objects.get(id=cavity_id)
		nestid=self.cleaned_data['nestid']
		observerinitials=self.cleaned_data['observerinitials']
		findmethod=self.cleaned_data['findmethod']
		species=self.cleaned_data['species']
		nestfate=self.cleaned_data['nestfate']
		notes=self.cleaned_data['notes']

		nest = Nest(cavity=cavity,nestid=nestid,observerinitials=observerinitials,findmethod=findmethod,species=species,nestfate=nestfate,notes=notes)
		return nest

class VisitForm(forms.Form):
	nest=forms.IntegerField(widget=forms.HiddenInput())
	#date=forms.DateField(label='Date',widget=extras.SelectDateWidget(years=date_years),required=False)
	date=forms.DateField(label='Date',required=False)
	time=forms.TimeField(label='Time',required=False)
	observerinitials=forms.CharField(label='Observer',required=False)
	eggs=forms.CharField(label='Eggs',required=False)
	nestlings=forms.CharField(label='Nestlings',required=False)
	fledglings=forms.CharField(label='Fledglings',required=False)
	#eggs=forms.IntegerField(label='Eggs',required=False)
	#nestlings=forms.IntegerField(label='Nestlings',required=False)
	#fledglings=forms.IntegerField(label='Fledglings',required=False)
	fledgedcertainty=forms.ChoiceField(label='Fledged Certainty',required=False,choices=FLEDGED_CHOICES)
	status=forms.ModelChoiceField(NestStatus.objects.all(),required=False)
	stage=forms.ModelChoiceField(NestStage.objects.all(),required=False)
	notes=forms.CharField(label='Notes',widget=forms.Textarea(attrs={'cols':40,'rows':20}),required=False)
	def create_value(self):
		date=self.cleaned_data['date']
		time=self.cleaned_data['time']
		datetime='%s %s' % (date, time)
		nest_id=self.cleaned_data['nest']
		eggs=self.cleaned_data['eggs']
		nestlings=self.cleaned_data['nestlings']
		observerinitials=self.cleaned_data['observerinitials']
		fledglings=self.cleaned_data['fledglings']
		fledgedcertainty=self.cleaned_data['fledgedcertainty']
		status=self.cleaned_data['status']
		stage=self.cleaned_data['stage']
		notes=self.cleaned_data['notes']
		nest=Nest.objects.get(id=nest_id)
		visit=Visit(date=datetime,nest=nest,eggs=eggs,observerinitials=observerinitials,nestlings=nestlings,fledglings=fledglings,fledgedcertainty=fledgedcertainty,status=status,stage=stage,notes=notes)
		return visit


