# Generated by Django 3.1 on 2020-08-15 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cls_name', models.TextField()),
                ('ownedby', models.TextField()),
                ('clsCode', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MutualTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cls_name', models.TextField()),
                ('ownedby', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(max_length=20)),
                ('cls_name', models.TextField()),
                ('ownedby', models.TextField()),
            ],
        ),
    ]
