import math

from collections import defaultdict

# Calculate arithmetic mean of list of numbers
def mean(nums):
    return sum(nums) / float(len(nums))

# Calculate standard deviation of a list of numbers.
# Setting bessel to True enables Bessel's Correction in the calculation, useful
# when calculating standard deviation for a sample of a population, rather than
# the entire population.
# See Bessel's Correction (http://en.wikipedia.org/wiki/Bessel%27s_correction)
def standardDeviation(nums, bessel = False):
    average = mean(nums)

    squaredDifferenceFromMean = [(num - average) ** 2 for num in nums]

    denominator = len(nums)
    if bessel:
            denominator -= 1

    return math.sqrt(sum(squaredDifferenceFromMean) / float(denominator))

# Calculate number of buckets to use in a histogram using Sturges' Rule,
# given the number of elements in the data. Sturges' Rule assumes the data
# is an approximate normal distribution.
def sturgesRuleBuckets(sizeOfData):
    return int(math.ceil(1 + (math.log(sizeOfData, 10) / math.log(2, 10))))

def sturgesRuleBucketRange(nums):
    return (max(nums) - min(nums)) / float(sturgesRuleBuckets(len(nums)))

def standardScores(nums):
    average = mean(nums)
    stdDev = standardDeviation(nums)
    return [(num - average) / stdDev for num in nums]

def deviationScores(nums, newMean = 50, newStdDev = 10):
    standardScores = standardScores(nums)
    return [standardScore * newStdDev + newMean for standardScore in standardScores]

# Calculate the correlation coefficient for a set of (x,y) pairs.
def correlationCoefficient(pairs):
    xs, ys = zip(*pairs)
    meanX = mean(xs)
    meanY = mean(ys)

    xDiffs = [(x - meanX) for x in xs]
    yDiffs = [(y - meanY) for y in ys]

    print zip(xDiffs, yDiffs)

    sumOfXDiffSquares = sum([xDiff ** 2 for xDiff in xDiffs])
    sumOfYDiffSquares = sum([yDiff ** 2 for yDiff in yDiffs])

    print sumOfXDiffSquares
    print sumOfYDiffSquares

    numerator = sum([pair[0] * pair[1] for pair in zip(xDiffs, yDiffs)])
    denominator = math.sqrt(sumOfXDiffSquares * sumOfYDiffSquares)

    print numerator
    print denominator

    return numerator / float(denominator)

# Calculate the correlation ratio for a set of pairs. Each pair should
# consist of a tuple, with the first element being the numerical
# data and the second element being the categorical data.
def correlationRatio(pairs):
    # Group data by categories by creating a map of category to list of values

    categoryToValues = defaultdict(list)
    for value, category in pairs:
        categoryToValues[category].append(value)

    # Calcuate intraclass variance, and also sum, count, and mean of all values in
    # while we're at it to save a loop.

    categoryData = dict()

    allValuesSum = 0
    allValuesCount = 0

    intraclassVariance = 0

    for category, values in categoryToValues.items():

        categoryData[category] = dict()
        categoryData[category]['count'] = len(values)
        categoryData[category]['mean'] = mean(values)
        categoryData[category]['meanDiffSquared'] = \
            [(value - categoryData[category]['mean']) ** 2 for value in values]

        print category + ": " + str(categoryData[category]['meanDiffSquared'])

        intraclassVariance += sum(categoryData[category]['meanDiffSquared'])

        allValuesSum += sum(values)
        allValuesCount += len(values)

    allValuesMean = allValuesSum / float(allValuesCount)

    # Calculate interclass variance

    interclassVariance = 0
    for category, values in categoryToValues.items():
        interclassVariance += categoryData[category]['count'] * ((categoryData[category]['mean'] - allValuesMean) ** 2)

    # Calculate the correlation ratio

    return float(interclassVariance) / (intraclassVariance + interclassVariance)


pairs = [
    (23, 'theremes'),
    (26, 'theremes'),
    (27, 'theremes'),
    (28, 'theremes'),
    (25, 'channelior'),
    (26, 'channelior'),
    (29, 'channelior'),
    (32, 'channelior'),
    (33, 'channelior'),
    (15, 'bureperry'),
    (16, 'bureperry'),
    (18, 'bureperry'),
    (22, 'bureperry'),
    (26, 'bureperry'),
    (29, 'bureperry')]

print correlationRatio(pairs)
