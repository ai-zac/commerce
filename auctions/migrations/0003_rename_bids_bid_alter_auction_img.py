# Generated by Django 4.2.6 on 2023-11-11 02:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_auction_category_comment_bids_auction_categories"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Bids",
            new_name="Bid",
        ),
        migrations.AlterField(
            model_name="auction",
            name="img",
            field=models.TextField(null=True),
        ),
    ]
