# -*- coding: utf-8 -*-
"""PCA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lWNgleoP9AQpyIxBNYcbbbTnfXogWcjr
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib as mpl
import matplotlib.pyplot as plt

plt.style.use('ggplot')

"""# **First, we load the dataset using Scikit-learn load_breast_cancer() function. Then, we convert the data into a pandas DataFrame  ** ****"""

from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
df = pd.DataFrame(data=cancer.data, columns=cancer.feature_names)

df.shape

df.head()

"""# **Apply PCA**

In the breast_cancer dataset, the original feature space has 30 dimensions denoted by p. PCA will transform (reduce) data into a k number of dimensions (where k << p) while keeping as much of the variation in the original dataset as possible. These k dimensions are known as the principal components.

# **Obtain the feature matrix**
"""

X = df.values
X.shape

"""# **Standardadise the Features**

The STANDARDIZE Z-Score Function will return a normalized value (z-score) based on the mean and standard deviation.
A z-score, or standard score, is used for standardizing scores on the same scale by dividing a score’s deviation by the standard deviation in a data set.

The values of the dataset are not equally scaled. So, we need to apply **z-score standardization** to get all features into the same scale. For this, we use S**cikit-learn "StandardScaler()"** class which is in the preprocessing submodule in **Scikit-learn**
"""

#Import the class
from sklearn.preprocessing import StandardScaler

#Create the object
scaler = StandardScaler()

#Calculate the mean and standard deviation
scaler.fit(X)
# Transform the values
X_scaled = scaler.transform(X)

"""**X_scaled which is also a 569x30 two-dimensional Numpy array.**

# **Choose the right number of dimensions (k)**

**Now, we are ready to apply PCA to our dataset. Before that, we need to choose the right number of dimensions (i.e., the right number of principal components — k). For this, we apply PCA with the original number of dimensions (i.e., 30) and see how well PCA captures the variance of the data.**

When developing a statistical model, one often uses methods that take advantage of randomness to lower the variance in your model and lessen the effects of overfitting.

**As a model is tuned and hyperparameters are adjusted, you want to ensure that any improvements (or declines in performance) are due to the actual changes you made, rather than due to the randomness you introduced. This is why it is imperative to set a random state (sometimes called a random seed), so that throughout the development process the same randomly-chosen data points (or randomly assigned parameters, whatever it may be) are being chosen every time.**
"""

from sklearn.decomposition import PCA

pca_30 = PCA(n_components=30, random_state=2020)
pca_30.fit(X_scaled)
X_pca_30 = pca_30.transform(X_scaled)

"""https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

Well, in PCA

 the randomized solver performs some pretty clever operations to reduce dimensionality even before the singular value decomposition is carried out. It first finds an orthogonal matrix Q such that multiplication of your data matrix by Q is approximately equal to your original data matrix (i.e. if your data matrix is called A, then the matrix norm ||A —Q Q*A|| is small). Q is chosen using a random Gaussian matrix — this is where the randomness is introduced.

In Scikit-learn, PCA is applied using the PCA() class. 
It is in the decomposition submodule in Scikit-learn. 
The most important hyperparameter in that class is n_components. 
It can take one of the following types of values.

•	**None:** This is the default value. If we do not specify the value, all components are kept. In our example, this exactly the same as n_components=30.

•	**int**: If this is a positive integer like 1, 2, 30, 100, etc, the algorithm will return that number of principal components. The integer value should be less than or equal to the original number of features in the dataset.

•	**float:** If 0 < n_components < 1, PCA will select the number of components such that the amount of variance that needs to be explained². For example, if n_components=0.95, the algorithm will select the number of components while preserving 95% of the variance in the data.
*

**When applying PCA, all you need to do is to create an instance of the PCA() class and fit it using the scaled values of X**

**Then apply the transformation**. 

***The variable X_pca_30 stores the transformed values of the principal components returned by the PCA() class. X_pca_30 is a 569x30 two-dimensional Numpy array. ***

We have not reduced the dimensionality, and therefore, the percentage of variance explained by 30 principal components should be 100%.
"""

print("Variance explained by all 30 principal components = ", sum(pca_30.explained_variance_ratio_ * 100))

"""**The explained_variance_ratio_ attribute of the PCA() class returns a one-dimensional numpy array which contains the values of the percentage of variance explained by each of the selected components.**"""

