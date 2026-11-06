from django.contrib import admin
from .models import Brand
from .models import Categorie
from .models import ServiciuAditional
from .models import Produs
from .models import VariantaCuloare
from .models import ArticolBlog

admin.site.register(Brand)
admin.site.register(Categorie)
admin.site.register(ServiciuAditional)
admin.site.register(Produs)
admin.site.register(VariantaCuloare)
admin.site.register(ArticolBlog)