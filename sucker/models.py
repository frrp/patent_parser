from django.db import models

from large_data_admin import db_fields as lda

"""
This is a data model roughly corresponding to this (from patent_codes.py):

id INTEGER PRIMARY KEY, docnum text, type text, pubdate text, country text,
                  appnum text, appdate text, prioritynum text, prioritydate text, prioritycountry text,
                  ipcmain text, ipcfurther text, title text, citations text, numcitations integer,
                  applicant text, inventors text, assignee text, examiner text, pctappnum text,
                  pctpubnum text, abstract text, field text, background text,
                  description text, detaileddescription text, claims text,
                  forwardcitations integer, spare1 text, spare2 real, spare3 text,
                  spare4 text, spare5 text, spare6 text, ai integer))
"""

class Citation(models.Model):
    docnum = models.TextField(max_length=20)
    pubdate = models.TextField(max_length=16)
    type = models.TextField(max_length=10)
    name = models.TextField(max_length=20)  # some name, main author of patent?
    code = models.TextField(max_length=10, blank=True, null=True, default="")  # alpha-numeric code of the examiner?

    def __unicode__(self):
        return u"%s" % (self.name, )

class Person(models.Model):  # this might be better called assignee with name not mandatory
    organization_name = models.TextField(null=True)
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    address = models.TextField(max_length=50, blank=True, null=True, default="")
    city = models.TextField(max_length=50, blank=True, null=True, default="")
    country = models.TextField(max_length=20, blank=True, null=True, default="")

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name, )

class Claim(models.Model):
    clm_id = models.TextField(max_length=20)
    text = models.TextField(max_length=100)

    def __unicode__(self):
        return u"%s" % (self.clm_id, )

class Patent(models.Model):
    document_number = models.TextField(max_length=20)
    type = models.TextField(max_length=10)
    publication_date = models.TextField(max_length=16)
    country = models.TextField(max_length=10)
    application_number = models.IntegerField(max_length=10)
    application_date = models.TextField(max_length=16)
    priority_number = models.IntegerField(max_length=20, default=0)
    priority_date = models.TextField(max_length=16, default="")
    priority_country = models.TextField(max_length=10, default="")
    ipcmain = models.TextField(max_length=10, default="")
    ipcfurther = models.TextField(max_length=10, default="")
    title = models.TextField(max_length=60, default="")
    citations = lda.ManyToManyField(Citation, "docnum", related_name="citations")
    applicants = lda.ManyToManyField(Person, "last_name", related_name="applicants")
    inventors = lda.ManyToManyField(Person, "last_name", related_name="inventors")
    assignees = lda.ManyToManyField(Person, "last_name", related_name="assignees")
    examiners = lda.ManyToManyField(Person, "last_name", related_name="examiners")
    pctappnum = models.TextField(max_length=30, default="")  # find in data and check!
    pctpubnum = models.TextField(max_length=30, default="")  # find in data and check!
    abstract = models.TextField(default="")
    field = models.TextField(max_length=50, default="")  # find in data and check!
    background = models.TextField(max_length=50)  # find in data and check!
    description = models.TextField(default="")
    detaileddescription = models.TextField(default="")
    claims = lda.ManyToManyField(Claim, "clm_id")
    forwardcitations = lda.ManyToManyField(Citation, "docnum", related_name="forwardcitations")  # is it OK?
    
    # ai = models.IntegerField(max_length=4)  # pointer to the AI db that contains NLP parsed data from each patent
                  
    def __unicode__(self):
        return u"%s %s" % (self.document_number, self.title, )

    """
    spare1
    spare2
    spare3
    spare4
    spare5
    spare6
    """
