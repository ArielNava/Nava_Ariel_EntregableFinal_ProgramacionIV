def carrito_context(request):
    carrito = request.session.get('carrito', {})
    total = sum(carrito.values()) if carrito else 0
    return {'carrito_cantidad': total}
