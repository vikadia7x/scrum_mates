import pyodbc
import pandas as pd
import numpy as np
from azure.storage.blob import BlockBlobService, PublicAccess
import os

"""
block_blob_service = BlockBlobService(account_name=account_name, account_key=key)

# Create a container called 'quickstartblobs'.
container_name ='quickstartblobs'
#block_blob_service.create_container(container_name)
local_path=os.getcwd()

fullpath = local_path + "/" + "meta_data.h5"
# Set the permission so the blobs are public.
block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

block_blob_service.create_blob_from_path(container_name, "meta_data.h5", fullpath)

print("\nList blobs in the container")
generator = block_blob_service.list_blobs(container_name)
for blob in generator:
    print("\t Blob name: " + blob.name)

full_path_to_file2 = local_path + "/" + "meta_data_1.h5"
block_blob_service.get_blob_to_path(container_name, "meta_data.h5", full_path_to_file2)

metaDataLinks1 = pd.read_hdf('meta_data_1.h5', 'metaDataLinks')

print(metaDataLinks1.head(50))
"""
userSelectedMovies = pd.DataFrame()
query_userselected = "SELECT * FROM [dbo].[showtimefinder_userselectmovies] WHERE isMovieRec = 0"
for chunk in pd.read_sql_query(query_userselected, cnxn, chunksize=10**4):
    userSelectedMovies = pd.concat([userSelectedMovies, chunk])
    print(userSelectedMovies)
print(userSelectedMovies.shape)
userSelectedMovies['movieName'] = userSelectedMovies['movieName'].astype(str)
print(userSelectedMovies.dtypes)

#Schedule query to change the isMovieRec value to 0 twice weekly

"""
userSelectedMovies['recommended'] = userSelectedMovies['movieName'].apply(recommendation)

def recommendation(movieName):
    
    return movieList
"""
    




