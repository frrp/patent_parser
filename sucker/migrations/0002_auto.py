# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field forwardcitations on 'Patent'
        m2m_table_name = db.shorten_name('ma_sucker_patent_forwardcitations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patent', models.ForeignKey(orm['ma_sucker.patent'], null=False)),
            ('citation', models.ForeignKey(orm['ma_sucker.citation'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patent_id', 'citation_id'])


    def backwards(self, orm):
        # Removing M2M table for field forwardcitations on 'Patent'
        db.delete_table(db.shorten_name('ma_sucker_patent_forwardcitations'))


    models = {
        'ma_sucker.citation': {
            'Meta': {'object_name': 'Citation'},
            'code': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'docnum': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'pubdate': ('django.db.models.fields.TextField', [], {'max_length': '16'}),
            'type': ('django.db.models.fields.TextField', [], {'max_length': '10'})
        },
        'ma_sucker.claim': {
            'Meta': {'object_name': 'Claim'},
            'clm_id': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        },
        'ma_sucker.patent': {
            'Meta': {'object_name': 'Patent'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'applicants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'applicants'", 'symmetrical': 'False', 'to': u"orm['ma_sucker.Person']"}),
            'application_date': ('django.db.models.fields.TextField', [], {'max_length': '16'}),
            'application_number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'assignees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assignees'", 'symmetrical': 'False', 'to': u"orm['ma_sucker.Person']"}),
            'background': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            'citations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'citations'", 'symmetrical': 'False', 'to': u"orm['ma_sucker.Citation']"}),
            'claims': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ma_sucker.Claim']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.TextField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'detaileddescription': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'document_number': ('django.db.models.fields.TextField', [], {'max_length': '20'}),
            'examiners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'examiners'", 'symmetrical': 'False', 'to': u"orm['ma_sucker.Person']"}),
            'field': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50'}),
            'forwardcitations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'forwardcitations'", 'symmetrical': 'False', 'to': u"orm['ma_sucker.Citation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'inventors'", 'symmetrical': 'False', 'to': u"orm['ma_sucker.Person']"}),
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
        'ma_sucker.person': {
            'Meta': {'object_name': 'Person'},
            'address': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.TextField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.TextField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['ma_sucker']