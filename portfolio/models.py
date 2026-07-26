from django.db import models
import cloudinary.models


class GeneralSetting(models.Model):
    # ── 1. SEO & Identidade da Marca ──
    site_title = models.CharField(
        max_length=120, 
        default="Fredy Segunda — Direção Criativa & Design Gráfico", 
        verbose_name="Título da Página (Browser & SEO)"
    )
    meta_description = models.TextField(
        default="Especializado em identidade visual e ilustração digital. Crio sistemas de marca com carácter — do conceito ao detalhe final.", 
        verbose_name="Descrição SEO para Google e Partilhas"
    )

    # ── 2. Status de Agenda & Disponibilidade ──
    is_available = models.BooleanField(
        default=True, 
        verbose_name="Atualmente disponível para Freelance/Novos Projetos?",
        help_text="Se ativo, exibe o indicador luminoso VERDE. Se desativar, exibe indicador de 'Agenda Ocupada' / em projeto."
    )
    availability_badge_text = models.CharField(
        max_length=120, 
        default="Disponível para Projetos Freelance & Colaborações", 
        verbose_name="Texto do Badge de Disponibilidade (Hero)"
    )
    hero_year = models.CharField(max_length=10, default="2026", verbose_name="Ano em Destaque (Hero/Footer)")
    
    # ── 3. Apresentação Principal (Hero) ──
    hero_title = models.TextField(
        default="Marcas que<br><span class=\"blue\">ficam</span><br>na memória.", 
        verbose_name="Título Principal do Hero (suporta HTML)"
    )
    hero_desc = models.TextField(
        default="Especializado em identidade visual e ilustração digital. Crio sistemas de marca com carácter — do conceito estético ao detalhe de acabamento final.", 
        verbose_name="Descrição Narrativa do Hero"
    )
    cv_file = cloudinary.models.CloudinaryField(
        'Ficheiro do Currículo (PDF/Asset)',
        blank=True,
        null=True,
        resource_type='raw',
        help_text="Ficheiro disponibilizado para download no botão 'Transferir Currículo'"
    )
    
    # ── 4. Estatísticas de Impacto (Stats) ──
    stat1_number = models.CharField(max_length=10, default="34+", verbose_name="Nº Estatística 1")
    stat1_label = models.CharField(max_length=35, default="Projetos Concluídos", verbose_name="Rótulo Estatística 1")
    stat2_number = models.CharField(max_length=10, default="3", verbose_name="Nº Estatística 2")
    stat2_label = models.CharField(max_length=35, default="Anos Experiência", verbose_name="Rótulo Estatística 2")
    stat3_number = models.CharField(max_length=10, default="18", verbose_name="Nº Estatística 3")
    stat3_label = models.CharField(max_length=35, default="Clientes Atendidos", verbose_name="Rótulo Estatística 3")

    # ── 5. Canais de Contacto & Redes Sociais ──
    contact_email = models.EmailField(default="fredy.segunda@email.com", verbose_name="Email Principal de Contacto")
    whatsapp_number = models.CharField(
        max_length=25, 
        blank=True, 
        null=True, 
        verbose_name="Número do WhatsApp",
        help_text="Formato internacional com código do país. Ex: +351912345678 (permite conversa direta)"
    )
    link_behance = models.URLField(blank=True, null=True, default="#", verbose_name="Link Behance (Essencial para Design)")
    link_dribbble = models.URLField(blank=True, null=True, default="#", verbose_name="Link Dribbble")
    link_instagram = models.URLField(blank=True, null=True, default="#", verbose_name="Link Instagram")
    link_linkedin = models.URLField(blank=True, null=True, default="#", verbose_name="Link LinkedIn")
    link_github = models.URLField(blank=True, null=True, verbose_name="Link GitHub / Outro Portfólio")
    
    # ── 6. Personalização do Bloco de Conversão (CTA Final) ──
    cta_title = models.CharField(
        max_length=150, 
        default="Pronto para dar vida ao seu próximo projeto?", 
        verbose_name="Título do Bloco de Contacto"
    )
    cta_subtitle = models.TextField(
        default="Estou atualmente disponível para projetos freelance, novas marcas e parcerias criativas que valorizem design memorável e detalhista.", 
        verbose_name="Subtítulo / Convite de Contacto"
    )
    
    class Meta:
        verbose_name = "Configuração Geral & Identidade"
        verbose_name_plural = "1. Configurações Gerais do Site"

    def __str__(self):
        return "Configurações Globais — Fredy Segunda Studio"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(GeneralSetting, self).save(*args, **kwargs)


