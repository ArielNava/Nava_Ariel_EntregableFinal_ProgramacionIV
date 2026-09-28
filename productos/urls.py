from django.urls import path
from . import views
urlpatterns=[
 path('',views.inventario,name='inventario'),
 path('agregar-producto/',views.agregar_producto,name='agregar_producto'),
 path('editar-producto/<int:pk>/',views.editar_producto,name='editar_producto'),
 path('eliminar-producto/<int:pk>/',views.eliminar_producto,name='eliminar_producto'),
 path('tienda/',views.tienda,name='tienda'),
 path('agregar/<int:producto_id>/',views.agregar_carrito,name='agregar_carrito'),
 path('quitar/<int:producto_id>/',views.quitar_carrito,name='quitar_carrito'),
 path('vaciar/',views.vaciar_carrito,name='vaciar_carrito'),
 path('carrito/',views.ver_carrito,name='ver_carrito'),
 path('finalizar/',views.finalizar_compra,name='finalizar_compra'),
 path('factura/',views.factura_view,name='factura'),
 path('chat/',views.chat_ia,name='chat_ia'),
 path('reportes/',views.reporte_ollama,name='reportes'),
 path('reporte/',views.reporte_ollama,name='reporte_ollama'),
]
