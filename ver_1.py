import requests, zipfile , os, tempfile , boto3
urls =['']

def download_handler(links_list):
    for link in links_list:
        data = requests.get(link)
        tmp = tempfile.NamedTemporaryFile(mode ='wb')
        full_filename = tmp.name
        dirname = os.path.dirname(full_filename)
        with open(full_filename, 'wb') as f:
            f.write(data.content)
            f.close()
        try:
            with zipfile.ZipFile(full_filename) as zf:
                zf.extractall(dirname)      
        except:
            os.rename(full_filename , dirname + "/" + os.path.basename(link))
            dirlist = os.listdir(dirname)
    return(dirname , dirlist)
def lambda_handler(event, context):
    bucket = ""
    s3 = boto3.resource('')
    upload_folder, upload_files = (download_handler(urls))
    for file in upload_files:
        file_path = upload_folder + "/" + file
        s3.meta.client.upload_file(file_path, bucket, file)
    return()