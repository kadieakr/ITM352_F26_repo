# Program to remove any scores from a list that are below 50.
 
from unittest import result


scores = [60, 45, 30, 85, 10, 90] 

scores = [score for score in scores if score >= 50]

print(scores)
