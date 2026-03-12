from pymongo import MongoClient
import numpy as np
import openai
openai.api_key = "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"

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["GRE_Practice"]

questions_collection = db["questions"]
session_collection = db["UserSession"]

print("Adaptive Test Started")

# Step 1: starting ability
ability = 0.5
user_id = "student101"
total_questions = 0
correct_answers = 0

def get_question(ability):
    # find question near ability level
    question = questions_collection.find_one({
        "difficulty": {"$gte": ability - 0.1, "$lte": ability + 0.1}
    })
    return question

def update_ability(ability, difficulty, correct):
    # IRT probability
    probability = 1 / (1 + np.exp(-(ability - difficulty)))

    result = 1 if correct else 0
    learning_rate = 0.1

    new_ability = ability + learning_rate * (result - probability)
    return new_ability

for i in range(10):

    print("\nCurrent ability:", round(ability,3))

    question = get_question(ability)

    print("Question:", question["question"])

    for opt in question["options"]:
        print("-", opt)

    answer = input("Your answer: ")

    correct = answer == question["correct_answer"]
    total_questions += 1

if correct:
    correct_answers += 1

    if correct:
        print("Correct!")
    else:
        print("Incorrect!")

    ability = update_ability(ability, question["difficulty"], correct)

    print("Updated ability:", round(ability,3))

    session_collection.update_one(
        {"user_id": user_id},
        {
            "$push": {
                "questions_attempted": {
                    "question_id": question["question_id"],
                    "selected_answer": answer,
                    "correct": correct
                }
            },
            "$set": {"current_ability": ability},
            "$inc": {"total_questions": 1,
                     "correct_answers": 1 if correct else 0}
        },
        upsert=True
    )

print("\nTest finished.")
prompt = f"""
Student Adaptive Test Performance

Ability Score: {ability}
Total Questions: {total_questions}
Correct Answers: {correct_answers}

Generate a short 3-step personalized study plan to help this student improve based on their weaknesses.
"""
print("\nPersonalized Study Plan:\n")

if ability < 0.4:
    print("1. Review basic arithmetic and algebra concepts.")
    print("2. Practice easy GRE quantitative questions.")
    print("3. Take another adaptive test focusing on fundamentals.")

elif ability < 0.7:
    print("1. Strengthen intermediate algebra and probability skills.")
    print("2. Practice medium difficulty GRE questions.")
    print("3. Focus on topics where mistakes occurred.")

else:
    print("1. Focus on advanced GRE quantitative problems.")
    print("2. Practice time management strategies.")
    print("3. Take full-length GRE mock tests.")
print("\nPersonalized Study Plan:\n")
print(study_plan)