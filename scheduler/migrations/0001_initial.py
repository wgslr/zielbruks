# Generated by Django 2.1.7 on 2019-06-12 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conflict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conflict_type', models.CharField(choices=[('ROOM', 'ROOM'), ('PROFESSOR', 'PROFESSOR'), ('GROUP', 'GROUP')], max_length=20)),
                ('object_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Group name')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Lesson name')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='scheduler.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Professor name')),
                ('surname', models.CharField(max_length=100, verbose_name='Professor surname')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='Professor email')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=30, unique=True, verbose_name='Room number')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Student name')),
                ('surname', models.CharField(max_length=100, verbose_name='Student surname')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='Student email')),
                ('index', models.CharField(max_length=30, null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='scheduler.Group')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='scheduler.Professor'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='scheduler.Room'),
        ),
        migrations.AddField(
            model_name='conflict',
            name='first_lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_lesson', to='scheduler.Lesson'),
        ),
        migrations.AddField(
            model_name='conflict',
            name='second_lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_lesson', to='scheduler.Lesson'),
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('name', 'professor', 'room', 'group', 'start_time', 'end_time')},
        ),
    ]
