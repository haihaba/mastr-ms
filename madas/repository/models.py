from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date, time
from m.models import Organisation, Formalquote
from mdatasync_server.models import NodeClient

class SampleNotInClassException(Exception):
    pass

class NotAuthorizedError(StandardError):
    pass

class MadasUser(User):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        User.__init__(self, *args, **kwargs)
        self.ldap_groups = None

    def set_ldap_groups(self, ldap_groups):
        if ldap_groups is None: ldap_groups = tuple()
        self.ldap_groups = ldap_groups
        
    @property
    def is_admin(self):
        assert self.ldap_groups is not None, "Ldap groups not set"
        return ('Administrators' in self.ldap_groups)

    @property
    def is_noderep(self):
        assert self.ldap_groups is not None, "Ldap groups not set"
        return ('Node Reps' in self.ldap_groups)

    @property
    def is_client(self):
        assert self.ldap_groups is not None, "Ldap groups not set"
        return len(self.ldap_groups) == 0

    def is_project_manager_of(self, project):
        return self.pk in [m.pk for m in project.managers.all()]
        
    def is_client_of(self, project):
        return (project.client and self.pk == project.client.pk)

class OrganismType(models.Model):
    """Currently, Microorganism, Plant, Animal or Human"""
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name

       
class BiologicalSource(models.Model):
    experiment = models.ForeignKey('Experiment')
    abbreviation = models.CharField(max_length=5)
    type = models.ForeignKey(OrganismType)
    information = models.TextField(null=True, blank=True)
    ncbi_id = models.PositiveIntegerField(null=True)
    label = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return str(self.label)
    
class AnimalInfo(models.Model):
    class Meta:
        verbose_name_plural = "Animal information"

    source = models.ForeignKey(BiologicalSource)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'U', u'Unknown')
    )
    sex = models.CharField(max_length=2, choices=GENDER_CHOICES, default=u'U')
    age = models.PositiveIntegerField(null=True, blank=True)
    parental_line = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.sex, str(self.age), self.parental_line)

class PlantInfo(models.Model):
    class Meta:
        verbose_name_plural = "Plant information"

    source = models.ForeignKey(BiologicalSource)
    development_stage = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    growing_place = models.CharField(max_length=255, null=True, blank=True)
    seeded_on = models.DateField(null=True, blank=True)
    transplated_on = models.DateField(null=True, blank=True)
    harvested_on = models.DateField(null=True, blank=True)
    harvested_at = models.TimeField(null=True, blank=True)
    night_temp_cels = models.PositiveIntegerField(null=True, blank=True)
    day_temp_cels = models.PositiveIntegerField(null=True, blank=True)
    light_hrs_per_day = models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)
    light_fluence = models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)
    light_source = models.TextField(null=True, blank=True)
    lamp_details = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s - %s" % (self.development_stage, self.growing_place)

class HumanInfo(models.Model):
    source = models.ForeignKey(BiologicalSource)
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
        (u'U', u'Unknown')
    )
    sex = models.CharField(null=True, max_length=2, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True)

    def __unicode__(self):
        return u"%s - %s - %s" % (self.sex, self.date_of_birth, self.location)

class MicrobialInfo(models.Model):
    source = models.ForeignKey(BiologicalSource)
    genus = models.CharField(max_length=255, null=True, blank=True)
    species = models.CharField(max_length=255, null=True, blank=True)
    culture_collection_id = models.CharField(max_length=255, null=True, blank=True)
    media = models.CharField(max_length=255, null=True, blank=True)
    fermentation_vessel = models.CharField(max_length=255, null=True, blank=True)
    fermentation_mode = models.CharField(max_length=255, null=True, blank=True)
    innoculation_density = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fermentation_volume = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    agitation = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ph = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    gas_type = models.CharField(max_length=255, null=True, blank=True)
    gas_flow_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    gas_delivery_method = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"%s - %s" % (self.genus, self.species)

class Organ(models.Model):
    experiment = models.ForeignKey('Experiment')
    name = models.CharField(max_length=255, null=True, blank=True)
    abbreviation = models.CharField(max_length=5)
    detail = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

class ExperimentStatus(models.Model):
    class Meta:
        verbose_name_plural = "Experiment statuses"

    name = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    created_on = models.DateField(null=False, default=date.today)
    client = models.ForeignKey(User, null=True)    
    managers = models.ManyToManyField(User, related_name='managed_projects')
    
    def __unicode__(self):
        return self.title + ' (' + self.client.username + ')'

class InstrumentMethod(models.Model):
    title = models.CharField(max_length=255)
    method_path = models.TextField()
    method_name = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    created_on = models.DateField(null=False, default=date.today)
    creator = models.ForeignKey(User)
    template = models.TextField()
    randomisation = models.BooleanField(default=False)
    blank_at_start = models.BooleanField(default=False)
    blank_at_end = models.BooleanField(default=False)
    blank_position = models.CharField(max_length=255,null=True)
    obsolete = models.BooleanField(default=False)
    obsolescence_date = models.DateField(null=True,blank=True)
    
    #future: quality control sample locations

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.version) 
        
