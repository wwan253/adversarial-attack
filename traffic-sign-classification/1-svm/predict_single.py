import joblib
import numpy as np
import os
from argparse import ArgumentParser
from feature_extractor import extract_features
from sklearn.multiclass import OneVsRestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA


def main(args):
    labels = ['i2', 'i4', 'i5', 'io', 'ip', 'p11', 'p23', 'p26', 'p5', 'pl30',
              'pl40', 'pl5', 'pl50', 'pl60', 'pl80', 'pn', 'pne', 'po', 'w57']
    lda: LinearDiscriminantAnalysis = joblib.load(os.path.join(args.model_dir, 'lda.model'))
    # pca: PCA = joblib.load(os.path.join(args.model_dir, 'pca.model'))
    classifier: OneVsRestClassifier = joblib.load(os.path.join(args.model_dir, 'svm.model'))
    test_file = [args.test_file]
    feat_intensity, feat_phog, feat_hog1, feat_hog2, feat_hog3 = extract_features(test_file)
    X_test_raw = np.hstack((feat_intensity, feat_phog, feat_hog1, feat_hog2, feat_hog3))
    X_test = lda.transform(X_test_raw)
    del X_test_raw
    X_test_n = normalize(X_test)

    y_predict = classifier.predict(X_test_n)
    print('The prediction for ' + args.test_file + ' is: ' + labels[y_predict[0]])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--test_file', type=str, required=True)
    parser.add_argument('--model_dir', type=str, required=True)
    args = parser.parse_args()

    main(args)
