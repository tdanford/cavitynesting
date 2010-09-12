from django.conf.urls.defaults import *

urlpatterns = patterns('',

	(r'^cavitynesting/plot/(?P<id>\d+)', 'cavitynesting.cavitydata.views.plot_handler'),
	(r'^cavitynesting/transect/(?P<id>\d+)', 'cavitynesting.cavitydata.views.transect_handler'),
	(r'^cavitynesting/tree/(?P<id>\d+)', 'cavitynesting.cavitydata.views.tree_handler'),
	(r'^cavitynesting/transecttree/(?P<id>\d+)', 'cavitynesting.cavitydata.views.transect_tree_handler'),
	(r'^cavitynesting/randomtree/(?P<id>\d+)', 'cavitynesting.cavitydata.views.random_tree_handler'),
	(r'^cavitynesting/cavity/(?P<id>\d+)', 'cavitynesting.cavitydata.views.cavity_handler'),
	(r'^cavitynesting/nest/(?P<id>\d+)', 'cavitynesting.cavitydata.views.nest_handler'),
	(r'^cavitynesting/visit/(?P<id>\d+)', 'cavitynesting.cavitydata.views.visit_handler'),
	(r'^cavitynesting/treespecies/(?P<id>\d+)', 'cavitynesting.cavitydata.views.tree_species_handler'),

	(r'^cavitynesting/plot-add.html', 'cavitynesting.cavitydata.views.plot_entry'),
	(r'^cavitynesting/transect-add.html', 'cavitynesting.cavitydata.views.transect_entry'),
	(r'^cavitynesting/transect-tree-add.html', 'cavitynesting.cavitydata.views.transect_tree_entry'),
	(r'^cavitynesting/random-tree-add.html', 'cavitynesting.cavitydata.views.random_tree_entry'),
	(r'^cavitynesting/tree-add.html', 'cavitynesting.cavitydata.views.tree_entry'),
	(r'^cavitynesting/cavity-add.html', 'cavitynesting.cavitydata.views.cavity_entry'),
	(r'^cavitynesting/nest-add.html', 'cavitynesting.cavitydata.views.nest_entry'),
	(r'^cavitynesting/visit-add.html', 'cavitynesting.cavitydata.views.visit_entry'),

	(r'^cavitynesting/plots/', 'cavitynesting.cavitydata.views.plot_index'),
	(r'^cavitynesting/transects/', 'cavitynesting.cavitydata.views.transect_index'),
	(r'^cavitynesting/trees/', 'cavitynesting.cavitydata.views.tree_index'),
	(r'^cavitynesting/transecttrees/', 'cavitynesting.cavitydata.views.transect_tree_index'),
	(r'^cavitynesting/randomtrees/', 'cavitynesting.cavitydata.views.random_tree_index'),
	(r'^cavitynesting/cavities/', 'cavitynesting.cavitydata.views.cavity_index'),
	(r'^cavitynesting/nests/', 'cavitynesting.cavitydata.views.nest_index'),
	(r'^cavitynesting/visits/', 'cavitynesting.cavitydata.views.visit_index'),
	(r'^cavitynesting/treespecies/', 'cavitynesting.cavitydata.views.tree_species_index'),
	(r'^cavitynesting/global/', 'cavitynesting.cavitydata.views.global_index'),

	(r'^cavitynesting/input_defaults.html', 'cavitynesting.cavitydata.views.input_defaults_handler'),
	(r'^cavitynesting/updates.html', 'cavitynesting.cavitydata.views.updates_view'),
	(r'^cavitynesting/treesurvey.html', 'cavitynesting.cavitydata.views.random_view'),
	(r'^cavitynesting/survey.html', 'cavitynesting.cavitydata.views.tree_survey_view'),

	(r'^cavitynesting/plotbirdspecies.html', 'cavitynesting.cavitydata.views.plot_bird_species_table'),
	(r'^cavitynesting/plotnestcounts.html', 'cavitynesting.cavitydata.views.new_plot_nest_view'),

	## RDF generation
	(r'^cavitynesting/rdf/tree/(?P<id>\d+)', 'cavitynesting.cavitydata.rdf_views.tree_rdf'),

	# Uncomment this for admin:
	#(r'^cavitynesting/admin.html', include('django.contrib.admin.urls')),

	# default
	(r'^cavitynesting/', 'cavitynesting.cavitydata.views.top_level'),
)