class Tool(models.Model):
    name = models.CharField(max_length=60, verbose_name="Ferramenta / Competência", help_text="Ex: Adobe Illustrator, Branding, Cinema 4D")
    percentage = models.PositiveIntegerField(verbose_name="Nível de Domínio (0 a 100%)", default=90)
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição", help_text="Menor número aparece primeiro")

    class Meta:
        ordering = ['order']
        verbose_name = "Ferramenta / Competência"
        verbose_name_plural = "3. Stack de Ferramentas"

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class CreativeStep(models.Model):
    step_number = models.CharField(max_length=10, verbose_name="Número do Passo", help_text="Ex: 01, 02, 03")
    title = models.CharField(max_length=100, verbose_name="Título da Etapa")
    description = models.TextField(verbose_name="Descrição Metodológica")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")

    class Meta:
        ordering = ['order']
        verbose_name = "Etapa de Trabalho"
        verbose_name_plural = "4. Processo Criativo"

    def __str__(self):
        return f"Etapa {self.step_number} — {self.title}"


class Project(models.Model):
    SECTION_CHOICES = [
        ('featured_main', '★ Destaque Principal (Showcase Amplo)'),
        ('featured_side', '■ Destaques Secundários (2 Cards)'),
        ('gallery_small', '❖ Galeria de Criações (Grid 3 Colunas)'),
        ('gallery_asym', '◆ Galeria Assimétrica (Conceitos/Assinatura)'),
        ('reel', '🎬 Clip de Animação / Vídeo Reel'),
    ]

    title = models.CharField(max_length=120, verbose_name="Título do Trabalho", blank=True, null=True, help_text="Nome da marca, projeto ou ilustração")
    category = models.CharField(max_length=60, verbose_name="Categoria / Serviço", blank=True, null=True, help_text="Ex: Identidade Visual, Motion Design, Packaging")
    description = models.TextField(verbose_name="Descrição Narrativa & Desafio", blank=True, null=True, help_text="Texto sempre visível nas novas cards editoriais")
    
    # Metadados de alto nível para clientes
    client_name = models.CharField(max_length=100, verbose_name="Marca / Cliente", blank=True, null=True, help_text="Ex: Nike, Estúdio Beta, Projeto Conceitual")
    project_year = models.CharField(max_length=10, verbose_name="Ano", blank=True, null=True, default="2026")
    project_url = models.URLField(verbose_name="Link do Projeto (Behance / Site Real)", blank=True, null=True, help_text="Permite que o utilizador aceda ao estudo de caso ao vivo")
    featured_tag = models.CharField(max_length=50, verbose_name="Tag de Destaque", blank=True, null=True, help_text="Ex: Premiado, Em Destaque, Rebrand 2026")
    
    section = models.CharField(max_length=25, choices=SECTION_CHOICES, verbose_name="Secção no Site", default='gallery_small')
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem na Secção", help_text="Define qual aparece primeiro na grelha")
    
    media_file = cloudinary.models.CloudinaryField(
        'Asset (Imagem ou Vídeo MP4)',
        resource_type='auto'
    )
    is_video = models.BooleanField(default=False, verbose_name="O ficheiro é um vídeo MP4/Loop?", help_text="Se ativo, reproduz automaticamente em mute na card e com som no Lightbox")

    class Meta:
        ordering = ['section', 'order']
        verbose_name = "Projeto do Portfólio"
        verbose_name_plural = "2. Gestão de Projetos & Obras"

    def __str__(self):
        return f"[{self.get_section_display().split()[1]}] {self.title or 'Projeto Sem Título'}"
