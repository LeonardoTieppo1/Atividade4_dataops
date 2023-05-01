from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
credentials_dict = {
  "type": "service_account",
  "project_id": "model-calling-343600",
  "private_key_id": "ac7eda61b6fa29bdcbe6ea02da2dd3f8ebaf450c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCo1gzgUAt1Rosk\n2YzaTNKBcVRtXjHfoCSj/H3HvQKQoYzi3uCchClknBMnJG3JFcPv1HjAy3UPv89V\nCRxIbq7WKGa9NhgcVZemcs2cKb5/DgyZSTMmj4erAJ2XTw9IE92PSYK3IqtFYULQ\nlY8WDwP7VPqB0dYZ46w64nUkuiXxId30vsZqcvDBZUzA+VhNQJ6mBQ5M5WUyGcsG\nWmL/66GGAawOkkVuzHz3U3XmdodjwMQKnjwDtuRce1aicG4y58i8nBm+vbhbmfax\nLgM5VISvfEVSjQxGyi/FsqE1jpopbLYv0bsZYGNSWf3RuGLJmOu8s+E7oG2mzsUl\nnGSpHjZDAgMBAAECggEAA8EZJMz5QqcKONkMX6q3czQDPEvAA/V9kX0i8BPJxum/\nH/WNyan+RtbzoOCxMkUyIX1rhZOT0eeIsDh7vdHJDUkO5v3/cXRAllQImQR5A6R0\nokOO7oVHIoXPSBb0qe+LJmcF9mJZrAX6it6jtMoqFmbwceRdHh+o0kX72qoeMt6H\nj+TlWxfHyM6H8P8xTUKjlnLFe5pzXfOb+WQC3S9UX4WkzSC+cA6OxzSAp+PadrkH\nY9iCVotOdMV5hPZowHz/qBwNR/IaU9EN1H4Fr/2rUZk4NN95KIAK6yim7KOFtzbS\nlVnHxbEwUWOLtRiDBkVXdE/Jdr/e3UtiLD9JHPMIFQKBgQDbXqGpiGvh54pMsTSf\nPGYMBtp3qqbr2it9Hg5pxNPLRsJKEJKG9jXPQhgVrbK3SEZJ28PW1YCXrSgGvxq8\nNu4hGNoNRlTyKtN5aDaJ6bMnA82nmSC+vtH7sAXU8sh7DcDIkMJCD9OfGyy6FbPi\ndKEWHkwp5zBgZCTLbyaTn93rrQKBgQDFB0S3j1onE+krCuEBbnWyNX3445GfYAQH\no/b54al49WlheFxlos1gDUwfs08OEcPr6h1YS3Pw8A2t3Q7zlDMblCPBq+9yCt6e\nLewcm+4l/WDUaS6IYmTnMd/wBz/m8NrQcpr72BI8mrLguJa0pg/lfV9XUjxeNsxJ\n/MCEa+XnrwKBgQCaMRTupg42dlo2d+Ql/P05fOO4c0Hqy6n/ws2cuJWp7y2Hg8iK\nhqrh6HInYrUYsPt+1LL94YoGktZsj40KOI3+w4oZBJOWuFV2o7KaE6MyTDEUmcRz\nbosIHvyqZpBWNh+Imn+AkcFMt3wjvDd5eEL12gvs9CyDxEA8of76iscg7QKBgE2Z\ns0LovwUtHmTJgB1kOA7caqUgXDZ9RpkLxzZb3re5UKwHD70oBeOS2SyTHsvXy2ab\nartf3GZE5d5Ydo8RC6ANFJgu87vi9BMw2xHZiE6GISEH3D/zIPK9/gk3kb+PlV8M\nBGa0j1o3Q8SmbxTvYstsOaTWytgAlS1+0wRUytQZAoGBAMyliSLNBW8pi9/LXZgI\nxhRZvz8ENZPlYsKCTgvclcyLbj0d7iFnz5eNxUaiBD5hZtgqgq2/qGnFbHwaAYt9\nHVehzkxowTVWnspS/IJ0yNv6apzcqPWvZe7aWZSUvFeYw21fA37aIYSFfYPSHobX\ntfqepDfRZx7eJ4YWuhzV04je\n-----END PRIVATE KEY-----\n",
  "client_email": "storagedataops@model-calling-343600.iam.gserviceaccount.com",
  "client_id": "104637843235005142622",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/storagedataops%40model-calling-343600.iam.gserviceaccount.com"
}

try:

    credentials =service_account.Credentials.from_service_account_info(credentials_dict)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket('atividade4_dataops_names')
    blob = bucket.blob('artist-names.csv')

    pages = []
    names = "Name \n"
    
    for i in range(1, 5):
        url ='https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' +str(i) + '.htm'
        pages.append(url)
    for item in pages:
        page = requests.get(item)
        soup = BeautifulSoup(page.text, 'html.parser')

        last_links = soup.find(class_='AlphaNav')
        last_links.decompose()
    
        artist_name_list = soup.find(class_='BodyText')
        artist_name_list_items = artist_name_list.find_all('a')
    
    for artist_name in artist_name_list_items:
        names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")
except Exception as ex:
    print(ex)
