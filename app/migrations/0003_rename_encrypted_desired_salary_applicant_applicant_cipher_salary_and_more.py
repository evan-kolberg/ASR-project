# Generated by Django 4.2.3 on 2023-07-27 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_salary_applicant_encrypted_desired_salary_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='encrypted_desired_salary',
            new_name='applicant_cipher_salary',
        ),
        migrations.RenameField(
            model_name='employer',
            old_name='encrypted_expected_salary',
            new_name='employer_cipher_salary',
        ),
    ]
