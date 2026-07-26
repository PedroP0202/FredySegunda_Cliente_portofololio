from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Project, GeneralSetting, CustomGallery, Tool, CreativeStep


@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("🎨 Personalização de Fundo & Temas de Cor", {
            "fields": ("bg_theme", "custom_bg_color", "accent_color"),
            "description": "Escolha a atmosfera cromática e a cor de luz do seu estúdio em tempo real sem alterar código."
        }),
        ("Identidade da Marca & SEO", {
            "fields": ("site_title", "meta_description"),
            "description": "Configurações gerais para motores de busca (Google) e cabeçalho do separador."
        }),
        ("Status de Agenda & Disponibilidade", {
            "fields": ("is_available", "availability_badge_text", "hero_year"),
            "description": "Controle em tempo real se o indicador luminoso no topo e hero do site exibe agenda aberta."
        }),
        ("Apresentação Principal (Hero)", {
            "fields": ("hero_title", "hero_desc", "cv_file"),
            "description": "Textos de introdução e ficheiro para download do currículo no Hero."
        }),
        ("Estatísticas de Destaque", {
            "fields": (
                ("stat1_number", "stat1_label"),
                ("stat2_number", "stat2_label"),
                ("stat3_number", "stat3_label")
            ),
            "description": "Indicadores chave apresentados abaixo dos botões iniciais."
        }),
        ("🎯 Redes Sociais Estratégicas & Contactos Rápidos", {
            "fields": ("contact_email", "whatsapp_number", "link_behance", "link_dribbble", "link_instagram", "link_linkedin", "link_github"),
            "description": "Estes canais ganharam máxima visibilidade: aparecerão no Topo do Site, no Hero Inicial e numa Barra Flutuante de fácil acesso!"
        }),
        ("Bloco Final de Conversão (CTA)", {
            "fields": ("cta_title", "cta_subtitle"),
            "description": "Mensagem convidativa na área final do portfólio antes da despedida."
        }),
    )

    def has_add_permission(self, request):
        if GeneralSetting.objects.exists():
            return False
        return True


