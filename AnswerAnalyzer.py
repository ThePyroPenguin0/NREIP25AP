import re
from collections import Counter

def format_questions(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    new_content = re.sub(r'^(\d+)\)', r'\1.', content, flags=re.MULTILINE)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def read_quiz(file_path):
    correct_answers = []
    incorrect_answers = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if re.match(r'^\d+\.', lines[i].strip()):
                for j in range(i + 1, min(i + 5, len(lines))):
                    answer_line = lines[j].strip()
                    if re.match(r'^[a-d]\)', answer_line):
                        if '*' in answer_line:
                            correct_answers.append(answer_line)
                        else:
                            incorrect_answers.append(answer_line)
                i += 5
            else:
                i += 1
    return correct_answers, incorrect_answers

def answer_start_proportions(answer_list):
    from collections import Counter
    starts = [ans[0].lower() for ans in answer_list if ans and ans[0].lower() in 'abcd']
    total = len(starts)
    counts = Counter(starts)
    for letter in 'abcd':
        proportion = counts[letter] / total if total > 0 else 0
        print(f"{letter}): {proportion:.2%} ({counts[letter]}/{total})")

def answer_length(list1, list2):
    def avg_length(lst):
        return sum(len(s) for s in lst) / len(lst) if lst else 0
    
    avg1 = avg_length(list1)
    avg2 = avg_length(list2)
    print(f"Average length of correct answers: {avg1:.2f}")
    print(f"Average length of incorrect answers: {avg2:.2f}")
    print(f"Length ratio of correct to incorrect answers: {avg1/avg2:.1f}:1")

def print_word_frequencies(entries, word):
    total_instances = 0;
    pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
    for idx, entry in enumerate(entries):
        count = len(pattern.findall(entry))
        total_instances += count   
    frequency = (total_instances / len(entries)) if entries else 0
    print(f"The word '{word}' appears {total_instances} time(s) with a {100*frequency:.2f}% chance of appearing in any answer in this list.")
    return frequency

def get_keyword_frequency(answers_list, min_length=5, top_n=15):
    text = ' '.join(answers_list).lower()
    words = re.findall(r'\b[a-zA-Z]{%d,}\b' % min_length, text) # I hate RegEx I hate RegEx I hate RegEx
    common = Counter(words).most_common(top_n)
    return [word for word, _ in common]

def main():
    filepath = r'C:\Users\glipo\Documents\GitHub\NREIP25AP\ExperimentLogs\Cogito\cogito_rag_5.txt'
    # format_questions(filepath)
    correct_answers_list, incorrect_answers_list = read_quiz(filepath)

    print("\nProportion of correct answers starting with each letter:")
    answer_start_proportions(correct_answers_list)
    print("\nProportion of incorrect answers starting with each letter:")
    answer_start_proportions(incorrect_answers_list)
    print("\n")
    answer_length(correct_answers_list, incorrect_answers_list)
    print("\n")

    # Static list of keywords formerly used, now dynamically generated
    # keywords = ['ai', 'agent', 'system', 'systems', 'information', 'language', 'environment', 'all of the above', 'none of the above', 'reasoning', 'knowledge', 'represenation', 'expert', 'algorithm', 'algorithms']
    keywords = get_keyword_frequency(correct_answers_list, min_length=5, top_n=30)
    keywords.append('all of the above')
    keywords.append('none of the above')
    for word in keywords:
        correct_frequency = print_word_frequencies(correct_answers_list, word)
        incorrect_frequency = print_word_frequencies(incorrect_answers_list, word)
        if incorrect_frequency != 0:
            percent_more_likely = (correct_frequency / incorrect_frequency) * 100
            print(f'The word "{word}" is {percent_more_likely:.2f}% as likely to appear in correct answers compared to incorrect answers.\n')
        elif(correct_frequency == 0):
            print(f'The word "{word}" is not present in the correct answers list.\n')
        else:
            print(f'Any answer with "{word}" will always be correct.\n')

main()