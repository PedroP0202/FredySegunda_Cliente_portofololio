from django.contrib import admin
from django.utils.html import format_html
from .models import Project, GeneralSetting, Tool, CreativeStep

@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("🌐 1. Identidade do Site & SEO", {
            "fields": ("site_title", "meta_description"),
            "description": "Configurações que aparecem na aba do navegador e nos motores de busca (Google)."
        }),
        ("🟢 2. Status de Agenda & Disponibilidade", {
            "fields": ("is_available", "availability_badge_text", "hero_year"),
            "description": "Controle o indicador verde/vermelho que mostra aos clientes se tem agenda aberta para novos trabalhos."
        }),
        ("📢 3. Secção Principal (Hero Showcase)", {
            "fields": ("hero_title", "hero_desc", "cv_file"),
            "description": "A frase de impacto inicial, a descrição introdutória e o ficheiro de currículo para download."
        }),
        ("📊 4. Estatísticas de Impacto", {
            "fields": (("stat1_number", "stat1_label"), ("stat2_number", "stat2_label"), ("stat3_number", "stat3_label")),
            "description": "Números de destaque exibidos em cartões vidro por baixo do botão principal."
        }),
        ("💬 5. Canais de Contacto & Redes Sociais", {
            "fields": ("contact_email", "whatsapp_number", "link_behance", "link_dribbble", "link_instagram", "link_linkedin", "link_github"),
            "description": "As redes e contactos que aparecerão nos botões, rodapé e convites do site."
        }),
        ("✉️ 6. Personalização do Convite Final (CTA & Contacto)", {
            "fields": ("cta_title", "cta_subtitle"),
            "description": "A mensagem de chamada de atenção antes de encerrar o portfólio."
        }),
    )

    def has_add_permission(self, request):
        if GeneralSetting.objects.exists():
            return False
        return True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('media_preview', 'title', 'category', 'section', 'client_name', 'project_year', 'order', 'is_video')
    list_editable = ('section', 'category', 'order', 'is_video')
    list_filter = ('section', 'is_video', 'project_year')
    search_fields = ('title', 'category', 'description', 'client_name')
    ordering = ('section', 'order')
    list_per_page = 20
    
    fieldsets = (
        ("📁 1. Asset & Media (Imagem ou Vídeo)", {
            "fields": ("media_file", "is_video", "section", "order"),
            "description": "Escolha o ficheiro no Cloudinary e onde ele irá aparecer no site (Destaque, Galeria 3 colunas, Assimétrico ou Reel)."
        }),
        ("✍️ 2. Editorial & Narrativa (Sempre Visível nas Cards)", {
            "fields": ("title", "category", "description"),
            "description": "Textos organizados por baixo ou ao lado de cada projeto para dar contexto profissional e autoridade ao trabalho."
        }),
        ("🏷️ 3. Metadados do Cliente & Links", {
            "fields": ("client_name", "project_year", "featured_tag", "project_url"),
            "classes": ("collapse",),
            "description": "Informações opcionais (nome da marca atendida, ano de entrega e link para o estudo de caso no Behance)."
        }),
    )

    def media_preview(self, obj):
        if not obj.media_file:
            return format_html('<span style="color: #888; font-style: italic;">Sem Media</span>')
        try:
            url = obj.media_file.url
            if obj.is_video:
                return format_html(
                    '<div class="thumb-preview"><video src="{}" style="width:75px; height:52px; object-fit:cover; border-radius:6px; background:#000;" autoplay muted loop playsinline></video></div>',
                    url
                )
            return format_html(
                '<div class="thumb-preview"><img src="{}" style="width:75px; height:52px; object-fit:cover; border-radius:6px; box-shadow: 0 2px 8px rgba(0,0,0,0.5);" /></div>',
                url
            )
        except Exception:
            return format_html('<span style="color: #e53e3e;">Erro URL</span>')

    media_preview.short_description = "Miniatura"


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage_progress', 'percentage', 'order')
    list_editable = ('percentage', 'order')
    ordering = ('order',)
    
    def percentage_progress(self, obj):
        return format_html(
            '<div style="background: rgba(255,255,255,0.08); border-radius: 20px; width: 120px; height: 10px; overflow: hidden; display: inline-block; vertical-align: middle;">'
            '<div style="background: #4C75EE; width: {}%; height: 100%; border-radius: 20px;"></div>'
            '</div>',
            obj.percentage
        )
    percentage_progress.short_description = "Nível Gráfico"


@admin.register(CreativeStep)
class CreativeStepAdmin(admin.ModelAdmin):
    list_display = ('step_badge', 'title', 'order')
    list_editable = ('title', 'order')
    ordering = ('order',)
    
    def step_badge(self, obj):
        return format_html(
            '<span style="background: #4C75EE; color: #fff; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-family: sans-serif;">{}</span>',
            obj.step_number
        )
    step_badge.short_description = "Passo Nº"
