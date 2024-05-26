from django.test import TestCase
from .models import Persona, DocTipo

class PersonaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        DocTipo.objects.create(tipo_doc_id=1, sigla='DNI', descripcion='documento')
        Persona.objects.create(nombre='John', apellido='Doe', tipo_doc=DocTipo.objects.get(pk=1), nro_doc='12345678')

    def test_nombre_label(self):
        persona = Persona.objects.get(id=1)
        field_label = persona._meta.get_field('nombre').verbose_name
        self.assertEqual(field_label, 'nombre')

    def test_apellido_label(self):
        persona = Persona.objects.get(id=1)
        field_label = persona._meta.get_field('apellido').verbose_name
        self.assertEqual(field_label, 'apellido')

    def test_nro_doc_label(self):
        persona = Persona.objects.get(id=1)
        field_label = persona._meta.get_field('nro_doc').verbose_name
        self.assertEqual(field_label, 'nro doc')

    def test_nombre_max_length(self):
        persona = Persona.objects.get(id=1)
        max_length = persona._meta.get_field('nombre').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_nombre_apellido(self):
        persona = Persona.objects.get(id=1)
        expected_object_name = f'{persona.nombre} {persona.apellido}'
        self.assertEqual(expected_object_name, str(persona))