# drive_utils.py

import io
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

def download_file(service, file_id):
    try:
        request = service.files().get_media(fileId=file_id)
        file_io = io.BytesIO()
        downloader = MediaIoBaseDownload(file_io, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download status: {int(status.progress() * 100)}%")
        file_io.seek(0)
        return file_io
    except Exception as e:
        print(f"Error downloading file ID {file_id}: {e}")
        raise

def upload_file(service, folder_id, doc, file_name):
    try:
        file_io = io.BytesIO()
        doc.save(file_io)
        file_io.seek(0)

        file_metadata = {
            'name': file_name,
            'parents': [folder_id],
            'mimeType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }

        media = MediaIoBaseUpload(file_io, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File uploaded with ID: {file.get('id')}")
        return file.get('id')
    except Exception as e:
        print(f"Error uploading file {file_name}: {e}")
        raise