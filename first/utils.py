from django.db.models import base
import matplotlib.pyplot as plt
import seaborn  as sns
import base64
from io import BytesIO
from django.contrib.auth.models import User 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
from sklearn.preprocessing import LabelEncoder



def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_center_coordinates(latA , lonA , latB=None , lonB=None):
    cord = (latA , lonA)
    if latB:
        cord = [(latA+latB)/2 , (lonA+lonB)/2]
    return cord

def get_zoom(distance):
    if distance <=100:
        return 16
    elif distance > 100 and distance <=5000:
        return 4
    else:
        return 2


def get_image():
    # create a bytes buffer for the image to save
    buffer = BytesIO()
    # create the plot with the use of BytesIO object as its file
    plt.savefig(buffer , format="png")
    # set the cursor beg of the stream
    buffer.seek(0)
    # retrive the entire content of the 'file'
    image_png = buffer.getvalue()
    # encoding decoding
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    # free the memory of buffer
    buffer.close()

    return graph


def get_simple_plot(chart , *args , **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    plt.xticks(rotation = 45)
    colors = sns.color_palette('pastel')[0:5]
    x = kwargs.get('base')
    print(x)
    data = kwargs.get('data')

    if chart == 'pie':
        Encoder = LabelEncoder()
        data = Encoder.fit_transform(data[x])
        plt.pie(data)
    else:
        sns.countplot(x=x,data=data)
    plt.tight_layout()


    graph = get_image()
    return graph