from flask import render_template, url_for, flash, redirect, request, Blueprint ,current_app,send_from_directory,Response,send_file
from flask_login import current_user,login_required
from app.models import Files
from app import db
from app.dashboard.forms import UploadFile
import os
import hashlib
import uuid
from azure.storage.blob import BlobClient


dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/dashboard" ,methods=["GET","POST"])
@login_required
def dash():
    form=UploadFile()
    files=Files.query.filter_by(username=current_user.username).all()
    if form.validate_on_submit():
        file=request.files['uploaded_file']
        file_md5=hashlib.md5(file.read()).hexdigest()
        file.seek(0)

        check_for_existing=Files.query.filter_by(username=current_user.username,md5=file_md5).first()
        if check_for_existing is None:
            file_name=Files.query.filter_by(fileName=file.filename).first()
            if file_name is not None:
                if (file_name.fileName==file.filename):
                       file.filename=os.path.splitext(file.filename)[0] + ' - ' + str(uuid.uuid4())[:8] + os.path.splitext(file.filename)[1]

            if current_app.config['UPLOAD_AZURE_BLOB']:
                upload_to_azure_storage_blob(file)
            else:
                upload_to_local_storage(file)

            obj=Files(username=current_user.username,fileName=file.filename,md5=file_md5)
            db.session.add(obj)
            db.session.commit()

            flash('File Uploaded Successfully', 'success')
            return redirect(url_for('dashboard.dash'))
        else:
            if(file.filename==check_for_existing.fileName):
                flash('File Already Exists', 'danger')
            else:
                flash('File Already Exists as '+check_for_existing.fileName, 'danger')
            return redirect(url_for('dashboard.dash'))
    return render_template("dashboard/dashboard.html" ,title="Dashboard", files=files,form=form)

@dashboard.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if current_app.config['UPLOAD_AZURE_BLOB']:
        url=current_app.config['AZURE_BLOB_PUBLIC_URL']+filename
        return redirect(url)
    else:    
        path = os.path.join(current_app.root_path,'files')
        return send_from_directory(directory=path, filename=filename, as_attachment=True)

@dashboard.route('/delete/<path:filename>',methods=['GET','POST'])
def delete(filename):
    if current_app.config['UPLOAD_AZURE_BLOB']:
        delete_from_azure_storage_blob(filename)
    else:
        delete_from_local_storage(filename)
    Files.query.filter_by(username=current_user.username,fileName=filename).delete()
    db.session.commit()
    flash('File Deleted Successfully', 'success')
    return redirect(url_for('dashboard.dash'))

def upload_to_local_storage(file):
    file_path=os.path.join(current_app.config['UPLOAD_FOLDER'],file.filename)
    file.save(file_path)

def delete_from_local_storage(filename):
    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))

def upload_to_azure_storage_blob(file):
    blob_client=BlobClient.from_connection_string(current_app.config['AZURE_BLOB_CONNECTION_STRING'],
                                                    current_app.config['AZURE_BLOB_CONTAINER_NAME'],
                                                    file.filename)
    blob_client.upload_blob(file)

def delete_from_azure_storage_blob(filename):
    blob_client=BlobClient.from_connection_string(current_app.config['AZURE_BLOB_CONNECTION_STRING'],
                                                    current_app.config['AZURE_BLOB_CONTAINER_NAME'],
                                                    filename)
    blob_client.delete_blob()