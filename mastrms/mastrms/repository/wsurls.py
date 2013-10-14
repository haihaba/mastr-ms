from django.conf.urls import *
from django.conf import settings
from mastrms.repository.wsviews import CSVUploadViewFile, CSVUploadViewCaptureCSV

urlpatterns = patterns('mastrms.repository.wsviews',
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)[/]*$', 'populate_select', {'SSL':settings.SSL_ENABLED}),
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)/(?P<value>\w+)[/]*$', 'populate_select', {'SSL':settings.SSL_ENABLED}),
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)/(?P<value>\w+)/(?P<field>\w+)/(?P<match>\w+)[/]*$', 'populate_select', {'SSL':settings.SSL_ENABLED}),
    (r'^records/(?P<model>\w+)/(?P<field>\w+)/(?P<value>.+)[/]*$', 'records', {'SSL':settings.SSL_ENABLED}),
    (r'^create/(?P<model>\w+)[/]*$', 'create_object', {'SSL':settings.SSL_ENABLED}),
    (r'^createSamples[/]*$', 'create_samples', {'SSL':settings.SSL_ENABLED}),
    (r'^batchcreate/samplelog[/]*$', 'batch_create_sample_logs', {'SSL':settings.SSL_ENABLED}),
    (r'^update/(?P<model>\w+)/(?P<id>\w+)[/]*$', 'update_object', {'SSL':settings.SSL_ENABLED}),
    (r'^delete/(?P<model>\w+)/(?P<id>\w+)[/]*$', 'delete_object', {'SSL':settings.SSL_ENABLED}),
    (r'^associate/(?P<model>\w+)/(?P<association>\w+)/(?P<parent_id>\w+)/(?P<id>\w+)[/]*$', 'associate_object', {'SSL':settings.SSL_ENABLED}),
    (r'^dissociate/(?P<model>\w+)/(?P<association>\w+)/(?P<parent_id>\w+)/(?P<id>\w+)[/]*$', 'dissociate_object', {'SSL':settings.SSL_ENABLED}),
    (r'^recreate_sample_classes/(?P<experiment_id>\w+)[/]*$', 'recreate_sample_classes', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsProject/(?P<project_id>\w+)[/]*$', 'recordsProject', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsExperiments[/]*$', 'recordsExperiments', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsExperiments/(?P<project_id>\w+)[/]*$', 'recordsExperimentsForProject', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsRuns[/]*$', 'recordsRuns', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsRuleGenerators[/]*$', 'recordsRuleGenerators', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsRuleGeneratorsAccessibility[/]*$', 'recordsRuleGeneratorsAccessibility', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsRuleGeneratorsAccessibilityEnabled[/]*$', 'recordsRuleGeneratorsAccessibilityEnabled', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsSamplesForExperiment[/]*$', 'recordsSamplesForExperiment', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsSamplesForRun[/]*$', 'recordsSamplesForRun', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsMAStaff[/]*$', 'recordsMAStaff', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsClientList[/]*$', 'recordsClientList', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsClientFiles[/]*$', 'recordsClientFiles', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsSamples/experiment__id/(?P<experiment_id>\w+)[/]*$', 'recordsSamples', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsSamplesForClient/client/(?P<client>.+)[/]*$', 'recordsSamplesForClient', {'SSL':settings.SSL_ENABLED}),
    (r'^recordsComponents[/]*$', 'recordsComponents', {'SSL':settings.SSL_ENABLED}),
    (r'^recent_projects[/]*$', 'recent_projects', {'SSL':settings.SSL_ENABLED}),
    (r'^recent_experiments[/]*$', 'recent_experiments', {'SSL':settings.SSL_ENABLED}),
    (r'^recent_runs[/]*$', 'recent_runs', {'SSL':settings.SSL_ENABLED}),
    (r'^sample_class_enable/(?P<id>\w+)[/]*$', 'sample_class_enable', {'SSL':settings.SSL_ENABLED}),
    (r'^files[/]*$', 'experimentFilesList', {'SSL':settings.SSL_ENABLED}),
    (r'^runFiles[/]*$', 'runFilesList', {'SSL':settings.SSL_ENABLED}),
    (r'^pendingfiles[/]*$', 'pendingFilesList', {'SSL':settings.SSL_ENABLED}),
    (r'^moveFile[/]*$', 'moveFile', {'SSL':settings.SSL_ENABLED}),
    (r'^uploadFile[/]*$', 'uploadFile', {'SSL':settings.SSL_ENABLED}),
    (r'^newFolder[/]*$', 'newFolder', {'SSL':settings.SSL_ENABLED}),
    (r'^uploadSampleCSV[/]*$', CSVUploadViewFile.as_view(), {'SSL':settings.SSL_ENABLED}),
    (r'^uploadRunCaptureCSV[/]*$', CSVUploadViewCaptureCSV.as_view(), {'SSL':settings.SSL_ENABLED}),
    (r'^packageFilesForDownload[/]*$', 'packageFilesForDownload', {'SSL':settings.SSL_ENABLED}),
    (r'^downloadPackage[/]*$', 'downloadPackage', {'SSL':settings.SSL_ENABLED}),
    (r'^downloadFile[/]*$', 'downloadFile', {'SSL':settings.SSL_ENABLED}),
    (r'^downloadClientFile/(?P<filepath>.+)$', 'downloadClientFile', {'SSL':settings.SSL_ENABLED}),
    (r'^downloadSOPFileById/(?P<sop_id>\w+)[/]*$', 'downloadSOPFileById', {'SSL':settings.SSL_ENABLED}),
    url(r'^downloadSOPFile/(?P<sop_id>\w+)/(?P<filename>.*)[/]*$', 'downloadSOPFile', {'SSL':settings.SSL_ENABLED}, name='downloadSOPFile'),
    (r'^downloadRunFile[/]*$', 'downloadRunFile', {'SSL':settings.SSL_ENABLED}),
    (r'^shareFile[/]*$', 'shareFile', {'SSL':settings.SSL_ENABLED}),
    (r'^updateSingleSource/(?P<exp_id>\w+)[/]*$', 'update_single_source', {'SSL':settings.SSL_ENABLED}),
    url(r'^generate_worklist/(?P<run_id>\w+)[/]*$', 'generate_worklist', {'SSL':settings.SSL_ENABLED}, name='generate_worklist'),
    url(r'^display_worklist/(?P<run_id>\w+)[/]*$', 'display_worklist', {'SSL':settings.SSL_ENABLED}, name='display_worklist'),
    url(r'^mark_run_complete/(?P<run_id>\w+)[/]*$', 'mark_run_complete', {'SSL':settings.SSL_ENABLED}, name='mark_run_complete'),
    url(r'^add_samples_to_run[/]*$', 'add_samples_to_run', {'SSL':settings.SSL_ENABLED}, name='add_samples_to_run'),
    url(r'^add_samples_to_class[/]*$', 'add_samples_to_class', {'SSL':settings.SSL_ENABLED}, name='add_samples_to_class'),
    url(r'^report_error[/]*$', 'report_error', {'SSL':settings.SSL_ENABLED}, name='report_error'),
    url(r'^remove_samples_from_run[/]*$', 'remove_samples_from_run', {'SSL':settings.SSL_ENABLED}, name='remove_samples_from_run'),
    url(r'^get_rule_generator[/]*$', 'get_rule_generator', {'SSL':settings.SSL_ENABLED}, name='get_rule_generator'),
    url(r'^create_rule_generator[/]*$', 'create_rule_generator', {'SSL':settings.SSL_ENABLED}, name='create_rule_generator'),
    url(r'^edit_rule_generator[/]*$', 'edit_rule_generator', {'SSL':settings.SSL_ENABLED}, name='edit_rule_generator'),
    url(r'^clone_rule_generator[/]*$', 'clone_rule_generator', {'SSL':settings.SSL_ENABLED}, name='clone_rule_generator'),
    url(r'^create_new_version_of_rule_generator[/]*$', 'create_new_version_of_rule_generator', {'SSL':settings.SSL_ENABLED}, name='create_new_version_of_rule_generator'),
    url(r'^check_experiment_cloneable/(?P<experiment_id>\d+)[/]*$', 'check_experiment_cloneable', {'SSL':settings.SSL_ENABLED}),
    url(r'^clone_run/(?P<run_id>\d+)[/]*$', 'clone_run', {'SSL':settings.SSL_ENABLED}),

)
