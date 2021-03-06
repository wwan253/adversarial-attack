import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import art.attacks.evasion

from art.estimators.classification import SklearnClassifier
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def visualize_classifier(model, X, y, ax=None, cmap='rainbow'):
    ax = ax or plt.gca()

    ax.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=cmap,
               clim=(y.min(), y.max()), zorder=3)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    xx, yy = np.meshgrid(np.linspace(*xlim, num=200),
                         np.linspace(*ylim, num=200))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    # Create a color plot with the results
    n_classes = len(np.unique(y))
    contours = ax.contourf(xx, yy, Z, alpha=0.3,
                           levels=np.arange(n_classes + 1) - 0.5,
                           cmap=cmap, zorder=1)

    ax.set(xlim=xlim, ylim=ylim)


# %matplotlib inline
plt.rcParams['figure.figsize'] = [8, 8]

random_state = 0

# Random_state: Determines random number generation for dataset creation. Pass an int for reproducible output across multiple function calls.
# Cluster_std: The standard deviation of the clusters.
# Xarray of shape [n_samples, n_features]: The generated samples.
# yarray of shape [n_samples]: The integer labels for cluster membership of each sample.
X, y = make_blobs(n_samples=600, n_features=2, centers=2,
                  random_state=random_state, cluster_std=1.0)

# scaling to [-1, 1] range
X_max = np.max(X, axis=0)
X_min = np.min(X, axis=0)

# This normalizes the sample to -1 to 1
X = 1 - 2 * (X - X_min) / (X_max - X_min)

# split into train test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

plt.figure()
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=50, cmap='rainbow')
# plt.show()

# To build a support vector machine model with radial basis function (rbf) kernal
model = SVC(kernel='rbf')
model.fit(X_train, y_train)


# visualize_classifier(model, X_test, y_test)
model_score = model.score(X_test, y_test)
print('Model Score:', model_score)

# SklearnClassifier = art.estimators.classification.SklearnClassifier
# TODO Question: why is the clip_values using the old min max of samples (X) ?  Wasn't it normalized to -1 and 1?
# classifier = SklearnClassifier(model=model, clip_values=(X_min, X_max))
classifier = SklearnClassifier(model=model, clip_values=(-1, 1))

predictions = classifier.predict(X_test)  # one-hot encoding
print('Prediction shape:', predictions.shape)

# eps is the attack step size
fgsm_attack = art.attacks.evasion.FastGradientMethod(estimator=classifier, eps=0.2)
# Generate adversarial samples and return them in an array.
fgsm_sample = fgsm_attack.generate(x=X_test)
fgsm_predictions = np.argmax(classifier.predict(fgsm_sample), axis=1)

# The accuracy is calculated by, for ones that accurately predicted the sample category, sum them up and divided by total # of samples
# This compares the FGSM accuracy with normal predictions
fgsm_delta = 1 - np.sum(fgsm_predictions == model.predict(X_test)) / len(y_test)
# This compares the FGSM accuracy with ground truth
fgsm_acc_truth = np.sum(fgsm_predictions == y_test) / len(y_test)
visualize_classifier(model, fgsm_sample, y_test)
print('The original model test accuray is', "{:.2%}".format(model_score),
      ', FGSM decreased it to', "{:.2%}".format(fgsm_acc_truth),
      ', FGSM delta is:', "{:.2%}".format(fgsm_delta))


# boundary_attack = art.attacks.evasion.BoundaryAttack(estimator=classifier, targeted=False, max_iter=1000, num_trial=20)
# boundary_sample = boundary_attack.generate(x=X_test)
# boundary_predictions = np.argmax(classifier.predict(boundary_sample), axis=1)
# # This compares the boundary accuracy with normal predictions
# boundary_delta = 1 - np.sum(boundary_predictions == model.predict(X_test)) / len(y_test)
# # This compares the boundary accuracy with ground truth
# boundary_acc_truth = np.sum(boundary_predictions == y_test) / len(y_test)
# visualize_classifier(model, boundary_sample, y_test)
# print('The original model test accuray is', "{:.2%}".format(model_score),
#       ', Boundary decreased it to', "{:.2%}".format(boundary_acc_truth),
#       ', Boundary delta is:', "{:.2%}".format(boundary_delta))


# simBA_attack = art.attacks.evasion.SimBA(classifier=classifier, attack='dct', max_iter=1000, order='random', targeted=False)
simBA_attack = art.attacks.evasion.ZooAttack(classifier=classifier, max_iter=1000)
simBA_sample = simBA_attack.generate(x=X_test)
simBA_predictions = np.argmax(classifier.predict(simBA_sample), axis=1)
simBA_delta = 1 - np.sum(simBA_predictions == model.predict(X_test)) / len(y_test)
# This compares the FGSM accuracy with ground truth
simBA_acc_truth = np.sum(simBA_predictions == y_test) / len(y_test)
visualize_classifier(model, simBA_sample, y_test)
print('The original model test accuray is', "{:.2%}".format(model_score),
      ', simBA decreased it to', "{:.2%}".format(simBA_acc_truth),
      ', simBA delta is:', "{:.2%}".format(simBA_delta))
print('lol')
