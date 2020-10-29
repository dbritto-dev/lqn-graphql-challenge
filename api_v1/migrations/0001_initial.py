# Generated by Django 3.1 on 2020-10-28 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('opening_text', models.TextField()),
                ('release_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fist_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Starship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('length', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('home_planet', models.CharField(max_length=150)),
                ('appears_in', models.ManyToManyField(blank=True, to='api_v1.Episode')),
                ('friends', models.ManyToManyField(blank=True, related_name='friends_by_human', to='api_v1.Human')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='episode',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes_by_director', to='api_v1.person'),
        ),
        migrations.AddField(
            model_name='episode',
            name='planets',
            field=models.ManyToManyField(related_name='episodes_by_planets', to='api_v1.Planet'),
        ),
        migrations.AddField(
            model_name='episode',
            name='producers',
            field=models.ManyToManyField(related_name='episodes_by_producers', to='api_v1.Person'),
        ),
        migrations.CreateModel(
            name='Droid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('primary_function', models.CharField(max_length=150)),
                ('appears_in', models.ManyToManyField(blank=True, to='api_v1.Episode')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]