from .models import *

from rest_framework import serializers


class BaseManyToManySerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        data = dict(data)
        for field_name, model_class in self.get_id_conversion_mappings():
            self._convert_ids_to_unique_ids(data, field_name, model_class)
        return super().to_internal_value(data)

    def _convert_ids_to_unique_ids(self, data, field_name, model_class):
        if field_name in data:
            ids = data.get(field_name)
            if not isinstance(ids, list):
                ids = [ids]
            objects = model_class.objects.filter(id__in=ids)
            id_map = {}
            for obj in objects:
                if obj.id not in id_map:
                    id_map[obj.id] = []
                id_map[obj.id].append(obj.unique_id)
            data[field_name] = [unique_id for id in ids for unique_id in id_map.get(id, [])]

    def create(self, validated_data):
        many_to_many_data = {field_name: validated_data.pop(field_name, []) for field_name, field_class in
                             self.get_many_to_many_fields()}
        instance = self.Meta.model.objects.create(**validated_data)
        for field_name, field_class in self.get_many_to_many_fields():
            if field_name in many_to_many_data:
                field_value = many_to_many_data[field_name]
                if hasattr(instance, field_name):
                    getattr(instance, field_name).set(field_value)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name, _ in self.get_many_to_many_fields():
            if hasattr(instance, field_name):
                representation[field_name] = [item.id for item in getattr(instance, field_name).all()]
        return representation

    def get_id_conversion_mappings(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_many_to_many_fields(self):
        raise NotImplementedError("Subclasses must implement this method.")


class AttributeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeName
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'


class AttributeSerializer(BaseManyToManySerializer):
    nazev_atributu_id = serializers.PrimaryKeyRelatedField(queryset=AttributeName.objects.all(), many=True,
                                                           required=False)
    hodnota_atributu_id = serializers.PrimaryKeyRelatedField(queryset=AttributeValue.objects.all(), many=True,
                                                             required=False)

    class Meta:
        model = Attribute
        fields = ["unique_id", "id", "nazev_atributu_id", "hodnota_atributu_id"]

    def get_id_conversion_mappings(self):
        return [
            ('nazev_atributu_id', AttributeName),
            ('hodnota_atributu_id', AttributeValue)
        ]

    def get_many_to_many_fields(self):
        return [
            ('nazev_atributu_id', AttributeName),
            ('hodnota_atributu_id', AttributeValue)
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductImageSerializer(BaseManyToManySerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, required=False)
    obrazek_id = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True, required=False)

    class Meta:
        model = ProductImage
        fields = ["unique_id", "id", "product", "obrazek_id", "nazev"]

    def get_id_conversion_mappings(self):
        return [
            ('product', Product),
            ('obrazek_id', Image)
        ]

    def get_many_to_many_fields(self):
        return [
            ('product', Product),
            ('obrazek_id', Image)
        ]


class CatalogSerializer(BaseManyToManySerializer):
    obrazek_id = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True, required=False)
    products_ids = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, required=False)
    attributes_ids = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), many=True, required=False)

    class Meta:
        model = Catalog
        fields = ["unique_id", "id", "nazev", "obrazek_id", "products_ids", "attributes_ids"]

    def get_id_conversion_mappings(self):
        return [
            ('obrazek_id', Image),
            ('products_ids', Product),
            ('attributes_ids', Attribute)
        ]

    def get_many_to_many_fields(self):
        return [
            ('obrazek_id', Image),
            ('products_ids', Product),
            ('attributes_ids', Attribute)
        ]


class ProductAttributesSerializer(BaseManyToManySerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, required=False)

    class Meta:
        model = ProductAttributes
        fields = ["unique_id", "id", "attribute", "product"]

    def get_id_conversion_mappings(self):
        return [
            ('product', Product),
        ]

    def get_many_to_many_fields(self):
         return [
            ('product', Product),
        ]
