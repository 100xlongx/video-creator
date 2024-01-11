from peewee import Model, CharField, TextField, DateTimeField, PrimaryKeyField
from .database import db
import datetime

class OAuthTokens(Model):
    id = PrimaryKeyField()
    user_id = CharField(max_length=255)
    provider = CharField(max_length=50)
    access_token = TextField()
    refresh_token = TextField(null=True)
    expires_at = DateTimeField()
    scopes = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return (f"ID: {self.id}, User ID: {self.user_id}, Provider: {self.provider}, "
            f"Access Token: {self.access_token}, Refresh Token: {self.refresh_token}, "
            f"Expires At: {self.expires_at}, Scopes: {self.scopes}, "
            f"Created At: {self.created_at}, Updated At: {self.updated_at}")
    
    class Meta:
        database = db
        table_name = 'oauth_tokens'