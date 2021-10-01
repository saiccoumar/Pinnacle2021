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
    # user_ids_series = np.array(data.index)
    movie_ids_series = data
    # print(user_ids_series[:2])
    print(movie_ids_series[:2])
    # User row and Movie Column
    # user_row = np.where(user_ids_series == user_id)[0]
    movie_col = np.where(movie_ids_series == movie_id)[0]
    
    # Take dot product of that row and column in U and V to make prediction
    
    pred = np.dot(user_mat, movie_mat)
    print("USERS AND MOVIES")
    # print(movie_ids_series)
    # print(user_ids_series)
    # print(user_row)
    # print(movie_col)

    movie_col = 10
    print("PRED")
    print(pred.shape)
    print(pred)
    user_row = 568
    print(movie_id)
    print(float(pred[user_row,movie_col]))
    print(type(float(pred[user_row,movie_col])))
    return float(pred[user_row,movie_col])

def create_train_test(data, t):
    data_DF = data.iloc[0:-10]    
    new_df = data.iloc[-10:]
    return data_DF, new_df

def loadDF(db="movies2.db"):
    con = sqlite3.connect(db)
    data = pd.read_sql("select * from itemRatings limit 100000",con)
    print(data.head)

    data['user'] = data['user'].astype('str')
    data['itemID'] = data['itemID'].astype('str')
    users = data['user'].unique() 
    movies = data['itemID'].unique() 

    data=data.pivot_table(index='user', columns='itemID', values='rating',fill_value=0)
    return data

def load_data_as_UIM(db="movies2.db"):
    con = sqlite3.connect(db)
    data = pd.read_sql("select * from itemRatings limit 100000",con)
    print(data.head)

    data['user'] = data['user'].astype('str')
    data['itemID'] = data['itemID'].astype('str')
    users = data['user'].unique() 
    movies = data['itemID'].unique() 

    print(data.shape)

    data_df,new_df = create_train_test(data,0.9)
    
    data=data.pivot_table(index='user', columns='itemID', values='rating',fill_value=0)
    
    print("TRAIN")
    print(data.shape)
    print(data.head())
    dataFinal = data.to_numpy()
    dataDF = dataFinal[:-10]
    newDF = dataFinal[-10:]
    return dataDF, newDF

def SVD(epochs,data,learning_rate=0.01,latent_features=6):
    

    # names = ['userId', 'movieId', 'rating', 'timestamp']
    # data = pd.read_csv('ml-100k/u.data', '\t', names=names,
    #                     engine='python')
    # # https://medium.com/@gazzaazhari/model-based-collaborative-filtering-systems-with-machine-learning-algorithm-d5994ae0f53b
    # columns = ['item_id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
    #         'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
    #         'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    # movies = pd.read_csv('ml-100k/u.item', sep='|', names=columns, encoding='latin-1')
    # movie_names = movies[['item_id', 'movie title']]
    # movie_names.head()


    


# NEW END
    data = data
    # data= data.to_numpy()
    # data = dataDF.to_numpy()

    p = np.random.uniform(0,1.1,size=(data.shape[0],latent_features))
    q = np.random.uniform(0,1.1,size=(latent_features, data.shape[1]))

    num_ratings = 0

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
                    num_ratings += 1
                    diff = data[i, j] - np.dot(p[i, :], q[:, j])
                    sse_accum += diff**2 #keep tracking the sum of square error for the matrix
                    for k in range(latent_features):
                        p[i, k] += learning_rate * (2*diff*q[k, j])
                        q[k, j] += learning_rate * (2*diff*p[i, k])
        learning_rate = learning_rate/1.02
        print("%d \t\t %f" % (epoch+1,np.sqrt(sse_accum / num_ratings)))
        num_ratings = 0 
    
    return(p,q,data)
def SVDUpgrade(d,epochs, user_matrix, item_matrix, learning_rate=0.0001,latent_features=6):
    data = d 
    p = user_matrix
    q = item_matrix

    num_ratings = 0
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
                    num_ratings+=1
                    diff = data[i, j] - np.dot(p[i, :], q[:, j])
                    # print(diff)
                    sse_accum += diff**2 #keep tracking the sum of square error for the matrix
                    for k in range(latent_features):
                        p[i, k] += learning_rate * (2*diff*q[k, j])
                        q[k, j] += learning_rate * (2*diff*p[i, k])
        learning_rate = learning_rate/1.02
        
        print("%d \t\t %f" % (epoch+1, np.sqrt(sse_accum / num_ratings)))
        num_ratings = 0
    pred = p.dot(q)
    print("PRED")
    print(pred[:10])
    print("DATA")
    print(data[:10])
    print("DELTA")
    delta = pred-data
    print(delta)
    count = 0
    
    for x_coord in range((data.shape[0])):
        for y_coord in range((data.shape[1])):
            if count<20:
                if data[x_coord,y_coord]:
                    print(delta[x_coord,y_coord])
                    count+=1
                
    return(p,q)
# train_data,test_data,new_data = load_data_as_UIM()
# print(data)
data,new_data = load_data_as_UIM()
dataFrame = loadDF()
print(len(data))
print(len(data[0]))

print("")
print(data)
print(len(new_data))
print(len(new_data[0]))
p,q,data=SVD(1,data)

for i in new_data:
    print(i)
    data = np.vstack([data,i])
print(len(data))
print(len(data[0]))
print(p.shape)
random = np.random.uniform(0,1.1,size=(data.shape[0]-p.shape[0],p.shape[1]))
for i in random:
    print(i)
    p = np.vstack([p,i])
print(p.shape)
p,q=SVDUpgrade(data, 15,p,q)
print(predict_rating(p,q,1,3448,dataFrame))
# print(predict_rating(p,q,1,2692,dataDF))
# print(predict_rating(p,q,1,2843,dataDF))