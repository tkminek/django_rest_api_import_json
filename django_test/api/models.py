from django.db import models


class AttributeValue(models.Model):
    unique_id = models.AutoField(primary_key=True)
    id = models.IntegerField(unique=True)
    hodnota = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"AttributeValue with id: {self.id}"


class AttributeName(models.Model):
    unique_id = models.AutoField(primary_key=True)
    id = models.IntegerField()
    nazev = models.CharField(max_length=255, null=True, blank=True)
    kod = models.CharField(max_length=255, null=True, blank=True)
    zobrazit = models.BooleanField(default=False)

    def __str__(self):
        return f"AttributeName with id: {self.id} and unique_id: {self.unique_id}"


class Attribute(models.Model):
    unique_id = models.AutoField(primary_key=True)
    id = models.IntegerField(unique=True)
    nazev_atributu_id = models.ManyToManyField(AttributeName, through='AttributeAttributeNameMapping')
    hodnota_atributu_id = models.ManyToManyField(AttributeValue, through='AttributeAttributeValueMapping')

    def __str__(self):
        return f"Attribute with id: {self.id}"


class AttributeAttributeNameMapping(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_name = models.ForeignKey(AttributeName, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute', 'attribute_name')


class AttributeAttributeValueMapping(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute', 'attribute_value')


class Product(models.Model):
    unique_id = models.AutoField(primary_key=True)
    id = models.IntegerField()
    nazev = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cena = models.FloatField(null=True, blank=True)
    mena = models.CharField(max_length=256, null=True, blank=True)
    published_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Product with id: 'self.id'"


class ProductAttributes(models.Model):
    unique_id = models.AutoField(primary_key=True)
    id = models.IntegerField()
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, to_field='id')
    product = models.ManyToManyField(Product, through='ProductAttributesProductMapping')

    def __str__(self):
        return f"ProductAttributes with id: {self.id}"


class ProductAttributesProductMapping(models.Model):
    product_attributes = models.ForeignKey(ProductAttributes, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product_attributes', 'product')


class Image(models.Model):
    unique_id = models.AutoField(primary_key=True)
    id = models.IntegerField()
    obrazek = models.URLField(null=True, blank=True)
    nazev = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Image with id: 'self.id'"


class ProductImage(models.Model):
    unique_id = models.AutoField(primary_key=True)
    id = models.IntegerField(null=True, blank=True)
    product = models.ManyToManyField(Product, through='ProductImageProductMapping')
    obrazek_id = models.ManyToManyField(Image, through='ProductImageImageMapping')
    nazev = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"ProductImage with id: 'self.id'"


class ProductImageProductMapping(models.Model):
    product_image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product_image', 'product')


class ProductImageImageMapping(models.Model):
    product_image = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product_image', 'image')


class Catalog(models.Model):
    unique_id = models.AutoField(primary_key=True)
    id = models.IntegerField(null=True, blank=True)
    nazev = models.CharField(max_length=256, null=True, blank=True)
    obrazek_id = models.ManyToManyField(Image, through='CatalogImageMapping')
    products_ids = models.ManyToManyField(Product, through='CatalogProductMapping')
    attributes_ids = models.ManyToManyField(Attribute, through='CatalogAttributeMapping')

    def __str__(self):
        return f"Catalog with id: 'self.id'"


class CatalogImageMapping(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('catalog', 'image')


class CatalogProductMapping(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('catalog', 'product')


class CatalogAttributeMapping(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('attribute', 'attribute')
