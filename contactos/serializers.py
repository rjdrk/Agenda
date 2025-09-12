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
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        telefonos_data = validated_data.pop('telefonos')
        contacto = Contacto.objects.create(**validated_data)
        for telefono_data  in telefonos_data:
            Telefono.objects.create(contacto=contacto, **telefono_data )
        return contacto

    def update(self, instance, validated_data):
        telefonos_data = validated_data.pop('telefonos')
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Actualizar teléfonos
        instance.telefonos.all().delete()
        for telefono_data in telefonos_data:
            Telefono.objects.create(contacto=instance, **telefono_data)
        
        return instance
