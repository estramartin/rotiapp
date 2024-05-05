from django.test import TestCase
from .models import EmpleadoCategoria, Empleado, Categoria
from apps.core.models import DocTipo


class EmpleadoCategoriaTest(TestCase):
    def setUp(self):
        doctipo = DocTipo.objects.create(descripcion='DNI', sigla='DNI')
        self.categoria = Categoria.objects.create(nombre='Bachero', descripcion='lava plancha', valor_hora=1000, valor_antiguedad=2000, aportes=19)
        self.empleado = Empleado.objects.create(
                                            nombre='Juan',
                                            apellido='Perez',
                                            nro_doc='32831554',
                                            fec_nac='1987-02-21',
                                            tipo_doc=doctipo,
                                            fecha_ingreso='2020-02-02',
                                            activo=True
                                            )
        self.empleado_categoria = EmpleadoCategoria.objects.create(empleado=self.empleado, categoria=self.categoria)

    def test_antiguedad(self):
        self.assertEqual(self.empleado_categoria.antiguedad, 4)
  
    def test_valor_antiguedad(self):
        self.assertEqual(self.empleado_categoria.valor_antiguedad, 8000)

    def test_valor_total_mensual(self):
        self.assertEqual(self.empleado_categoria.valor_total_mensual(200), 168480)
    
    def test_diario_minutos_sin_antiguedad(self):
        self.assertEqual(self.empleado_categoria.diario_minutos_sin_antiguedad(300), 5000.0)

    def test_valor_total_semanal(self):
        self.assertEqual(self.empleado_categoria.valor_total_semanal(44), 37260.0)
