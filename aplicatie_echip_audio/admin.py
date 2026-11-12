import csv
from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
from .models import Brand, Subcategorie, Categorie, ServiciuAditional, Produs, VariantaCuloare, ArticolBlog

admin.site.site_header = "Panou de Administrare"
admin.site.site_title = "Admin"
admin.site.site_url = "/"
admin.site.index_title = "Bine ai venit!"

class VariantaCuloareInline(admin.TabularInline):
    model = VariantaCuloare
    extra = 1
    
class SubcategorieInline(admin.TabularInline):
    model = Subcategorie
    extra = 1

class BrandAdmin(admin.ModelAdmin):
    search_fields = ("nume", "=site_web")
    search_help_text = "Caută în funcție de nume sau întrega adresă către site-ul web"
    
class SubcategorieAdmin(admin.ModelAdmin):
    search_fields = ("nume", "descriere")
    search_help_text = "Caută în funcție de nume sau cuvinte din descriere"
    
class CategorieAdmin(admin.ModelAdmin):
    search_fields = ("nume", "descriere")
    search_help_text = "Caută în funcție de nume sau cuvinte din descriere"
    inlines = [SubcategorieInline]
    
class ServiciuAditionalAdmin(admin.ModelAdmin):
    search_fields = ("nume", "descriere")
    search_help_text = "Caută în funcție de nume sau cuvinte din descriere"

class ProdusAdmin(admin.ModelAdmin):
    @admin.display(
        description = "reducere",
        ordering = "reducere"
    )
    def are_reducere(self, obj):
        if obj.reducere == 0:
            return format_html("<i>Nu are reducere</i>", None)
        return format_html("<b>{}%</b>", obj.reducere)
    
    @admin.action(description="Exportă toate atributele produselor selectate")
    def export_produse(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="produse.csv"'
        writer = csv.writer(response)
        writer.writerow(["Model", "Preț", "Reducere", "În showroom", "Dată adăugare", "Specificații tehnice"])
        for produs in queryset:
            writer.writerow([
                produs.model,
                produs.pret,
                produs.reducere,
                produs.in_showroom,
                produs.data_adaugare,
                produs.specificatii_tehnice
            ])
        return response
    
    @admin.action(description="Exportă prețurile produselor selectate")
    def export_preturi(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="preturi.csv"'
        writer = csv.writer(response)
        writer.writerow(["Model", "Preț", "Reducere"])
        for produs in queryset:
            writer.writerow([
                produs.model,
                produs.pret,
                produs.reducere
            ])
        return response

    fieldsets = (
        ("Caracteristici obligatorii", {
            "fields": ("subcategorie", "brand", "model", "pret")
        }),
        ("Caracteristici suplimentare", {
            "fields": ("reducere", "in_showroom", "specificatii_tehnice", "servicii", "descriere"),
            "classes": ("collapse",)
        })
    )
    actions = ["export_produse", "export_preturi"]
    list_display = ("brand", "model", "are_reducere")
    list_per_page = 5
    list_filter = ("subcategorie__categorie", "subcategorie", "brand", "in_showroom", "servicii", "data_adaugare")
    search_fields = ("model", "brand__nume")
    search_help_text = ("Caută în funcție de brand sau model")
    ordering = ("brand", "model",)
    empty_value_display = "[NULL]"
    inlines = [VariantaCuloareInline]
    
class VariantaCuloareAdmin(admin.ModelAdmin):
    search_fields = ("nume", "produs__model", "produs__brand__nume")
    search_help_text = "Caută în funcție de numele culorii, modelul sau brandul produsului"
    
class ArticolBlogAdmin(admin.ModelAdmin):
    search_fields = ("titlu", "continut")
    search_help_text = "Caută în funcție de titlu sau cuvinte din conținut"

admin.site.register(Brand, BrandAdmin)
admin.site.register(Subcategorie, SubcategorieAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(ServiciuAditional, ServiciuAditionalAdmin)
admin.site.register(Produs, ProdusAdmin)
admin.site.register(VariantaCuloare, VariantaCuloareAdmin)
admin.site.register(ArticolBlog, ArticolBlogAdmin)