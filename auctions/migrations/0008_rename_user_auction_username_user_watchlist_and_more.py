# Generated by Django 4.2.6 on 2023-11-27 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auction_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='user',
            new_name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(to='auctions.auction'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auction'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auction'),
        ),
    ]