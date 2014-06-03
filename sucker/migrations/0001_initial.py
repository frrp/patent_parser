# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Citation'
        db.create_table(u'sucker_citation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docnum', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('pubdate', self.gf('django.db.models.fields.TextField')(max_length=16)),
            ('type', self.gf('django.db.models.fields.TextField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('code', self.gf('django.db.models.fields.TextField')(default='', max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'sucker', ['Citation'])

        # Adding model 'Person'
        db.create_table(u'sucker_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization_name', self.gf('django.db.models.fields.TextField')(null=True)),
            ('first_name', self.gf('django.db.models.fields.TextField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.TextField')(max_length=50)),
            ('address', self.gf('django.db.models.fields.TextField')(default='', max_length=50, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.TextField')(default='', max_length=50, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.TextField')(default='', max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'sucker', ['Person'])

        # Adding model 'Claim'
        db.create_table(u'sucker_claim', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clm_id', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
        ))
        db.send_create_signal(u'sucker', ['Claim'])

        # Adding model 'Patent'
        db.create_table(u'sucker_patent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_number', self.gf('django.db.models.fields.TextField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.TextField')(max_length=10)),
            ('publication_date', self.gf('django.db.models.fields.TextField')(max_length=16)),
            ('country', self.gf('django.db.models.fields.TextField')(max_length=10)),
            ('application_number', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('application_date', self.gf('django.db.models.fields.TextField')(max_length=16)),
            ('priority_number', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=20)),
            ('priority_date', self.gf('django.db.models.fields.TextField')(default='', max_length=16)),
            ('priority_country', self.gf('django.db.models.fields.TextField')(default='', max_length=10)),
            ('ipcmain', self.gf('django.db.models.fields.TextField')(default='', max_length=10)),
            ('ipcfurther', self.gf('django.db.models.fields.TextField')(default='', max_length=10)),
            ('title', self.gf('django.db.models.fields.TextField')(default='', max_length=60)),
            ('pctappnum', self.gf('django.db.models.fields.TextField')(default='', max_length=30)),
            ('pctpubnum', self.gf('django.db.models.fields.TextField')(default='', max_length=30)),
            ('abstract', self.gf('django.db.models.fields.TextField')(default='')),
            ('field', self.gf('django.db.models.fields.TextField')(default='', max_length=50)),
            ('background', self.gf('django.db.models.fields.TextField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('detaileddescription', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'sucker', ['Patent'])

        # Adding M2M table for field citations on 'Patent'
        m2m_table_name = db.shorten_name(u'sucker_patent_citations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patent', models.ForeignKey(orm[u'sucker.patent'], null=False)),
            ('citation', models.ForeignKey(orm[u'sucker.citation'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patent_id', 'citation_id'])

        # Adding M2M table for field applicants on 'Patent'
        m2m_table_name = db.shorten_name(u'sucker_patent_applicants')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patent', models.ForeignKey(orm[u'sucker.patent'], null=False)),
            ('person', models.ForeignKey(orm[u'sucker.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patent_id', 'person_id'])

        # Adding M2M table for field inventors on 'Patent'
        m2m_table_name = db.shorten_name(u'sucker_patent_inventors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patent', models.ForeignKey(orm[u'sucker.patent'], null=False)),
            ('person', models.ForeignKey(orm[u'sucker.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patent_id', 'person_id'])

        # Adding M2M table for field assignees on 'Patent'
        m2m_table_name = db.shorten_name(u'sucker_patent_assignees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patent', models.ForeignKey(orm[u'sucker.patent'], null=False)),
            ('person', models.ForeignKey(orm[u'sucker.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patent_id', 'person_id'])

        # Adding M2M table for field examiners on 'Patent'
        m2m_table_name = db.shorten_name(u'sucker_patent_examiners')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patent', models.ForeignKey(orm[u'sucker.patent'], null=False)),
            ('person', models.ForeignKey(orm[u'sucker.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patent_id', 'person_id'])

        # Adding M2M table for field claims on 'Patent'
        m2m_table_name = db.shorten_name(u'sucker_patent_claims')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patent', models.ForeignKey(orm[u'sucker.patent'], null=False)),
            ('claim', models.ForeignKey(orm[u'sucker.claim'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patent_id', 'claim_id'])

        # Adding M2M table for field forwardcitations on 'Patent'
        m2m_table_name = db.shorten_name(u'sucker_patent_forwardcitations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patent', models.ForeignKey(orm[u'sucker.patent'], null=False)),
            ('citation', models.ForeignKey(orm[u'sucker.citation'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patent_id', 'citation_id'])


    def backwards(self, orm):
        # Deleting model 'Citation'
        db.delete_table(u'sucker_citation')

        # Deleting model 'Person'
        db.delete_table(u'sucker_person')

        # Deleting model 'Claim'
        db.delete_table(u'sucker_claim')

        # Deleting model 'Patent'
        db.delete_table(u'sucker_patent')

        # Removing M2M table for field citations on 'Patent'
        db.delete_table(db.shorten_name(u'sucker_patent_citations'))

        # Removing M2M table for field applicants on 'Patent'
        db.delete_table(db.shorten_name(u'sucker_patent_applicants'))

        # Removing M2M table for field inventors on 'Patent'
        db.delete_table(db.shorten_name(u'sucker_patent_inventors'))

        # Removing M2M table for field assignees on 'Patent'
        db.delete_table(db.shorten_name(u'sucker_patent_assignees'))

        # Removing M2M table for field examiners on 'Patent'
        db.delete_table(db.shorten_name(u'sucker_patent_examiners'))

        # Removing M2M table for field claims on 'Patent'
        db.delete_table(db.shorten_name(u'sucker_patent_claims'))

        # Removing M2M table for field forwardcitations on 'Patent'
        db.delete_table(db.shorten_name(u'sucker_patent_forwardcitations'))


    models = {
        u'sucker.citation': {
            'Meta': {'object_name': 'Citation'},
            'code': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'docnum': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'pubdate': ('django.db.models.fields.TextField', [], {'max_length': '16'}),
            'type': ('django.db.models.fields.TextField', [], {'max_length': '10'})
        },
        u'sucker.claim': {
            'Meta': {'object_name': 'Claim'},
            'clm_id': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        u'sucker.patent': {
            'Meta': {'object_name': 'Patent'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'applicants': ('django.db.models.ManyToManyField', [], {'related_name': "'applicants'", 'symmetrical': 'False', 'to': u"orm['sucker.Person']"}),
            'application_date': ('django.db.models.fields.TextField', [], {'max_length': '16'}),
            'application_number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'assignees': ('django.db.models.ManyToManyField', [], {'related_name': "'assignees'", 'symmetrical': 'False', 'to': u"orm['sucker.Person']"}),
            'background': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            'citations': ('django.db.models.ManyToManyField', [], {'related_name': "'citations'", 'symmetrical': 'False', 'to': u"orm['sucker.Citation']"}),
            'claims': ('django.db.models.ManyToManyField', [], {'to': u"orm['sucker.Claim']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.TextField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'detaileddescription': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'document_number': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'examiners': ('django.db.models.ManyToManyField', [], {'related_name': "'examiners'", 'symmetrical': 'False', 'to': u"orm['sucker.Person']"}),
            'field': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50'}),
            'forwardcitations': ('django.db.models.ManyToManyField', [], {'related_name': "'forwardcitations'", 'symmetrical': 'False', 'to': u"orm['sucker.Citation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventors': ('django.db.models.ManyToManyField', [], {'related_name': "'inventors'", 'symmetrical': 'False', 'to': u"orm['sucker.Person']"}),
            'ipcfurther': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '10'}),
            'ipcmain': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '10'}),
            'pctappnum': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '30'}),
            'pctpubnum': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '30'}),
            'priority_country': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '10'}),
            'priority_date': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '16'}),
            'priority_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '20'}),
            'publication_date': ('django.db.models.fields.TextField', [], {'max_length': '16'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '60'}),
            'type': ('django.db.models.fields.TextField', [], {'max_length': '10'})
        },
        u'sucker.person': {
            'Meta': {'object_name': 'Person'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            'organization_name': ('django.db.models.fields.TextField', [], {'null': 'True'})
        }
    }

    complete_apps = ['sucker']