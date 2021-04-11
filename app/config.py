import os


class Config:
    SECRET_KEY = 'secretkey'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    UPLOAD_FOLDER = 'app/files'

    #Set To True if you want to upload to azure blob storage
    UPLOAD_AZURE_BLOB = False
    AZURE_BLOB_CONNECTION_STRING=''
    AZURE_BLOB_CONTAINER_NAME=''
    AZURE_BLOB_PUBLIC_URL='' #https://{account_name}.blob.core.windows.net/{container_name}/
