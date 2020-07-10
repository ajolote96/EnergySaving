from experta import *
from .models import Registro

class Producto(Fact):
    pass

class Cupon(Fact):
    pass

class Promo(Fact):
    pass

class Ofertas(KnowledgeEngine):

    @DefFacts()
    def carga_promociones_pack(self):
        """Genera las promociones vigentes"""
        yield Promo(tipo="PACK", producto1="Fregona ACME", producto2="Mopa ACME", descuento="25%")
        yield Promo(tipo="PACK", producto1="Pasta Gallo", producto2="Tomate Frito", descuento="10%")

    @Rule(Promo(tipo="PACK", producto1=MATCH.p1, producto2=MATCH.p2, descuento=MATCH.d),
          OR(
              AND(
                  NOT(Producto(nombre=MATCH.p1)),
                  Producto(nombre=MATCH.p2)
              ),
              AND(
                  Producto(nombre=MATCH.p1),
                  NOT(Producto(nombre=MATCH.p2))
              )
          )
    )
    def pack(self, p1, p2, d):
        """
        El cliente querrá comprar un producto adicional en su próxima visita.
        """
        Registro.objects.create(title="Cupon", message=d)
        self.declare(Cupon(tipo="PACK", producto1=p1, producto2=p2, descuento=d))