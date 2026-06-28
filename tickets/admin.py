from django.contrib import admin
from .models import (
    UserProfile, UserSettings, Ticket, Comment,
    TicketHistory, AuditLog,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'items_per_page', 'email_notifications']
    list_filter = ['theme', 'email_notifications']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class TicketHistoryInline(admin.TabularInline):
    model = TicketHistory
    extra = 0
    readonly_fields = ['user', 'field', 'old_value', 'new_value', 'changed_at']
    can_delete = False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'service', 'status', 'priority', 'created_at']
    list_filter = ['status', 'priority', 'service', 'created_at']
    search_fields = ['title', 'description', 'owner__username']
    date_hierarchy = 'created_at'
    inlines = [CommentInline, TicketHistoryInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at']
    search_fields = ['text']


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'field', 'old_value', 'new_value', 'user', 'changed_at']
    list_filter = ['field', 'changed_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'request_id', 'user', 'method', 'path', 'status_code', 'ip']
    list_filter = ['method', 'status_code', 'created_at']
    search_fields = ['request_id', 'path', 'user__username', 'ip']
    date_hierarchy = 'created_at'
    readonly_fields = ['request_id', 'user', 'ip', 'user_agent', 'method',
                       'path', 'status_code', 'created_at']
