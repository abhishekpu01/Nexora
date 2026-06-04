from fastapi import FastAPI, UploadFile, File, Form
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from nexoraadmin_service.utils.utils import get_base_color, createSuccessResponse, createFailedResponse
import tensorflow as tf
load_dotenv()
import cv2
import numpy as np
from contextlib import asynccontextmanager
import os
from transformers import pipeline
from nexoraadmin_service.constants.labels import TYPE_LABELS, TYPE_TO_CATEGORY
from nexoraadmin_service.decorators.decorator import check_permissions
import base64

app = FastAPI()

@app.post("/getmetadata")
@check_permissions(['PRODUCT_CREATE', 'PRODUCT_EDIT', 'PRODUCTVARIANT_CREATE', 'PRODUCTVARIANT_EDIT'])
async def getMetaData(image: UploadFile = File(...), flag: bool = Form(...),token: str = Form(...)):
    try:
        contents = await image.read()
        if flag:
            try:
                classifier = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
                result = classifier(base64.b64encode(contents).decode("utf-8"), candidate_labels=TYPE_LABELS)
                response = None
                max = 0
                for prob in result:
                    if prob['score'] > max:
                        max = prob['score']
                        response = prob

                if response:
                    response['category'] = TYPE_TO_CATEGORY[response['label']]
                return createSuccessResponse(response)
            except Exception as e:
                return createFailedResponse(str(e))

        else:
            try:
                nparr = np.frombuffer(contents, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w = img.shape[:2]

                crop = img[
                    h//4:3*h//4,
                    w//4:3*w//4
                ]

                pixels = crop.reshape(-1, 3)

                kmeans = KMeans(n_clusters=3, random_state=42)
                kmeans.fit(pixels)
                colors = kmeans.cluster_centers_.astype(int)
                counts = np.bincount(kmeans.labels_)
                dominant_color = colors[np.argmax(counts)]
                result = get_base_color(dominant_color)
                return createSuccessResponse({'color':result})
            
            except Exception as e:
                return createFailedResponse(str(e))
            
    except Exception as e:
        return createFailedResponse(str(e))
