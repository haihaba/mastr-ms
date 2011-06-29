from django.conf.urls.defaults import *

urlpatterns = patterns('madas.repository.wsviews',
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)[/]*$', 'populate_select', {'SSL':True}),
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)/(?P<value>\w+)[/]*$', 'populate_select', {'SSL':True}),
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)/(?P<value>\w+)/(?P<field>\w+)/(?P<match>\w+)[/]*$', 'populate_select', {'SSL':True}),
    (r'^records/(?P<model>\w+)/(?P<field>\w+)/(?P<value>.+)[/]*$', 'records', {'SSL':True}),
    (r'^recordsClients/(?P<model>\w+)/(?P<field>\w+)/(?P<value>.+)[/]*$', 'recordsClients', {'SSL':True}),
    (r'^create/(?P<model>\w+)[/]*$', 'create_object', {'SSL':True}),
    (r'^createSamples[/]*$', 'create_samples', {'SSL':True}),
    (r'^batchcreate/samplelog[/]*$', 'batch_create_sample_logs', {'SSL':True}),
    (r'^update/(?P<model>\w+)/(?P<id>\w+)[/]*$', 'update_object', {'SSL':True}),
    (r'^delete/(?P<model>\w+)/(?P<id>\w+)[/]*$', 'delete_object', {'SSL':True}),
    (r'^associate/(?P<model>\w+)/(?P<association>\w+)/(?P<parent_id>\w+)/(?P<id>\w+)[/]*$', 'associate_object', {'SSL':True}),
    (r'^dissociate/(?P<model>\w+)/(?P<association>\w+)/(?P<parent_id>\w+)/(?P<id>\w+)[/]*$', 'dissociate_object', {'SSL':True}),
    (r'^recreate_sample_classes/(?P<experiment_id>\w+)[/]*$', 'recreate_sample_classes', {'SSL':True}),
    (r'^recordsExperiments[/]*$', 'recordsExperiments', {'SSL':True}),
    (r'^recordsExperiments/(?P<project_id>\w+)[/]*$', 'recordsExperimentsForProject', {'SSL':True}),
    (r'^recordsSamplesForExperiment[/]*$', 'recordsSamplesForExperiment', {'SSL':True}),
    (r'^recordsClientList[/]*$', 'recordsClientList', {'SSL':True}),
    (r'^recordsClientFiles[/]*$', 'recordsClientFiles', {'SSL':True}),
    (r'^recordsSamples/experiment__id/(?P<experiment_id>\w+)[/]*$', 'recordsSamples', {'SSL':True}),
    (r'^recordsSamplesForClient/client/(?P<client>.+)[/]*$', 'recordsSamplesForClient', {'SSL':True}),
    (r'^recent_experiments[/]*$', 'recent_experiments', {'SSL':True}),
    (r'^recent_runs[/]*$', 'recent_runs', {'SSL':True}),
    (r'^sample_class_enable/(?P<id>\w+)[/]*$', 'sample_class_enable', {'SSL':True}),
    (r'^files[/]*$', 'experimentFilesList', {'SSL':True}),
    (r'^runFiles[/]*$', 'runFilesList', {'SSL':True}),
    (r'^pendingfiles[/]*$', 'pendingFilesList', {'SSL':True}),
    (r'^moveFile[/]*$', 'moveFile', {'SSL':True}),
    (r'^uploadFile[/]*$', 'uploadFile', {'SSL':True}),
    (r'^uploadSampleCSV[/]*$', 'uploadCSVFile', {'SSL':True}),
    (r'^downloadFile[/]*$', 'downloadFile', {'SSL':True}),
    (r'^downloadClientFile/(?P<filepath>.+)$', 'downloadClientFile', {'SSL':True}),
    (r'^downloadSOPFile/(?P<sop_id>\w+)[/]*$', 'downloadSOPFile', {'SSL':True}),
    (r'^downloadRunFile[/]*$', 'downloadRunFile', {'SSL':True}),
    (r'^shareFile[/]*$', 'shareFile', {'SSL':True}),
    (r'^updateSingleSource/(?P<exp_id>\w+)[/]*$', 'update_single_source', {'SSL':True}),
    url(r'^generate_worklist/(?P<run_id>\w+)[/]*$', 'generate_worklist', {'SSL':True}, name='generate_worklist'),
    url(r'^mark_run_complete/(?P<run_id>\w+)[/]*$', 'mark_run_complete', {'SSL':True}, name='mark_run_complete'),
    url(r'^add_samples_to_run[/]*$', 'add_samples_to_run', {'SSL':True}, name='add_samples_to_run'),
    url(r'^add_samples_to_class[/]*$', 'add_samples_to_class', {'SSL':True}, name='add_samples_to_class'),
    url(r'^report_error[/]*$', 'report_error', {'SSL':True}, name='report_error'),
    url(r'^remove_samples_from_run[/]*$', 'remove_samples_from_run', {'SSL':True}, name='remove_samples_from_run'),
)
