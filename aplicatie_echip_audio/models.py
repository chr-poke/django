from django.db import models


class Brand(models.Model):
    class Meta:
        ordering = ["nume"]
        indexes = [
            models.Index(fields=["tara_origine"], name="index_tara_origine"),
        ]
        verbose_name_plural = "Branduri"
    
    nume = models.CharField(
        max_length=100,
        unique=True,
        error_messages={"unique": "Acest brand există deja în baza de date!"}
    )
    tara_origine = models.CharField(max_length=100)
    site_web = models.URLField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to="brand_logos/")

    def __str__(self):
        return self.nume


class Categorie(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(culoare__regex=r'^#[a-fA-F0-9]{6}$'),
                name="categorie_culoare_hex_valid",
                violation_error_message="Codul HEX este invalid!"
            )
        ]
        verbose_name_plural = "Categorii"

    class NivelExpertiza(models.TextChoices):
        INCEPATOR = "IN", "Începător"
        INTERMEDIAR = "IT", "Intermediar"
        AUDIOFIL = "AU", "Audiofil"

    nume = models.CharField(
        max_length=100,
        unique=True,
        error_messages={"unique": "Această categorie există deja în baza de date!"}
    )
    descriere = models.TextField(null=True, blank=True)
    culoare = models.CharField(
        max_length=7, 
        help_text="Cod HEX, ex: #FF0000",
        unique=True,
        error_messages={
            "max_length": "Codul HEX trebuie să aibă exact 7 caractere.",
            "unique": "Această culoare a fost folosită deja pentru altă categorie."
        }
    )
    sigla = models.ImageField(upload_to="categorii_sigle/")
    nivel_expertiza = models.CharField(
        max_length=2,
        choices=NivelExpertiza.choices,
        default=NivelExpertiza.INCEPATOR,
    )

    def __str__(self):
        return self.nume


class ServiciuAditional(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cost__gte=0.00),
                name="serviciu_cost_pozitiv",
                violation_error_message="Costul suplimentar al serviciului nu poate fi negativ!"
            )
        ]
        verbose_name_plural = "Servicii Aditionale"
    
    nume = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    descriere_serviciu = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nume


class Produs(models.Model):
    class Meta:
        ordering = ["-data_adaugare", "pret"]
        indexes = [
            models.Index(fields=["pret"], name="index_pret_produs"),
            models.Index(fields=["-data_adaugare"], name="index_data_adaugare_produs"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(pret__gte=0.00),
                name="produs_pret_pozitiv",
                violation_error_message="Prețul produsului trebuie să fie un număr pozitiv!"
            ),
            models.CheckConstraint(
                condition=models.Q(reducere__lte=100),
                name="produs_reducere_valid",
                violation_error_message="Procentul de reducere nu poate fi mai mare decăt 100!"
            )
        ]
        verbose_name_plural = "Produse"
    
    class TipConexiune(models.TextChoices):
        CABLU = "C", "Cablu"
        BLUETOOTH = "B", "Bluetooth"
        AMBELE = "A", "Ambele"

    model = models.CharField(max_length=150)
    pret = models.DecimalField(max_digits=12, decimal_places=2, help_text="Prețul de vânzare în RON")
    reducere = models.PositiveIntegerField(default=0, blank=True, help_text="Procent de reducere (0-100)")
    in_showroom = models.BooleanField(default=False, blank=True)
    data_adaugare = models.DateField(auto_now_add=True)
    tip_conexiune = models.CharField(
        max_length=1,
        choices=TipConexiune.choices,
        default=TipConexiune.CABLU,
    )
    specificatii_tehnice = models.JSONField(default=list, blank=True)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="produse")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="produse")
    servicii = models.ManyToManyField(ServiciuAditional, related_name="produse", blank=True)

    def __str__(self):
        return f"{self.brand.nume} {self.model}"


class VariantaCuloare(models.Model):
    class Meta:
        unique_together = (("produs", "culoare"))
        constraints = [
            models.CheckConstraint(
                condition=models.Q(culoare__regex=r'^#[a-fA-F0-9]{6}$'),
                name="varianta_culoare_hex_valid",
                violation_error_message="Codul HEX este invalid!"
            )
        ]
        indexes = [
            models.Index(fields=["stoc"], name="index_stoc_varianta_culoare"),
        ]
        verbose_name_plural = "Variante Culoare"
    
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name="variante_culoare")
    culoare = models.CharField(
        max_length=7, 
        help_text="Cod HEX, ex: #FF0000",
        error_messages={"max_length": "Codul HEX trebuie să aibă exact 7 caractere."}
    )
    nume_culoare = models.CharField(max_length=50)
    stoc = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.produs.model} - {self.nume_culoare}"


class ArticolBlog(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["titlu"], name="index_titlu_articol"),
        ]
        verbose_name_plural = "Articole Blog"
    
    titlu = models.CharField(
        max_length=100,
        unique=True,
        error_messages={"unique": "Există deja un articol cu același titlu în baza de date."}
    )
    continut = models.TextField()
    data_publicare = models.DateTimeField(auto_now_add=True)
    produse_mentionate = models.ManyToManyField(Produs, related_name="articole", blank=True)

    def __str__(self):
        return self.titlu