from django.test import TestCase
from cenas.models import Evento

class EventoTestCase(TestCase):
  def setUp(self):
    Evento.objects.create(tituloEvento="Evento de prueba", fechaEvento="1970-01-01", activo=True)

  def test_evento_creado(self):
    evento = Evento.objects.get(tituloEvento="Evento de prueba")
    self.assertEqual(getattr(evento, "activo"), True)
