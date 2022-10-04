from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length = 20)),
                ('nickname', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('profile_image', models.URLField(blank=True)),
                ('can_search_by_email;', models.BooleanField(default=True)),
                ('is_shown;', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User')),
                ('is_done', models.BooleanField(default='FALSE')),
                ('is_stored', models.BooleanField(default='FALSE')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='Todo',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Todo', to='api.User'),
        ),
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('bg_color', models.CharField(max_length=10)),
                ('feeling_temp', models.CharField(max_length=10)),
                ('emoji', models.CharField(max_lenght=10)),
                ('is_secret', models.BooleanField(default='FALSE')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='Diary',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Diary', to='api.User'),
        ),
    ]