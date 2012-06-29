# -*- coding: UTF-8 -*-
#

from __future__ import with_statement
import urllib,re,random,json
from google.appengine.api import files
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
    def get(self):
        data = {}
        q = KeyValue.all()
        data["file_list"] = []
        data["save_url"] = self.request.host_url + '/disk/content/'
        data["del_url"] =self.request.host_url + '/disk/delete?id=' 
        for s in q:
            data["file_list"].append(s.key_index)
        data["upload_url"] = self.request.host_url + "/disk/upload"#upload_url
        path = 'disk/index.html'
        self.response.out.write(template.render(path, data))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get_file_size(self, file):
        file.seek(0, 2) # Seek to the end of the file
        size = file.tell() # Get the position of EOF
        file.seek(0) # Reset the file position to the beginning
        return size
    
    def write_blob(self, data, info):
        blob = files.blobstore.create(
            mime_type=info['type'],
            _blobinfo_uploaded_filename=info['name']
        )
        with files.open(blob, 'a') as f:
            f.write(data)
        files.finalize(blob)
        return files.blobstore.get_blob_key(blob)


    def post(self):
        for name, fieldStorage in self.request.POST.items():
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = str(random.randint(0, 1000)) + re.sub(r'^.*\\', '',
                fieldStorage.filename)
            result['type'] = fieldStorage.type
            result['size'] = self.get_file_size(fieldStorage.file)

            blob_key = str(self.write_blob(fieldStorage.value, result))
            blob_info = blobstore.BlobInfo.get(blob_key)
            key = blob_info.filename
            value = str(blob_info.key())
            t = KeyValue(key_index = key, value = value)
            t.put()
            result["url"] = self.request.host_url + '/disk/content/%s' % key
            result["error"] = 0
            result["message"] = "SUCCESS" 
            self.response.write(json.dumps(result, separators=(',',':')))
            return
class DeleteHandler(webapp.RequestHandler):
    def get(self):
        id = self.request.get('id')
        if not id:
            self.response.set_status(404)
        q = KeyValue.all()
        q.filter("key_index", id)
        for s in q:
            blob_info = blobstore.BlobInfo.get(s.value)
            blob_info.delete()
        db.delete(q)
        
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        q= KeyValue.all()
        q.filter("key_index = ", resource)
        re = q.fetch(1)
        if len(re) == 0:
            self.response.set_status(404)
            return
        
        blob_info = blobstore.BlobInfo.get(re[0].value)
        self.send_blob(blob_info)

class KeyValue(db.Model):
    key_index = db.StringProperty(required=True)
    value = db.StringProperty()
