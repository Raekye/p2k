# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 22:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FlagPass',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroundItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tag', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('metadata', models.BinaryField()),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hp', models.IntegerField()),
                ('avatar', models.IntegerField()),
                ('gold', models.IntegerField()),
                ('centre_lat', models.FloatField()),
                ('centre_lon', models.FloatField()),
                ('pos_lat', models.FloatField()),
                ('pos_lon', models.FloatField()),
                ('status', models.CharField(max_length=64)),
                ('bio', models.CharField(max_length=256)),
                ('clan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='main.Clan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tag', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('metadata', models.BinaryField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='main.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tag', models.IntegerField()),
                ('transient_exp', models.IntegerField()),
                ('total_exp', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tag', models.IntegerField()),
                ('hp', models.IntegerField()),
                ('metadata', models.BinaryField()),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TradePostListing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tag', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('metadata', models.BinaryField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CityFlag',
            fields=[
                ('structure_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Structure')),
                ('level', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('main.structure',),
        ),
        migrations.CreateModel(
            name='NatureStructure',
            fields=[
                ('structure_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Structure')),
                ('last_harvest', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
            bases=('main.structure',),
        ),
        migrations.CreateModel(
            name='PlayerStructure',
            fields=[
                ('structure_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Structure')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.structure',),
        ),
        migrations.AddField(
            model_name='flagpass',
            name='builder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flag_passes_given', to='main.Player'),
        ),
        migrations.AddField(
            model_name='flagpass',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flag_passes_received', to='main.Player'),
        ),
        migrations.AddField(
            model_name='clan',
            name='leader',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clan_lead', to='main.Player'),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('playerstructure_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.PlayerStructure')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'abstract': False,
            },
            bases=('main.playerstructure',),
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('playerstructure_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.PlayerStructure')),
                ('level', models.IntegerField()),
                ('availability', models.IntegerField()),
                ('fee', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('main.playerstructure',),
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('playerstructure_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.PlayerStructure')),
                ('fee', models.IntegerField()),
                ('skill', models.IntegerField()),
                ('level', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('main.playerstructure',),
        ),
        migrations.CreateModel(
            name='TradePost',
            fields=[
                ('playerstructure_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.PlayerStructure')),
                ('corresponding_city', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='city2', to='main.City')),
            ],
            options={
                'abstract': False,
            },
            bases=('main.playerstructure',),
        ),
        migrations.AddField(
            model_name='playerstructure',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Player'),
        ),
        migrations.AddField(
            model_name='tradepostlisting',
            name='tradepost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TradePost'),
        ),
        migrations.AddField(
            model_name='player',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='main.City'),
        ),
        migrations.AddField(
            model_name='cityflag',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.City'),
        ),
        migrations.AddField(
            model_name='city',
            name='major',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_cities', to='main.Player'),
        ),
    ]
