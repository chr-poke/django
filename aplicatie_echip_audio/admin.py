from django.contrib import admin
from .models import Brand, Subcategorie, Categorie, ServiciuAditional, Produs, VariantaCuloare, ArticolBlog

admin.site.register([Brand, Subcategorie, Categorie, ServiciuAditional, Produs, VariantaCuloare, ArticolBlog])