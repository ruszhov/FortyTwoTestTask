# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table(u'hello_contact')
        # Adding model 'Contact'
        db.create_table(u'hello_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('other_contacts', self.gf('django.db.models.fields.TextField')(max_length=200, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'hello', ['Contact'])

        # Deleting model 'HttpRequestLog'
        db.delete_table(u'hello_httprequestlog')
        # Adding model 'HttpRequestLog'
        db.create_table(u'hello_httprequestlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('request_method', self.gf('django.db.models.fields.CharField')(max_length=6, db_index=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('server_protocol', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'hello', ['HttpRequestLog'])

        # Deleting model 'ModelActionLog'
        db.delete_table(u'hello_modelactionlog')
        # Adding model 'ModelActionLog'
        db.create_table(u'hello_modelactionlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('instance', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'hello', ['ModelActionLog'])

    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table(u'hello_contact')

        # Deleting model 'HttpRequestLog'
        db.delete_table(u'hello_httprequestlog')

        # Deleting model 'ModelActionLog'
        db.delete_table(u'hello_modelactionlog')

    models = {
        u'hello.contact': {
            'Meta': {'object_name': 'Contact'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'hello.httprequestlog': {
            'Meta': {'object_name': 'HttpRequestLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'request_method': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_index': 'True'}),
            'server_protocol': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'hello.modelactionlog': {
            'Meta': {'object_name': 'ModelActionLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['hello']