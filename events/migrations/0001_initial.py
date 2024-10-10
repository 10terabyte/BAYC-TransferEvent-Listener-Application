# Generated by Django 5.1.2 on 2024-10-10 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransferEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_id', models.CharField(max_length=100, verbose_name='Token ID')),
                ('from_address', models.CharField(max_length=42, verbose_name='Sender Address')),
                ('to_address', models.CharField(max_length=42, verbose_name='Recipient Address')),
                ('transaction_hash', models.CharField(max_length=66, verbose_name='Transaction Hash')),
                ('block_number', models.IntegerField(verbose_name='Block Number')),
            ],
            options={
                'verbose_name': 'Transfer Event',
                'verbose_name_plural': 'Transfer Events',
                'ordering': ['-block_number'],
            },
        ),
    ]
