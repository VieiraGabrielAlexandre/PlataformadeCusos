from django.db import models
from django.conf import settings


class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )


class Course(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descricao Simples', blank=True)
    about = models.TextField('Sobre o Curso', blank=True)
    start_date = models.DateField(
        'Data de Inicio', null=True, blank=True
    )
    image = models.ImageField(
        upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('courses:details', (), {'slug': self.slug})

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']


class Enrollment(models.Model):

    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuario',
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, verbose_name='Curso', related_name='enrollments'
    )
    status = models.IntegerField(
        'Situacao', choices=STATUS_CHOICES, default=1, blank=True
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    class Meta:
        verbose_name = 'Inscricao'
        verbose_name_plural = 'Inscricoes'
        unique_together = (('user', 'course'),)