class Experiment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    comment = models.TextField(null=True)
    users = models.ManyToManyField(User, through='UserExperiment', null=True)
    status = models.ForeignKey(ExperimentStatus, null=True)
    created_on = models.DateField(null=False, default=date.today)
    formal_quote = models.ForeignKey(Formalquote, null=True)
    job_number = models.CharField(max_length=30)
    project = models.ForeignKey(Project)
    instrument_method = models.ForeignKey(InstrumentMethod, null=True, blank=True)
    # ? files
    
    def ensure_dir(self):
        import settings, os
        
        yearpath = settings.REPO_FILES_ROOT + os.sep + 'experiments/' + str(self.created_on.year)
        monthpath = yearpath + '/' + str(self.created_on.month)
        exppath = monthpath + '/' + str(self.id)
        
        if not os.path.exists(exppath):
            os.makedirs(exppath)
            
        return exppath

    def __unicode__(self):
        return self.title

class StandardOperationProcedure(models.Model):
    responsible = models.CharField(max_length=255, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    area_where_valid = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    organisation = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=255, null=True, blank=True)
    defined_by = models.CharField(max_length=255, null=True, blank=True)
    replaces_document = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    attached_pdf = models.TextField(null=True, blank=True)
    experiments = models.ManyToManyField(Experiment, null=True, blank=True)

    def __unicode__(self):
        return self.label

class Treatment(models.Model):
    experiment = models.ForeignKey('Experiment')
    abbreviation = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name

class SampleTimeline(models.Model):
    experiment = models.ForeignKey('Experiment')
    abbreviation = models.CharField(max_length=5)
    timeline = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        if self.timeline == None:
            return ""
        return self.timeline

class SampleClass(models.Model):
    class Meta:
        verbose_name_plural = "Sample classes"

    class_id = models.CharField(max_length=255)
    experiment = models.ForeignKey(Experiment)
    biological_source = models.ForeignKey(BiologicalSource, null=True)
    treatments = models.ForeignKey(Treatment, null=True)
    timeline = models.ForeignKey(SampleTimeline,null=True)
    organ = models.ForeignKey(Organ, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        val = ''
        if self.biological_source is not None:
            if self.biological_source.abbreviation is not None:
                val = val + self.biological_source.abbreviation
        if self.treatments is not None:
            if self.treatments.abbreviation is not None:
                val = val + self.treatments.abbreviation
        if self.timeline is not None:
            if self.timeline.abbreviation is not None:
                val = val + self.timeline.abbreviation
        if self.organ is not None:
            if self.organ.abbreviation is not None:
                val = val + self.organ.abbreviation
        if val == '':
            val = 'class_' + str(self.id)
        return val

class Sample(models.Model):
    sample_id = models.CharField(max_length=255)
    sample_class = models.ForeignKey(SampleClass, null=True, blank=True)
    experiment = models.ForeignKey(Experiment)
    label = models.CharField(max_length=255)
    comment = models.TextField(null=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __unicode__(self):
        return str(self.label)

    def run_filename(self, run):
        if self.sample_class is None:
            print 'sample not in class'
            raise SampleNotInClassException
        else:
            return str(self.sample_class) + '-' + str(run.id) + '-' + str(self.id) + '.d'
    
class Run(models.Model):
    method = models.ForeignKey(InstrumentMethod)
    created_on = models.DateField(null=False, default=date.today)
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=255,null=True,blank=True)
    samples = models.ManyToManyField(Sample, through="RunSample")
    machine = models.ForeignKey(NodeClient)
    generated_output = models.TextField(null=True, blank=True)
    
    def sortedSamples(self):
        #TODO if method indicates randomisation and blanks, now is when we would do it
        return self.samples.all()
    
    def __unicode__(self):
        return "%s (%s v.%s)" % (self.title, self.method.title, self.method.version)

class SampleLog(models.Model):
    LOG_TYPES = (
            (0, u'Received'),
            (1, u'Stored'),
            (2, u'Prepared'),
            (3, u'Acquired'),
            (4, u'Data Processed')
        )
    type = models.PositiveIntegerField(choices=LOG_TYPES, default=0)
    changetimestamp = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True)
    sample = models.ForeignKey(Sample)
    
    def __unicode__(self):
        return "%s: %s" % (self.LOG_TYPES[self.type][1], self.description)

class UserInvolvementType(models.Model):
    """Principal Investigator or Involved User"""
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class UserExperiment(models.Model):
    user = models.ForeignKey(User)
    experiment = models.ForeignKey(Experiment)
    type = models.ForeignKey(UserInvolvementType)
    additional_info = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s-%s" % (self.user, self.experiment)

class RunSample(models.Model):
    run = models.ForeignKey(Run)
    sample = models.ForeignKey(Sample)
    filename = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = u'repository_run_samples'

    def __unicode__(self):
        return "Run: %s, Sample: %s, Filename: %s." % (self.run, self.sample, self.filename)
