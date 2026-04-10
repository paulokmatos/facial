from django.db import models


class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    foto = models.ImageField(upload_to='fotos/')
    face_label = models.IntegerField(unique=True, editable=False)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.pk and self.face_label is None:
            ultimo = Pessoa.objects.order_by('-face_label').first()
            self.face_label = (ultimo.face_label + 1) if ultimo else 1
        super().save(*args, **kwargs)
