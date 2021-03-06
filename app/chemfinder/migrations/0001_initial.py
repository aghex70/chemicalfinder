# Generated by Django 2.2.9 on 2020-11-09 19:27

import chemfinder.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NER',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('label', models.CharField(max_length=50, null=True)),
                ('ner_type', models.CharField(choices=[('NER', 'NER'), ('ChemNER', 'ChemNER'), ('TrainedNER', 'TrainedNER')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=25, null=True)),
                ('document_number', models.CharField(max_length=25, null=True)),
                ('kind', models.CharField(max_length=25, null=True)),
                ('date', models.DateField(null=True)),
                ('title', models.TextField()),
                ('abstract', models.TextField()),
                ('description', models.TextField()),
                ('inventors', djongo.models.fields.ArrayField(model_container=chemfinder.models.Inventor)),
                ('created_date', models.DateTimeField(blank=True)),
            ],
        ),
    ]
