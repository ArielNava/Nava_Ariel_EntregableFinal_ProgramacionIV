from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, ConsultaIA
import requests
from django.db.models import F, Q
import random
from datetime import datetime

def generar_codigo(categoria=""):
    pref="PC"; c=categoria.lower()
    if "acces" in c: pref="ACC"
    elif "cable" in c: pref="CAB"
    elif "mouse" in c or "teclad" in c or "hub" in c or "audif" in c: pref="PER"
    elif "laptop" in c or "lap" in c: pref="LAP"
    return f"{pref}{random.randint(100,999)}"

def armar_carrito(request):
    carrito=request.session.get('carrito',{}); items=[]; total=0
    for pid,cant in carrito.items():
        try:
            p=Producto.objects.get(id=int(pid)); sub=p.precio*cant; total+=sub
            items.append({'producto':p,'cantidad':cant,'subtotal':sub})
        except: pass
    count=sum(carrito.values()) if carrito else 0
    return items,total,count

def inventario(request):
    q=request.GET.get('q','').strip()
    productos=Producto.objects.all().order_by('-id')
    if q: productos=productos.filter(Q(nombre__icontains=q) | Q(codigo__icontains=q) | Q(categoria__icontains=q) | Q(descripcion__icontains=q))
    total_valor=sum([p.precio * p.cantidad_existente for p in productos])
    _,_,carrito_count=armar_carrito(request)
    return render(request,'productos/inventario.html',{'productos':productos,'total_valor':total_valor,'carrito_count':carrito_count,'q':q,'total_resultados':productos.count()})

def agregar_producto(request):
    if request.method=='POST':
        Producto.objects.create(nombre=request.POST.get('nombre'),codigo=(request.POST.get('codigo') or generar_codigo(request.POST.get('categoria',''))).upper(),categoria=request.POST.get('categoria','computadora'),precio=float(request.POST.get('precio',0)),cantidad_existente=int(request.POST.get('cantidad_existente',0)),stock_minimo=int(request.POST.get('stock_minimo',3)),descripcion=request.POST.get('descripcion',''))
        return redirect('/')
    return render(request,'productos/producto_form.html',{'accion':'Agregar','codigo_default':generar_codigo()})

def editar_producto(request,pk):
    p=get_object_or_404(Producto,id=pk)
    if request.method=='POST':
        p.nombre=request.POST.get('nombre'); p.codigo=request.POST.get('codigo'); p.categoria=request.POST.get('categoria'); p.precio=float(request.POST.get('precio',0)); p.cantidad_existente=int(request.POST.get('cantidad_existente',0)); p.stock_minimo=int(request.POST.get('stock_minimo',3)); p.descripcion=request.POST.get('descripcion',''); p.save()
        return redirect('/')
    return render(request,'productos/producto_form.html',{'accion':'Editar','producto':p})

def eliminar_producto(request,pk): get_object_or_404(Producto,id=pk).delete(); return redirect('/')

def tienda(request):
    q=request.GET.get('q','').strip()
    cat=request.GET.get('cat','').strip()
    productos=Producto.objects.all().order_by('nombre')
    if q: productos=productos.filter(Q(nombre__icontains=q) | Q(codigo__icontains=q) | Q(descripcion__icontains=q))
    if cat: productos=productos.filter(categoria=cat)
    categorias=Producto.objects.values_list('categoria',flat=True).distinct().order_by('categoria')
    _,_,count=armar_carrito(request)
    return render(request,'productos/tienda.html',{'productos':productos,'categorias':categorias,'carrito_count':count,'q':q,'cat_actual':cat,'total_resultados':productos.count()})

def agregar_carrito(request,producto_id):
    producto=get_object_or_404(Producto,id=producto_id)
    if producto.cantidad_existente>0:
        producto.cantidad_existente-=1; producto.save()
        carrito=request.session.get('carrito',{}); carrito[str(producto_id)]=carrito.get(str(producto_id),0)+1
        request.session['carrito']=carrito; request.session.modified=True
    return redirect(request.META.get('HTTP_REFERER','/tienda/'))

