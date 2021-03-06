from PIL import Image
from RGBAImage import *
import math
import statistics
from os import walk
import os
import matplotlib.pyplot as plt

#will need to get data and change the directory for accessing dataset

def getPixelInfo(image_path):

  im = Image.open(image_path)
  pixel_values = list(im.getdata())

  image = RGBAImage(pixel_values)
  image.setAll()
  maxPixelValues = image.getMaxRGBA()
  minPixelValues = image.getMinRGBA()
  meanPixelValue = image.getMeanRGBA()
  
  #print ({'Maximum Pixel Values': maxPixelValues, 'Minimum PixelValues': minPixelValues, 'Mean Pixel Values': meanPixelValue})
  return (maxPixelValues, minPixelValues, meanPixelValue)


def getAllPng(TrainOrTest):
  f = []
  for (dirpath, dirnames, filenames) in walk('./' + TrainOrTest):
    for filename in filenames:
      rel_dir = os.path.relpath(dirpath)
      rel_file = os.path.join(rel_dir, filename)
      f.append(rel_file)
  f = f[1:]
  # overallRedMax = []
  # overallGreenMax = []
  # overallBlueMax = []
  # overallRedMin = []
  # overallGreenMin = []
  # overallBlueMin = []
  overallRedMean = []
  overallGreenMean = []
  overallBlueMean = []
  for path in f:
    maximum, minimum, avg = getPixelInfo(path)
    # overallRedMax.append(maximum[0])
    # overallGreenMax.append(maximum[1])
    # overallBlueMax.append(maximum[2])
    # overallRedMin.append(minimum[0])
    # overallGreenMin.append(minimum[1])
    # overallBlueMin.append(minimum[2])
    overallRedMean.append(avg[0])
    overallGreenMean.append(avg[1])
    overallBlueMean.append(avg[2])
  # maxRed = max(overallRedMax)
  # maxGreen = max(overallGreenMax)
  # maxBlue = max(overallBlueMax)
  # minRed = min(overallRedMin)
  # minGreen = min(overallGreenMin)
  # minBlue = min(overallBlueMin)


  # return [[maxRed, maxGreen, maxBlue], [minRed, minGreen, minBlue], [meanRed, meanGreen, meanBlue]]
  return [overallRedMean, overallGreenMean, overallBlueMean]

def main():
  means = getAllPng('Test') #pass in Train or Test
  r = means[0]
  g = means[1]
  b = means[2]
  meanRed = statistics.mean(r)
  meanGreen = statistics.mean(g)
  meanBlue = statistics.mean(b)
  # plt.hist(r, bins = 'auto')
  # plt.xlabel('Colour Intensity')
  # plt.ylabel('Number of Pictures')
  # plt.title('Histogram of Average Red Pixel Value')
  # plt.show()
  # plt.hist(g, bins = 'auto')
  # plt.xlabel('Colour Intensity')
  # plt.ylabel('Number of Pictures')
  # plt.title('Histogram of Average Green Pixel Value')
  # plt.show()
  # plt.hist(b, bins = 'auto')
  # plt.xlabel('Colour Intensity')
  # plt.ylabel('Number of Pictures')
  # plt.title('Histogram of Average Blue Pixel Value')
  # plt.show()
  # all Test: 3799
  picCount = len(r)



  print('Number of Images in Test Data:', picCount)
  print('Mean Red Pixel Value:', round(meanRed, 2))
  print('Mean Green Pixel Value:', round(meanGreen, 2))
  print('Mean Blue Pixel Value:', round(meanBlue, 2))


main()

# x = [1,2 , 3]
# y = [2,3 , 4]
# plt.scatter(x, y, label='red', color='red', marker='1', s=30)
# plt.xlabel('x-axis')
# plt.ylabel('y-axis')
# plt.title('scatter graph')
# plt.legend()
# plt.show()
