# Generated by Django 4.2.4 on 2023-08-17 04:37

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mkt_id', models.BigIntegerField(null=True, unique=True)),
                ('google_id', models.BigIntegerField(null=True, unique=True)),
                ('first_name', models.CharField(max_length=15, null=True)),
                ('last_name', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(max_length=15, unique=True)),
                ('email_verified_at', models.DateTimeField(null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('phone_verified_at', models.DateTimeField(null=True)),
                ('avatar', models.CharField(max_length=255, null=True)),
                ('role', models.SmallIntegerField(default=1)),
                ('two_fa_enabled_at', models.DateTimeField(null=True)),
                ('two_fa_secret', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
                'ordering': ['-created_at', '-updated_at', 'id'],
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(null=True)),
                ('useragent', models.TextField(max_length=500)),
                ('ip', models.CharField(max_length=255)),
                ('session_id', models.CharField(max_length=255, null=True)),
                ('extra_info', models.JSONField()),
                ('is_verified', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='usermodel',
            index=models.Index(fields=['email', 'id'], name='user_email_de573b_idx'),
        ),
    ]