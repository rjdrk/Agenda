from rest_framework import serializers
from .models import Contacto, Telefono

class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ['id','numero_telefono','referencia']

class ContactoSerializer(serializers.ModelSerializer):
    telefonos = TelefonoSerializer(many=True)

    class Meta:
        model = Contacto
        fields = ['id','nombre','apellido','email','telefonos']

    def create(self, validated_data):
        telefonos_data = validated_data.pop('telefonos', [])
        contacto = Contacto.objects.create(**validated_data)
        for telefono in telefonos_data:
            Telefono.objects.create(person=contacto, **telefono)
        return contacto

    def update(self, instance, validated_data):
        telefonos_data = validated_data.pop('telefonos', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if telefonos_data is not None:
            instance.telefonos.all().delete()
            for telefono in telefonos_data:
                Telefono.objects.create(person=instance, **telefono)
        return instance
