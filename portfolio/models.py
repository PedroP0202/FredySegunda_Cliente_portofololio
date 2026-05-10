from django.db import models

class GeneralSetting(models.Model):
    # Hero Section
    hero_year = models.CharField(max_length=10, default="2025", verbose_name="Ano no Hero")
    hero_title = models.TextField(default="Marcas que<br><span class=\"blue\">ficam</span><br>na memória.", verbose_name="Título (suporta HTML)")
    hero_desc = models.TextField(default="Especializado em identidade visual e ilustração digital. Crio sistemas de marca com carácter — do conceito ao detalhe final.", verbose_name="Descrição do Hero")
    
    # Stats
    stat1_number = models.CharField(max_length=10, default="34+", verbose_name="Nº Estatística 1")
    stat1_label = models.CharField(max_length=30, default="Projetos", verbose_name="Label Estatística 1")
    stat2_number = models.CharField(max_length=10, default="3", verbose_name="Nº Estatística 2")
    stat2_label = models.CharField(max_length=30, default="Anos exp.", verbose_name="Label Estatística 2")
    stat3_number = models.CharField(max_length=10, default="18", verbose_name="Nº Estatística 3")
    stat3_label = models.CharField(max_length=30, default="Clientes", verbose_name="Label Estatística 3")

    # Footer/Contact
    contact_email = models.EmailField(default="fredy.segunda@email.com", verbose_name="Email de Contacto")
    link_instagram = models.URLField(blank=True, null=True, default="#", verbose_name="Link Instagram")
    link_linkedin = models.URLField(blank=True, null=True, default="#", verbose_name="Link LinkedIn")
    cv_file = models.FileField(upload_to='cv_files/', blank=True, null=True, verbose_name="Ficheiro do CV (PDF)")

    class Meta:
        verbose_name = "Configuração Geral"
        verbose_name_plural = "Configurações Gerais"

    def __str__(self):
        return "Configurações do Portefólio"

    def save(self, *args, **kwargs):
        # Enforce singleton
        self.pk = 1
        super(GeneralSetting, self).save(*args, **kwargs)

class Tool(models.Model):
    name = models.CharField(max_length=50, verbose_name="Ferramenta")
    percentage = models.PositiveIntegerField(verbose_name="Percentagem (0-100)", default=80)
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")

    class Meta:
        ordering = ['order']
        verbose_name = "Ferramenta"
        verbose_name_plural = "Ferramentas"

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class CreativeStep(models.Model):
    step_number = models.CharField(max_length=10, verbose_name="Número do Passo", help_text="Ex: 01, 02")
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")

    class Meta:
        ordering = ['order']
        verbose_name = "Passo do Processo"
        verbose_name_plural = "Processo Criativo"

    def __str__(self):
        return f"{self.step_number} - {self.title}"

class Project(models.Model):
    SECTION_CHOICES = [
        ('featured_main', 'Destaque Principal (Alto)'),
        ('featured_side', 'Destaque Secundário (Médio)'),
        ('gallery_small', 'Galeria (Grade 3)'),
        ('gallery_asym', 'Galeria (Assimétrico)'),
        ('reel', 'Reel Clip'),
    ]

    title = models.CharField(max_length=100, verbose_name="Título", blank=True, null=True)
    category = models.CharField(max_length=50, verbose_name="Categoria/Tipo", blank=True, null=True)
    description = models.TextField(verbose_name="Descrição", blank=True, null=True)
    
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, verbose_name="Secção no Site")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")
    
    media_file = models.FileField(upload_to='projects_media/', verbose_name="Ficheiro (Imagem/Vídeo)")
    is_video = models.BooleanField(default=False, verbose_name="É vídeo?")

    class Meta:
        ordering = ['order']
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return self.title if self.title else f"Projeto em {self.get_section_display()}"
