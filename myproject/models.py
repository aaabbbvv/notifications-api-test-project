# from django.db import models
#
#
# class Country(models.Model):
#     name = models.CharField(max_length=25, blank=True, null=True)
#     code = models.CharField(max_length=5, blank=True, null=True)
#     code_exp = models.CharField(max_length=5, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'country'
#
#
# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)
#
#
# class Language(models.Model):
#     name = models.CharField(max_length=32, blank=True, null=True)
#     title = models.CharField(max_length=32, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'language'
#
#
# class NotificationCategory(models.Model):
#     name = models.CharField(max_length=32, blank=True, null=True)
#     title = models.CharField(max_length=32, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'notification_category'
#
#
# class NotificationTemplate(models.Model):
#     notification_category = models.ForeignKey(NotificationCategory, models.DO_NOTHING, blank=True, null=True)
#     name = models.CharField(max_length=32, blank=True, null=True)
#     txt = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'notification_template'
#
#
# class Project(models.Model):
#     user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
#     name = models.CharField(max_length=510, blank=True, null=True)
#     address = models.CharField(max_length=510, blank=True, null=True)
#     started = models.DateTimeField()
#     lat = models.FloatField(blank=True, null=True)
#     lng = models.FloatField(blank=True, null=True)
#     country = models.ForeignKey(Country, models.DO_NOTHING)
#     archived = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'project'
#
#
# class TranslationString(models.Model):
#     content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)
#     object_id = models.IntegerField(blank=True, null=True)
#     translation_field_id = models.IntegerField(blank=True, null=True)
#     language = models.ForeignKey(Language, models.DO_NOTHING, blank=True, null=True)
#     text = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'translation_string'
#
#
# class User(models.Model):
#     first_name = models.CharField(max_length=255, blank=True, null=True)
#     last_name = models.CharField(max_length=255, blank=True, null=True)
#     email = models.CharField(unique=True, max_length=255, blank=True, null=True)
#     role_id = models.PositiveIntegerField(blank=True, null=True)
#     password = models.CharField(max_length=45, blank=True, null=True)
#     active = models.IntegerField(blank=True, null=True)
#     verified = models.IntegerField(blank=True, null=True)
#     language = models.ForeignKey(Language, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'user'
#
#
# class UserNotification(models.Model):
#     user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
#     notification_template = models.ForeignKey(NotificationTemplate, models.DO_NOTHING, blank=True, null=True)
#     notification_type = models.IntegerField()
#     status = models.IntegerField()
#     created = models.DateTimeField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user_notification'
#
#
# class UserNotificationOption(models.Model):
#     user_notification = models.ForeignKey(UserNotification, models.DO_NOTHING, blank=True, null=True)
#     field_id = models.IntegerField(blank=True, null=True)
#     txt = models.CharField(max_length=32, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user_notification_option'
#
#
# class UserNotificationSetting(models.Model):
#     user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
#     notification_template = models.ForeignKey(NotificationTemplate, models.DO_NOTHING, blank=True, null=True)
#     system_notification = models.IntegerField()
#     push_notification = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'user_notification_setting'
#
#
# class UserRole(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'user_role'
