from sqlite3.dbapi2 import connect
import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
import sqlite3
# from svd import predict_rating,SVD
def predict_rating(user_mat, movie_mat, user_id, movie_id,data):
    
    # Use the training data to create a series of users and movies that matches the ordering in training data
    user_ids_series = np.array(data.index)
    movie_ids_series = np.array(data.columns)
    print(user_ids_series[:2])
    print(movie_ids_series[:2])
    # User row and Movie Column
    user_row = np.where(user_ids_series == user_id)[0]
    movie_col = np.where(movie_ids_series == movie_id)[0]
    
    # Take dot product of that row and column in U and V to make prediction
    pred = np.dot(user_mat[user_row, :], movie_mat[:, movie_col])
    
    return pred

def SVD(epochs,learning_rate=0.01,latent_features=6,db="movies2.db"):
    con = sqlite3.connect(db)
    data = pd.read_sql("select * from itemRatings limit 100000",con)
    print(data.head)

    """
    names = ['userId', 'movieId', 'rating', 'timestamp']
    data = pd.read_csv('ml-100k/u.data', '\t', names=names,
                        engine='python')
    # https://medium.com/@gazzaazhari/model-based-collaborative-filtering-systems-with-machine-learning-algorithm-d5994ae0f53b
    columns = ['item_id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
            'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
            'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    movies = pd.read_csv('ml-100k/u.item', sep='|', names=columns, encoding='latin-1')
    movie_names = movies[['item_id', 'movie title']]
    movie_names.head()


    """
    data['user'] = data['user'].astype('str')
    data['itemID'] = data['itemID'].astype('str')
    users = data['user'].unique() 
    movies = data['itemID'].unique() 

    print(data.shape)

#training_df, validation_df,new_df = create_train_test(data,0.9)

    dataDF=data.pivot_table(index='user', columns='itemID', values='rating',fill_value=0)


    print("TRAIN")
    print(dataDF.shape)
    print(dataDF.head())


# NEW END
    data = dataDF.to_numpy()

    p = np.random.uniform(0,1.1,size=(data.shape[0],latent_features))
    q = np.random.uniform(0,1.1,size=(latent_features, data.shape[1]))

    num_ratings = np.count_nonzero(~np.isnan(data))

    sse_accum = 0
    pred = p.dot(q)
    print("PRED")
    print(pred)
    print("DATA")
    print(data)
    print("DELTA")
    print(pred-data)

    for epoch in range(epochs):
        sse_accum=0
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                # sse_accum = 0
        # if the rating exists
        
#             print(data[i,j])
                if data[i, j] > 0:
                    diff = data[i, j] - np.dot(p[i, :], q[:, j])
                    sse_accum += diff**2 #keep tracking the sum of square error for the matrix
                    for k in range(latent_features):
                        p[i, k] += learning_rate * (2*diff*q[k, j])
                        q[k, j] += learning_rate * (2*diff*p[i, k])
        learning_rate = learning_rate/1.02
        print("%d \t\t %f" % (epoch+1, sse_accum / num_ratings))
    return(p,q,data,dataDF)
def SVDUpgrade(d,epochs, user_matrix, item_matrix, learning_rate=0.0001,latent_features=6):
    data = d 
    p = user_matrix
    q = item_matrix

    num_ratings = np.count_nonzero(~np.isnan(data))
    sse_accum = 0
    pred = p.dot(q)
    print("PRED")
    print(pred)
    print("DATA")
    print(data)
    print("DELTA")
    print(pred-data)

    for epoch in range(epochs):
        sse_accum=0
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                # sse_accum = 0
        # if the rating exists
        
#             print(data[i,j])
                if data[i, j] > 0:
                    diff = data[i, j] - np.dot(p[i, :], q[:, j])
                    sse_accum += diff**2 #keep tracking the sum of square error for the matrix
                    for k in range(latent_features):
                        p[i, k] += learning_rate * (2*diff*q[k, j])
                        q[k, j] += learning_rate * (2*diff*p[i, k])
        learning_rate = learning_rate/1.02
        print("%d \t\t %f" % (epoch+1, sse_accum / num_ratings))
    return(p,q)
p,q,data,dataDF=SVD(4)
p,q=SVDUpgrade(data, 3,p,q)
print(predict_rating(p,q,1,3448,dataDF))
print(predict_rating(p,q,1,2692,dataDF))
print(predict_rating(p,q,1,2843,dataDF))