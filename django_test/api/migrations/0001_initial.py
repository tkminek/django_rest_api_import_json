# Generated by Django 4.2.15 on 2024-08-17 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attribute",
            fields=[
                ("unique_id", models.AutoField(primary_key=True, serialize=False)),
                ("id", models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="AttributeName",
            fields=[
                ("unique_id", models.AutoField(primary_key=True, serialize=False)),
                ("id", models.IntegerField()),
                ("nazev", models.CharField(blank=True, max_length=255, null=True)),
                ("kod", models.CharField(blank=True, max_length=255, null=True)),
                ("zobrazit", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="AttributeValue",
            fields=[
                ("unique_id", models.AutoField(primary_key=True, serialize=False)),
                ("id", models.IntegerField(unique=True)),
                ("hodnota", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="AttributeAttributeValueMapping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.attribute"
                    ),
                ),
                (
                    "attribute_value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.attributevalue",
                    ),
                ),
            ],
            options={"unique_together": {("attribute", "attribute_value")},},
        ),
        migrations.CreateModel(
            name="AttributeAttributeNameMapping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.attribute"
                    ),
                ),
                (
                    "attribute_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.attributename",
                    ),
                ),
            ],
            options={"unique_together": {("attribute", "attribute_name")},},
        ),
        migrations.AddField(
            model_name="attribute",
            name="hodnota_atributu_id",
            field=models.ManyToManyField(
                through="api.AttributeAttributeValueMapping", to="api.attributevalue"
            ),
        ),
        migrations.AddField(
            model_name="attribute",
            name="nazev_atributu_id",
            field=models.ManyToManyField(
                through="api.AttributeAttributeNameMapping", to="api.attributename"
            ),
        ),
    ]
