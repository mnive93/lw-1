# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InviteEmails'
        db.create_table(u'invites_inviteemails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emailaddress', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'invites', ['InviteEmails'])


    def backwards(self, orm):
        # Deleting model 'InviteEmails'
        db.delete_table(u'invites_inviteemails')


    models = {
        u'invites.inviteemails': {
            'Meta': {'object_name': 'InviteEmails'},
            'emailaddress': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['invites']