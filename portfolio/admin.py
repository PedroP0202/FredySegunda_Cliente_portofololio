from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Project, GeneralSetting, Tool, CreativeStep


@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identidade da Marca & SEO", {
            "fields": ("site_title", "meta_description"),
            "description": "Configurações gerais para motores de busca (Google) e cabeçalhos de navegador."
        }),
        ("Status de Agenda & Disponibilidade", {
            "fields": ("is_available", "availability_badge_text", "hero_year"),
            "description": "Controle em tempo real se o indicador luminoso no topo do site exibe agenda disponível ou em projeto."
        }),
        ("Apresentação Principal (Hero)", {
            "fields": ("hero_title", "hero_desc", "cv_file"),
            "description": "Textos de introdução ao seu trabalho e ficheiro para download do currículo."
        }),
        ("Estatísticas de Destaque", {
            "fields": (
                ("stat1_number", "stat1_label"),
                ("stat2_number", "stat2_label"),
                ("stat3_number", "stat3_label")
            ),
            "description": "Indicadores chave apresentados abaixo dos botões iniciais."
        }),
        ("Canais de Contacto & Redes Sociais", {
            "fields": ("contact_email", "whatsapp_number", "link_behance", "link_dribbble", "link_instagram", "link_linkedin", "link_github"),
            "description": "Links sociais exibidos no rodapé e número para botão de chat WhatsApp direto."
        }),
        ("Bloco Final de Conversão (CTA)", {
            "fields": ("cta_title", "cta_subtitle"),
            "description": "Mensagem convidativa na área final do portfólio antes do contacto."
        }),
    )

    def has_add_permission(self, request):
        if GeneralSetting.objects.exists():
            return False
        return True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('media_preview_box', 'title_display', 'section_badge', 'category', 'client_name', 'order', 'is_video')
    list_editable = ('order', 'is_video')
    list_filter = ('section', 'is_video', 'project_year', 'category')
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
            "fields": ("media_file", "is_video", "section", "order"),
            "description": "Selecione a obra no Cloudinary e escolha em que galeria do site deseja expor o trabalho."
        }),
        ("Conteúdo Editorial & Narrativa", {
            "fields": ("title", "category", "description"),
            "description": "Textos descritivos que acompanham o cartão editorial no site."
        }),
        ("Metadados & Ligações Externas", {
            "fields": ("client_name", "project_year", "featured_tag", "project_url"),
            "classes": ("collapse",),
            "description": "Informações de apoio (ano da obra, nome da marca e link para visualização no Behance/Live site)."
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
    section_badge.short_description = "Secção no Site"

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
        updated = queryset.update(section='featured_main')
        self.message_user(request, f"{updated} obra(s) movida(s) para o Showcase Principal do site.", messages.SUCCESS)

    @admin.action(description="■ Mover selecionados para Destaques Secundários")
    def move_to_featured_side(self, request, queryset):
        updated = queryset.update(section='featured_side')
        self.message_user(request, f"{updated} obra(s) movida(s) para os Destaques Secundários.", messages.SUCCESS)

    @admin.action(description="❖ Mover selecionados para Galeria (3 Colunas)")
    def move_to_gallery_small(self, request, queryset):
        updated = queryset.update(section='gallery_small')
        self.message_user(request, f"{updated} obra(s) transferida(s) para a Galeria de Criações.", messages.SUCCESS)

    @admin.action(description="◆ Mover selecionados para Galeria Assimétrica")
    def move_to_gallery_asym(self, request, queryset):
        updated = queryset.update(section='gallery_asym')
        self.message_user(request, f"{updated} obra(s) atribuida(s) à Galeria Assimétrica.", messages.SUCCESS)

    @admin.action(description="🎬 Mover selecionados para Vídeo Reel")
    def move_to_reel(self, request, queryset):
        updated = queryset.update(section='reel', is_video=True)
        self.message_user(request, f"{updated} obra(s) movida(s) e ativadas na secção de Vídeo Reel.", messages.SUCCESS)

    @admin.action(description="🔄 Alternar Status de Vídeo / Imagem")
    def toggle_video_status(self, request, queryset):
        for obj in queryset:
            obj.is_video = not obj.is_video
            obj.save()
        self.message_user(request, f"Status de vídeo invertido para {queryset.count()} obra(s).", messages.INFO)


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
