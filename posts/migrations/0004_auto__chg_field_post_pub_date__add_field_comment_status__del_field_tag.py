# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Post.pub_date'
        db.alter_column('posts_post', 'pub_date', self.gf('django.db.models.fields.DateField')())
        # Adding field 'Comment.status'
        db.add_column('posts_comment', 'status',
                      self.gf('django.db.models.fields.CharField')(default='P', max_length=2),
                      keep_default=False)

        # Deleting field 'Tag.post'
        db.delete_column('posts_tag', 'post_id')

        # Adding M2M table for field post on 'Tag'
        db.create_table('posts_tag_post', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['posts.tag'], null=False)),
            ('post', models.ForeignKey(orm['posts.post'], null=False))
        ))
        db.create_unique('posts_tag_post', ['tag_id', 'post_id'])


    def backwards(self, orm):

        # Changing field 'Post.pub_date'
        db.alter_column('posts_post', 'pub_date', self.gf('django.db.models.fields.DateTimeField')())
        # Deleting field 'Comment.status'
        db.delete_column('posts_comment', 'status')

        # Adding field 'Tag.post'
        db.add_column('posts_tag', 'post',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=datetime.datetime(2013, 1, 4, 0, 0), to=orm['posts.Post']),
                      keep_default=False)

        # Removing M2M table for field post on 'Tag'
        db.delete_table('posts_tag_post')


    models = {
        'posts.comment': {
            'Meta': {'object_name': 'Comment'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['posts.Post']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '2'})
        },
        'posts.post': {
            'Meta': {'object_name': 'Post'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'posts.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['posts.Post']", 'symmetrical': 'False'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['posts']