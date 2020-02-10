import pandas
import numpy
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

X = pandas.read_csv('Lab8_feature_data.csv')

for col in X:
    if isinstance(X.loc[1, col], str):
        X[col] = [complex(x.strip('()')) for x in X[col]]

y = X['user_id']

X = X.drop(columns='key_pressed')
X = X.drop(columns='user_id')

for col in X:
    if(X.loc[1,col],complex):
        X[col] = X[col].real

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8,stratify=y)


# paramopts = {'max_depth':[4,8,None], 
#     'n_estimators':[300,1000],
#     'n_jobs':[-1], 
#     'max_features':['sqrt', 'log2']}
# gridSearch = GridSearchCV(RandomForestClassifier(), paramopts, cv=3,verbose = 3, n_jobs = -1)
# gridSearch.fit(X_train,y_train)
# print(gridSearch.best_params_)



classifier = RandomForestClassifier(n_estimators=1000,max_depth=None,max_features='sqrt', random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', numpy.sqrt(metrics.mean_squared_error(y_test, y_pred)))
print('Accuracy:', metrics.accuracy_score(y_test, y_pred, normalize=True, sample_weight=None))





