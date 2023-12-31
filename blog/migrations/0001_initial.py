# Generated by Django 4.2.2 on 2023-07-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogpost',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=60)),
                ('head0', models.CharField(default='', max_length=600)),
                ('chead0', models.CharField(default='', max_length=6000)),
                ('head1', models.CharField(default='', max_length=600)),
                ('chead1', models.CharField(default='', max_length=6000)),
                ('head2', models.CharField(default='', max_length=600)),
                ('chead2', models.CharField(default='', max_length=6000)),
                ('thumbainail', models.ImageField(default='', upload_to='blog/images')),
            ],
        ),
    ]
