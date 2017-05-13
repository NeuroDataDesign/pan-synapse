def epsilonDifference(num1, num2, threshold=.0001):
    if abs(num1 - num2) < threshold:
        return True
    return False
