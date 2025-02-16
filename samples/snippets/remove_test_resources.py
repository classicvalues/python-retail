# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.api_core.exceptions import PermissionDenied
from google.cloud.storage.bucket import Bucket

from google.cloud import storage
from google.cloud.retail import DeleteProductRequest, ListProductsRequest, \
    ProductServiceClient

project_number = os.getenv('GOOGLE_CLOUD_PROJECT_NUMBER')
bucket_name = os.getenv('BUCKET_NAME')

default_catalog = "projects/{0}/locations/global/catalogs/default_catalog/branches/default_branch".format(
    project_number)

storage_client = storage.Client()


def delete_bucket():
    """Delete bucket"""
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except:
        print("Bucket {} does not exists".format(bucket_name))
    else:
        delete_object_from_bucket(bucket)
        bucket.delete()
        print("bucket {} is deleted".format(bucket_name))


def delete_object_from_bucket(bucket: Bucket):
    """Delete object from bucket"""
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()
    print("all objects are deleted from GCS bucket {}".format(bucket.name))


def delete_all_products():
    """Delete all products in the catalog"""
    product_client = ProductServiceClient()
    list_request = ListProductsRequest()
    list_request.parent = default_catalog
    products = product_client.list_products(list_request)
    delete_count = 0
    for product in products:
        delete_request = DeleteProductRequest()
        delete_request.name = product.name
        try:
            product_client.delete_product(delete_request)
            delete_count += 1
        except PermissionDenied:
            print(
                "Ignore PermissionDenied in case the product does not exist at time of deletion")
    print(f"{delete_count} products were deleted from {default_catalog}")


delete_bucket()
delete_all_products()
