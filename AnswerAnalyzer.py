import re

def read_quiz(file_path):
    correct_answers = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if re.match(r'^\d+\.', lines[i].strip()):
                for j in range(i + 1, min(i + 5, len(lines))):
                    answer_line = lines[j].strip()
                    if re.match(r'^[a-d]\)', answer_line) and '*' in answer_line:
                        correct_answers.append(answer_line)
                i += 5
            else:
                i += 1
    return correct_answers

def main():
    correct_answers_list = read_quiz(r'C:\Users\glipo\Documents\GitHub\NREIP25AP\chat-AI Multiple Choice Exam.txt')
    print("The correct answers are:")
    for answer in correct_answers_list:
        print(answer)

main()