# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StateLog'
        db.create_table('django_fsm_log_statelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm["%s.%s" % (User._meta.app_label, User._meta.object_name)], null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('transition', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('django_fsm_log', ['StateLog'])


    def backwards(self, orm):
        # Deleting model 'StateLog'
        db.delete_table('django_fsm_log_statelog')


    models = {
        "%s.%s" % (User._meta.app_label, User._meta.module_name): {
            'Meta': {'object_name': User.__name__},
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'django_fsm_log.statelog': {
            'Meta': {'object_name': 'StateLog'},
            'by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s.%s']" % (User._meta.app_label, User._meta.object_name), 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'transition': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['django_fsm_log']
