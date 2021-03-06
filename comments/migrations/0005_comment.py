# Generated by Django 2.1.3 on 2018-11-25 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20181124_0559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.User')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.Post')),
            ],
        ),
    ]
