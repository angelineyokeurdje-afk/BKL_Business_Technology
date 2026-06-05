from django.db import models


class Product(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    image       = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'


class SiteSettings(models.Model):
    """Paramètres du site gérés depuis l'admin."""

    hero_image = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name="Image d'accueil"
    )
    hero_titre = models.CharField(
        max_length=200,
        default="Bienvenue sur BKLbusiness",
        verbose_name="Titre d'accueil"
    )
    hero_description = models.TextField(
        default="Découvrez notre catalogue de produits et services.",
        verbose_name="Description d'accueil"
    )

    def __str__(self):
        return "Paramètres du site"

    class Meta:
        verbose_name = "Paramètres du site"