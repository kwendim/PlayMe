# Generated by Django 2.1.3 on 2019-02-19 02:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('rating', models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('high_score', models.PositiveIntegerField(blank=True, default=0)),
                ('description', models.TextField(blank=True)),
                ('link', models.URLField(verbose_name='game_url')),
                ('purchase_number', models.PositiveIntegerField(blank=True, default=0)),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('category', models.CharField(choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Combat', 'Combat'), ('Educational', 'Educational'), ('Puzzle', 'Puzzle'), ('RPG', 'RPG'), ('Sports', 'Sports'), ('Strategy', 'Strategy')], max_length=20)),
                ('price', models.IntegerField(blank=True, default=0)),
                ('thumbnail', models.ImageField(blank=True, default='def.jpg', upload_to='thumbnail')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_developer', models.BooleanField(default=False)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_score', models.FloatField(blank=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_state', models.TextField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.PositiveIntegerField()),
                ('state', models.CharField(choices=[('PE', 'pending'), ('CO', 'confirmed')], default='PE', max_length=9)),
                ('reference', models.IntegerField(blank=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Game')),
                ('payee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Payee', to='backend.Profile')),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Payer', to='backend.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Profile'),
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together={('game', 'player')},
        ),
    ]
