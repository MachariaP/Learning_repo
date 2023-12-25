#!/usr/bin/env python3
'''
    - standard indentation is 4 space
    - implicit continuation - you can divide statements after parentheses,
      brackets and braces and before or after operators like '+' and '-'
    - explicit continuation - use the '\' character to divide statements
      anywhere on a line
'''
# Python code for a Test Scores Program

counter = 0
score_total = 0
test_score = 0
exit_condition = 7

while counter < exit_condition:
    test_score = int(input("Enter test score: "))
    if test_score >= 0 and test_score <= 100:
        score_total += test_score
        counter += 1

average_score = round(score_total / counter)

print("Total Score: " + str(score_total))
print("Average Score: " + str(average_score))

# Two ways to continue one statement over two or more lines
# 1. Implicit continuation
print("Total Score: " + str(score_total)
        + "\nAverage Score: " + str(average_score))

# 2. Explicit continuation
print("Total Score: " + str(score_total) \
        + "\nAverage Score: " + str(average_score))
