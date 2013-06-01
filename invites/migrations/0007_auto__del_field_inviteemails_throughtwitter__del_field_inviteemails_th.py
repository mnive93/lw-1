# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'InviteEmails.throughtwitter'
        db.delete_column(u'invites_inviteemails', 'throughtwitter')

        # Deleting field 'InviteEmails.throughfb'
        db.delete_column(u'invites_inviteemails', 'throughfb')


    def backwards(self, orm):
        # Adding field 'InviteEmails.throughtwitter'
        db.add_column(u'invites_inviteemails', 'throughtwitter',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'InviteEmails.throughfb'
        db.add_column(u'invites_inviteemails', 'throughfb',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        u'invites.inviteemails': {
            'Meta': {'object_name': 'InviteEmails'},
            'emailaddress': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['invites']