def quitar_carrito(request,producto_id):
    carrito=request.session.get('carrito',{}); cant=carrito.get(str(producto_id),0)
    if cant>0:
        try: pr=Producto.objects.get(id=int(producto_id)); pr.cantidad_existente+=cant; pr.save()
        except: pass
        carrito.pop(str(producto_id),None); request.session['carrito']=carrito; request.session.modified=True
    return redirect('/carrito/')

def vaciar_carrito(request):
    carrito=request.session.get('carrito',{})
    for pid,cant in carrito.items():
        try: pr=Producto.objects.get(id=int(pid)); pr.cantidad_existente+=cant; pr.save()
        except: pass
    request.session['carrito']={}; request.session.modified=True; return redirect('/carrito/')

def ver_carrito(request):
    items,total,count=armar_carrito(request)
    return render(request,'productos/carrito.html',{'items':items,'total':total,'count':count,'carrito_count':count})

def finalizar_compra(request):
    items,total,count=armar_carrito(request)
    if count==0: return redirect('/carrito/')
    if request.method=='POST':
        request.session['ultima_factura']={'nombre':request.POST.get('nombre'),'ci':request.POST.get('ci'),'telefono':request.POST.get('telefono'),'direccion':request.POST.get('direccion'),'num':random.randint(10000,99999),'fecha':datetime.now().strftime("%d/%m/%Y %H:%M"),'total':float(total),'count':count,'items':[{'nombre':i['producto'].nombre,'codigo':i['producto'].codigo,'precio':float(i['producto'].precio),'cantidad':i['cantidad'],'subtotal':float(i['subtotal'])} for i in items]}
        request.session['carrito']={}; request.session.modified=True; return redirect('/factura/')
    return render(request,'productos/checkout.html',{'items':items,'total':total,'count':count,'carrito_count':count})

def factura_view(request):
    f=request.session.get('ultima_factura')
    if not f: return redirect('/')
    return render(request,'productos/factura.html',{'f':f,'carrito_count':0})

def chat_ia(request):
    respuesta=None; pregunta=""; historial=ConsultaIA.objects.order_by('-fecha')[:20]
    _,_,count=armar_carrito(request)
    if request.method=='POST':
        pregunta=request.POST.get('pregunta','').strip()
        if pregunta:
            productos=list(Producto.objects.values('codigo','nombre','categoria','precio','cantidad_existente','stock_minimo','descripcion')[:80])
            prompt=f"Eres asistente Tecno Center. INVENTARIO: {productos} PREGUNTA: {pregunta} Responde max 4 lineas."
            try:
                r=requests.post("http://127.0.0.1:11434/api/generate",json={"model":"qwen2.5:1.5b","prompt":prompt,"stream":False},timeout=120)
                respuesta=r.json().get('response','Sin respuesta') if r.status_code==200 else f"Error {r.status_code}"
            except Exception as e: respuesta=f"ERROR: {e}"
            ConsultaIA.objects.create(pregunta=pregunta,respuesta=respuesta)
    return render(request,'productos/chat_ia.html',{'respuesta':respuesta,'pregunta':pregunta,'historial':historial,'carrito_count':count})

def reporte_ollama(request):
    productos=Producto.objects.all().order_by('-cantidad_existente')
    total=sum([p.precio * p.cantidad_existente for p in productos])
    bajo=productos.filter(cantidad_existente__lt=F('stock_minimo'))
    _,_,count=armar_carrito(request)
    return render(request,'productos/reporte_ollama.html',{'productos':productos,'total':total,'bajo':bajo,'total_productos':productos.count(),'total_unidades':sum([p.cantidad_existente for p in productos]),'categorias':productos.values('categoria').distinct().count(),'carrito_count':count})
