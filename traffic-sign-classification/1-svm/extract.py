import os
from argparse import ArgumentParser
from feature_extractor import extract_features_and_save

"""
code to run extract.py:
python3 extract.py --train_dir ../../Data/Train --test_dir ../../Data/Test
"""

def main(args):
    reducedDir = ['i4', 'pl30', 'pl80', 'w57']
    if args.train_dir:
        train_dirs = [os.path.join(args.train_dir, f) for f in os.listdir(args.train_dir)]
        train_files = []
        for subDir in train_dirs:
            if args.reduced and subDir.split('\\')[-1] in reducedDir:
                for file in os.listdir(subDir):
                    train_files.append(os.path.join(subDir, file))
        extract_features_and_save(train_files, os.path.join(args.output_dir, 'train'))

    if args.test_dir:
        test_files = os.listdir(args.test_dir)
        test_files = [os.path.join(args.test_dir, f) for f in test_files]
        extract_features_and_save(test_files, os.path.join(args.output_dir, 'test'))


if __name__ == '__main__':
    outputDir = os.path.split(os.getcwd())[0] + r"\1-svm\Features\Reduced Features"
    trainDataDir = os.path.dirname(os.path.split(os.getcwd())[0]) + r"\Data\Train"
    testDataDir = os.path.dirname(os.path.split(os.getcwd())[0]) + r"\Data\Test"

    parser = ArgumentParser()
    parser.add_argument('--train_dir', type=str)
    parser.add_argument('--test_dir', type=str)
    parser.add_argument('--output_dir', type=str, default='./features/')
    parser.add_argument('--reduced', action='store_false')
    # args = parser.parse_args()
    args = parser.parse_args(['--train_dir', trainDataDir,
                              '--test_dir', testDataDir,
                              '--output_dir', outputDir])
                              # '--reduced', True])
    main(args)