pca_30.explained_variance_ratio_*100

"""# **Explanation**

The first component alone captures about 44.27% of the variability in the dataset and the second component alone captures about 18.97% of the variability in the dataset and so on. Also, note that the values of the above array are sorted in descending order. Taking the sum of the above array will return the total variance explained by each of the selected components.

If we get the cumulative sum of the above array, we can see the following array.
"""

np.cumsum(pca_30.explained_variance_ratio_*100)

"""**Now we shall try for the plot**"""

plt.plot(np.cumsum(pca_30.explained_variance_ratio_))
plt.xlabel('Number of Component')
plt.ylabel('Explained Variance')
plt.savefig('Elbow_Plot.png',dpi=100)

"""# **Explanation**

We can see that the first 10 principal components keep about 95.1% of the variability in the dataset while reducing 20 (30–10) features in the dataset. That’s great. The remaining 20 features only contain less than 5% of the variability in data.

*   It is not possible to create a scatterplot for our breast_cancer dataset because it contains 30 features
*   Reducing the number of dimensions to two or three makes it possible to create a 2d scatterplot or 3d scatterplot which helps us to detect patterns such as clusters in our dataset.
*   Therefore, dimensionality reduction is extremely useful for data visualization.
*   But, keep in mind that, in our problem, if we create a 2d scatterplot using the first 2 principal components, it only explains about 63.24% of the variability in data and if we create a 3d scatterplot using the first 3 principal components, it only explains about 72.64% of the variability in data

**Apply PCA by setting n_components=2**

This will transform our original data onto a two-dimensional space. This will return 2 components that capture 63.24% of the variability in data as said earlier
"""

pca_2 = PCA(n_components=2, random_state=2020)
pca_2.fit(X_scaled)
X_pca_2 = pca_2.transform(X_scaled)

plt.figure(figsize=(10,7))
sns.scatterplot(x=X_pca_2[:,0], y=X_pca_2[:,1],s=70, hue=cancer.target,palette=['green', 'cyan'])
plt.title("2D Scatterplot:63.24% of variance captured",pad=15)
plt.xlabel("First Principal Component")
plt.ylabel("Second Principal Component")
plt.savefig("2D-scatterplot.png")

"""# **Another Visualization**

**Yellowbrick machine learning** is a visualization library. 

Using the PCA Visualizer (an object that learns from data to produce a visualization), we can create an even more informative 2d scatterplot with a just few lines of code.
"""

from yellowbrick.features import PCA
visualizer= PCA(scale=True, projection =2, classes =['malignant', 'benign'],random_state=2020, colors=['brown', 'blue'])
visualizer.fit_transform(X, cancer.target)
visualizer.show(outpath='2D_scatterplot_y.png')

"""## **Applying PCA by setting n_components=3**

**This will transform our original data onto a three-dimensional space. This will return 3 components that capture 72.64% of the variability in data **
"""

pca_3 = PCA(n_components=3, random_state=2020)
pca_3.fit(X_scaled)
X_pca_3 = pca_3.transform(X_scaled)

"""Now, we create a 3d scatterplot of the data using the values of the three principal components."""

from mpl_toolkits import mplot3d
fig = plt.figure(figsize = (12, 8))
ax = plt.axes(projection ='3d')
sctt = ax.scatter3D(X_pca_3[:,0], X_pca_3[:, 1], X_pca_3[:, 2], c=cancer.target, s=50, alpha=0.6) 
   # X_pca_3[:,0], X_pca_3[:,1], X_pca_3[:,2], c=cancer.target, s=50, alpha=0.6) 
plt.title('3D Scatterplot: 72.64% of the variability captured', pad=15)
ax.set_xlabel('First Principal Component')
ax.set_ylabel('Second Principal Component')
ax.set_xlabel('Third Principal Component')
plt.savefig('3d_scatterplot.png')

visualizer_3= PCA(scale=True, projection =3, classes =['malignant', 'benign'],random_state=2020, colors=['red', 'blue'])
visualizer_3.fit_transform(X, cancer.target)

"""# **Let’s apply PCA to our dataset with n_components=0.95.**

This will select the number of components while preserving 95% of the variability in the data
"""

pca_95 =PCA(n_components=0.95, random_state=2020)
pca_95.fit(X_scaled)
X_pca_95 = pca_95.transform(X_scaled)

X_pca_95.shape