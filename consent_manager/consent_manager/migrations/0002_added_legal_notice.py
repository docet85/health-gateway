# Generated by Django 2.2.5 on 2020-04-06 14:35

from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('consent_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consentmanageruser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.CreateModel(
            name='LegalNoticeVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', martor.models.MartorField()),
                ('change_comment', models.CharField(blank=True, max_length=200)),
                ('v_major', models.IntegerField(default=0)),
                ('v_minor', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='consent_manager.Endpoint')),
                ('previous_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='consent_manager.LegalNoticeVersion')),
            ],
        ),
        migrations.CreateModel(
            name='LegalNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_major', models.BooleanField(default=False)),
                ('text', martor.models.MartorField()),
                ('change_comment', models.CharField(blank=True, max_length=200)),
                ('current_version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='consent_manager.LegalNoticeVersion')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='consent_manager.Endpoint')),
            ],
        ),
        migrations.AddField(
            model_name='consent',
            name='legal_notice_version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='consent_manager.LegalNoticeVersion'),
        ),
    ]