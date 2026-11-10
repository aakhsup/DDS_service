from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    # --- Поля модели (это данные, которые будут в таблице dds_category) ---
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.type.name})"

    class Meta:
        verbose_name = "Категория" # Как называть ОДНУ запись (в формах, заголовках)
        verbose_name_plural = "Категории" # Как называть МНОГО записей (заголовок списка)
        ordering = ['name'] # Правило: всегда сортировать по имени

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date}: {self.category.name} — {self.amount} ₽"
