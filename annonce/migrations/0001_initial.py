# Generated by Django 5.0.2 on 2024-03-19 02:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='creer_annonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annonce', models.CharField(max_length=30)),
                ('marque_voiture', models.CharField(max_length=50)),
                ('modele_voiture', models.CharField(max_length=50)),
                ('prix_voiture', models.BigIntegerField()),
                ('body_style', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('debut_promo', models.DateTimeField()),
                ('fin_promo', models.DateTimeField()),
                ('description', models.CharField(max_length=150)),
                ('type', models.CharField(max_length=10)),
                ('photo_voiture', models.ImageField(upload_to='annonces/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('annonce_achieve', 'annonce_achieve')], default='pending', max_length=20)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('annonce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to='annonce.creer_annonce')),
            ],
        ),
    ]