@admin.register(CustomGallery)
class CustomGalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag', 'layout_style_badge', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'tag', 'description')
    ordering = ('order',)
    
    fieldsets = (
        ("Configuração da Galeria", {
            "fields": ("name", "tag", "description", "layout_style", "order", "is_active"),
            "description": "Crie coleções temáticas exclusivas (ex: 'Projetos Identidade Visual 2026', 'Série de Ilustração Nike'). As galerias ativas surgem no menu e na página do site!"
        }),
    )

    def layout_style_badge(self, obj):
        color = '#10b981' if obj.layout_style == 'grid3' else '#8b5cf6'
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 10px; border-radius:6px; font-weight:600; font-size:0.8rem;">{}</span>',
            color, obj.get_layout_style_display().split(" (")[0]
        )
    layout_style_badge.short_description = "Estilo de Layout"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('media_preview_box', 'title_display', 'section_badge', 'gallery_assign_badge', 'category', 'client_name', 'order', 'is_video')
    list_editable = ('order', 'is_video')
    list_filter = ('custom_gallery', 'section', 'is_video', 'project_year', 'category')
    search_fields = ('title', 'category', 'description', 'client_name', 'featured_tag')
    ordering = ('section', 'order')
    list_per_page = 20

    actions = [
        'move_to_featured_main',
        'move_to_featured_side',
        'move_to_gallery_small',
        'move_to_gallery_asym',
        'move_to_reel',
        'toggle_video_status'
    ]
    
    fieldsets = (
        ("Ficheiro & Alocação Visual", {
            "fields": ("media_file", "is_video", "section", "custom_gallery", "order"),
            "description": "Selecione a obra no Cloudinary e escolha em que área geral ou em qual Galeria Customizada ela deve brilhar!"
        }),
        ("Conteúdo Editorial & Narrativa", {
            "fields": ("title", "category", "description"),
            "description": "Textos descritivos que acompanham o cartão editorial no site."
        }),
        ("Metadados & Ligações Externas", {
            "fields": ("client_name", "project_year", "featured_tag", "project_url"),
            "classes": ("collapse",),
            "description": "Informações de apoio (ano da obra, marca atendida e link no Behance)."
        }),
    )

    def title_display(self, obj):
        title = obj.title or "Obra sem título"
        tag = f' <span style="color:#60a5fa; font-size:0.75rem; margin-left:6px;">[{obj.featured_tag}]</span>' if obj.featured_tag else ""
        return format_html(f'<strong>{title}</strong>{tag}')
    title_display.short_description = "Título da Obra"

    def section_badge(self, obj):
        colors = {
            'featured_main': '#3b82f6',
            'featured_side': '#6366f1',
            'gallery_small': '#10b981',
            'gallery_asym': '#8b5cf6',
            'reel': '#f43f5e'
        }
        color = colors.get(obj.section, '#64748b')
        label = obj.get_section_display().split(' (')[0]
        return format_html(
            '<span style="border-left: 3px solid {}; padding-left: 8px; font-weight: 500;">{}</span>',
            color, label
        )
    section_badge.short_description = "Secção Padrão"

    def gallery_assign_badge(self, obj):
        if obj.custom_gallery and obj.custom_gallery.is_active:
            return format_html('<span style="color:#34d399; font-weight:700;">★ {}</span>', obj.custom_gallery.name)
        return format_html('<span style="color:#64748b; font-size:0.85rem;">— Normal —</span>')
    gallery_assign_badge.short_description = "Galeria Específica"

    def media_preview_box(self, obj):
        if not obj.media_file:
            return format_html('<span style="color: #64748b; font-style: italic;">Sem Media</span>')
        try:
            url = obj.media_file.url
            if obj.is_video:
                return format_html(
                    '<div class="studio-thumb">'
                    '<video src="{}#t=0.1" preload="metadata" style="width:100%; height:100%; object-fit:cover;"></video>'
                    '<span class="studio-thumb-badge" style="color:#f43f5e;">VIDEO</span>'
                    '</div>',
                    url
                )
            return format_html(
                '<div class="studio-thumb">'
                '<img src="{}" alt="Preview" loading="lazy" />'
                '<span class="studio-thumb-badge">IMG</span>'
                '</div>',
                url
            )
        except Exception:
            return format_html('<span style="color: #e53e3e;">Erro de Link</span>')
    media_preview_box.short_description = "Miniatura"

    # ── Bulk Executive Actions ──
    @admin.action(description="★ Mover selecionados para Showcase Principal")
    def move_to_featured_main(self, request, queryset):
        queryset.update(section='featured_main', custom_gallery=None)
        self.message_user(request, "Obras movidas para o Showcase Principal.", messages.SUCCESS)

    @admin.action(description="■ Mover selecionados para Destaques Secundários")
    def move_to_featured_side(self, request, queryset):
        queryset.update(section='featured_side', custom_gallery=None)
        self.message_user(request, "Obras movidas para Destaques Secundários.", messages.SUCCESS)

    @admin.action(description="❖ Mover selecionados para Galeria (3 Colunas)")
    def move_to_gallery_small(self, request, queryset):
        queryset.update(section='gallery_small', custom_gallery=None)
        self.message_user(request, "Obras transferidas para a Galeria de Criações.", messages.SUCCESS)

    @admin.action(description="◆ Mover selecionados para Galeria Assimétrica")
    def move_to_gallery_asym(self, request, queryset):
        queryset.update(section='gallery_asym', custom_gallery=None)
        self.message_user(request, "Obras atribuidas à Galeria Assimétrica.", messages.SUCCESS)

    @admin.action(description="🎬 Mover selecionados para Vídeo Reel")
    def move_to_reel(self, request, queryset):
        queryset.update(section='reel', is_video=True, custom_gallery=None)
        self.message_user(request, "Obras movidas e ativadas no Vídeo Reel.", messages.SUCCESS)

    @admin.action(description="🔄 Alternar Status de Vídeo / Imagem")
    def toggle_video_status(self, request, queryset):
        for obj in queryset:
            obj.is_video = not obj.is_video
            obj.save()
        self.message_user(request, "Status de vídeo invertido com sucesso.", messages.INFO)


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'progress_bar_view', 'percentage', 'order')
    list_editable = ('percentage', 'order')
    ordering = ('order',)
    
    def progress_bar_view(self, obj):
        return format_html(
            '<div style="background: rgba(255,255,255,0.06); border-radius: 6px; width: 140px; height: 8px; overflow: hidden; display: inline-block; vertical-align: middle;">'
            '<div style="background: #3b66f5; width: {}%; height: 100%; border-radius: 6px;"></div>'
            '</div>',
            obj.percentage
        )
    progress_bar_view.short_description = "Nível Gráfico"


@admin.register(CreativeStep)
class CreativeStepAdmin(admin.ModelAdmin):
    list_display = ('step_badge_view', 'title', 'order')
    list_editable = ('title', 'order')
    ordering = ('order',)
    
    def step_badge_view(self, obj):
        return format_html(
            '<span style="background: rgba(59, 102, 245, 0.2); color: #60a5fa; border: 1px solid rgba(59, 102, 245, 0.4); padding: 3px 10px; border-radius: 6px; font-weight: 700; font-size: 0.82rem;">Nº {}</span>',
            obj.step_number
        )
    step_badge_view.short_description = "Etapa"
