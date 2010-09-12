import django
from cavitynesting.cavitydata.models import *

decay_class_list=[]
cavity_locations_list= [ 'Upper', 'Middle', 'Lower' ]
cavity_contents_list = [ 'Unsure/Unknown', 'Eggs', 'Nestlings', 'Eggs and Nestlings', 'Nestlings and Nearby Fledglings']
nest_status_list = ['Unsure/Unknown', 'Active', 'Inactive', 'Cavity/Nest Destroyed', 'Tree Removed/Fell Over']
nest_find_method_list = ['Luck', 'Parental Behavior', 'Systematic Search', 'Non-behavioral Cue', 'Previous Year\'s Nest', 'Young Behavior']
nest_stage_list = ['Unsure/Unknown', 'Excavation/Nest Building', 'Laying', 'Incubation', 'Nestling', 'Fledgling']
nest_fate_list = ['Unsure/Unknown', 'Successful', 'Unsuccessful']

def init_models():
	for x in decay_class_list:
		v = DecayClass(name=x)
		v.save()
	for x in cavity_locations_list:
		v = CavityLocations(name=x)
		v.save()
	for x in cavity_contents_list:
		v = CavityContents(name=x)
		v.save()
	for x in nest_status_list:
		v = NestStatus(name=x)
		v.save()
	for x in nest_find_method_list:
		v = NestFindMethods(name=x)
		v.save()
	for x in nest_stage_list:
		v = NestStage(name=x)
		v.save()
	for x in nest_fate_list:
		v = NestFate(name=x)
		v.save()

