# 1D Adaptive Testing System

This project implements a 1-Dimensional Adaptive Testing System using Python and MongoDB.

The system dynamically selects questions based on a student's previous responses to estimate their proficiency level. The student's ability score is updated using an Item Response Theory (IRT) model.

After completing the test, the system generates a personalized study plan based on the student's performance.

---

## How to Run the Project

1. Install required libraries

pip install -r requirements.txt

2. Start MongoDB

Make sure MongoDB is running locally on port 27017.

3. Run the program

python adaptive_test.py

---

## Adaptive Algorithm Logic

The student begins with an ability score of 0.5.

If the student answers correctly, the ability score increases and the next question becomes harder.

If the student answers incorrectly, the ability score decreases and the next question becomes easier.

The ability score is updated using a simplified Item Response Theory (IRT) formula.

---

## AI Log

ChatGPT was used to assist in generating GRE-style questions, designing the MongoDB schema, and implementing the adaptive testing algorithm. AI also helped debug Python errors and dependency issues during development.

---

## API Documentation

GET /next-question
Returns the next adaptive question based on student ability.

POST /submit-answer
Submits the student's answer and updates ability score.

GET /study-plan
Generates a personalized study plan after the test ends.
