import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing


# NEW Begin

def create_train_test(data, t):
    training_df = data.iloc[0:int(data.shape[0]*t)]    
    validation_df = data.iloc[int(data.shape[0]*t):-10]    
    new_df = data.iloc[-10:]
    return training_df, validation_df,new_df

def predict_rating(user_mat, movie_mat, user_id, movie_id,data):
    
    # Use the training data to create a series of users and movies that matches the ordering in training data
    user_ids_series = np.array(data.index)
    movie_ids_series = np.array(data.columns)
    
    # User row and Movie Column
    user_row = np.where(user_ids_series == user_id)[0][0]
    movie_col = np.where(movie_ids_series == movie_id)[0][0]
    
    # Take dot product of that row and column in U and V to make prediction
    pred = np.dot(user_mat[user_row, :], movie_mat[:, movie_col])
    
    return pred


def validation_comparison(val_df, num_preds,user_mat,movie_mat,data):
    # Thank you anna wangliu
    val_users = np.array(val_df['userId'])
    val_movies = np.array(val_df['movieId'])
    val_ratings = np.array(val_df['rating'])    
    
    for index in range(num_preds):
        print (val_users[index],val_movies[index], val_ratings[index])
        pred = predict_rating(user_mat, movie_mat, val_users[index], val_movies[index],data)        
        print("The actual rating for user {} on movie {} is {}.\n While the predicted rating is {}.".format(val_users[index], val_movies[index], val_ratings[index], round(pred)))
        print("The RMSE for is {}",rmse(val_ratings[index],pred))


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



data['userId'] = data['userId'].astype('str')
data['movieId'] = data['movieId'].astype('str')
users = data['userId'].unique() 
movies = data['movieId'].unique() 

# print(data.shape[0]*0.9)
training_df, validation_df,new_df = create_train_test(data,0.9)
print("FLAG")
print(data.shape)
print(training_df.shape)
print(validation_df.shape)
print(new_df.shape)

print("Total Unique Users", len(users))
# should be 943
print("Total Unique Movies", len(movies))
# should be 1682
print(data.head())
data3=data.pivot_table(index='userId', columns='movieId', values='rating',fill_value=0)
data = training_df.pivot_table(index='userId', columns='movieId', values='rating',fill_value=0)
# https://predictivehacks.com/item-based-collaborative-filtering-in-python/
data2 = validation_df.pivot_table(index='userId', columns='movieId', values='rating',fill_value=0)
data4 = new_df.pivot_table(index='userId', columns='movieId', values='rating',fill_value=0)

print("TRAIN")
print(data.shape)
print(data.head())
print("TEST")
print(data2.shape)
print(data2.head())


# NEW END

data = data.to_numpy()
data2 = data2.to_numpy()
data3 = data3.to_numpy()
data4 = data4.to_numpy()
def SVD(epochs,learning_rate=0.01,latent_features=6, ):

    p = np.random.uniform(0,1.1,size=(data.shape[0],latent_features))
    q = np.random.uniform(0,1.1,size=(latent_features, data.shape[1]))

    num_ratings = np.count_nonzero(~np.isnan(data))
# print(p)
# print(q)
    sse_accum = 0
    pred = p.dot(q)
    print("PRED")
    print(pred)
    print("DATA")
    print(data)
    print("DELTA")

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
def SVDUpgrade(epochs, user_matrix, item_matrix, learning_rate=0.0001,latent_features=6):

    p = user_matrix
    q = item_matrix

    num_ratings = np.count_nonzero(~np.isnan(data))
# print(p)
# print(q)
    sse_accum = 0
    pred = p.dot(q)
    print("PRED")
    print(pred)
    print("DATA")
    print(data)
    print("DELTA")

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
# p,q=SVD(20)
# p,q=SVDUpgrade(5,p,q)
print(data.shape)
print(data4.shape)
data = data+data4
# p,q = SVDUpdate(p,q)
print("RMSE: ")
# print(p.dot(q)-data)
# print(validation_comparison(validation_df,10,p,q,data3))
# p,q=SVD(25)

