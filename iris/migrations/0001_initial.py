# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Topic'
        db.create_table('iris_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('creator_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('creator_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('iris', ['Topic'])

        # Adding model 'Item'
        db.create_table('iris_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['iris.Topic'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('creator_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['contenttypes.ContentType'])),
            ('creator_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('iris', ['Item'])

        # Adding model 'Participant'
        db.create_table('iris_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='participants', to=orm['iris.Topic'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('item_last_read', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['iris.Item'], null=True, blank=True)),
        ))
        db.send_create_signal('iris', ['Participant'])

        # Adding model 'ParticipantJoin'
        db.create_table('iris_participantjoin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['iris.Participant'])),
        ))
        db.send_create_signal('iris', ['ParticipantJoin'])


    def backwards(self, orm):
        
        # Deleting model 'Topic'
        db.delete_table('iris_topic')

        # Deleting model 'Item'
        db.delete_table('iris_item')

        # Deleting model 'Participant'
        db.delete_table('iris_participant')

        # Deleting model 'ParticipantJoin'
        db.delete_table('iris_participantjoin')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'iris.item': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Item'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'creator_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'creator_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['iris.Topic']"})
        },
        'iris.participant': {
            'Meta': {'object_name': 'Participant'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_last_read': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['iris.Item']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participants'", 'to': "orm['iris.Topic']"})
        },
        'iris.participantjoin': {
            'Meta': {'object_name': 'ParticipantJoin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['iris.Participant']"})
        },
        'iris.topic': {
            'Meta': {'ordering': "('modified',)", 'object_name': 'Topic'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'creator_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['iris']
