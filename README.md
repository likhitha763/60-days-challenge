# Day 8: Arrays Through Real Data

This project focuses on arrays as one of the most important data structures in software.

## Problem

We create an array of simulated user activity numbers and count how many numbers have digits that are all even.

Example data:

```python
user_activity = [124, 48, 3, 22, 302, 77, 84, 19, 50, 246]
```

We then filter the list to keep only values whose digits are all even.

## How the code works

- The array stores multiple numbers in one place.
- We loop through each number.
- We split the number into digits.
- We check whether every digit is even.
- We collect the matches into a new list.

## Why arrays are important in real systems

Arrays are used everywhere in software systems:

- analytics dashboards store metrics in arrays
- logs and event streams are processed in batches
- user activity tracking keeps records in ordered lists
- machine learning pipelines often work with numeric arrays

Arrays make it easy to process many values efficiently and consistently.

## Output example

```text
Simulated user data:
[124, 48, 3, 22, 302, 77, 84, 19, 50, 246]

Numbers with only even digits:
[48, 22, 84, 50, 246]

Total matching numbers: 5
```

## GitHub repository

This project is ready to be pushed to GitHub:

```bash
git init
git add .
git commit -m "Add Day 8 arrays project"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## LinkedIn reflection

"Today I worked on arrays, one of the most important foundations of software engineering. Arrays let us store and process lots of related values together, which is exactly how real systems handle user data, logs, analytics, and activity tracking. This exercise helped me understand how simple data structures can support powerful real-world apps."

## File

- `day8_arrays_through_real_data.py` contains the working code.
