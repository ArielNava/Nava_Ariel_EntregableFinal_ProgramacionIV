from django import forms
from.models import Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo','nombre','descripcion','categoria','precio','cantidad_existente','stock_minimo','estado']
        widgets = {
            'codigo': forms.TextInput(attrs={'class':'input','placeholder':'Ej: P001'}),
            'nombre': forms.TextInput(attrs={'class':'input'}),
            'descripcion': forms.Textarea(attrs={'class':'input','rows':3}),
            'categoria': forms.Select(attrs={'class':'input'}),
            'precio': forms.NumberInput(attrs={'class':'input','min':0,'step':'0.01'}),
            'cantidad_existente': forms.NumberInput(attrs={'class':'input','min':0}),
            'stock_minimo': forms.NumberInput(attrs={'class':'input','min':0}),
            'estado': forms.CheckboxInput(attrs={'style':'width:18px;height:18px'}),
        }
