import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from productos.models import Producto
Producto.objects.all().delete()
for c,n,cat,pre,cant in [("PC001","Laptop HP i7","computadoras",4500,5),("PC002","PC Gamer RTX 4060","computadoras",7200,2),("MON001","Monitor 24 144Hz","perifericos",1200,0),("TEC001","Teclado Mecanico RGB","perifericos",350,3),("MOU001","Mouse G502","perifericos",280,1),("RAM001","RAM 16GB DDR4","componentes",550,4),("SSD001","SSD 1TB NVMe","componentes",680,10)]:
    Producto.objects.create(codigo=c,nombre=n,categoria=cat,precio=pre,cantidad_existente=cant,stock_minimo=3)
print("Datos cargados")
