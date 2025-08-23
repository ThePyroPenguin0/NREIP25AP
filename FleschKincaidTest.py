import re
import sys

def syllables(word): # My grasp of linguistics isn't the best (certainly not English) so take feel free to modify.
    word = word.lower()
    syllable_count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith("e"):
        syllable_count -= 1
    if syllable_count == 0:
        syllable_count = 1
    return syllable_count

def flesch_kincaid_test(text): # Currently returns the Flesch-Kincaid Grade (0-100, with 0 being hardest and 100 being easiest) of a line.
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    num_sentences = len(sentences)
    words = re.findall(r'\w+', text)
    num_words = len(words)
    num_syllables = sum(syllables(word) for word in words)
    if num_sentences == 0 or num_words == 0:
        return 0
    return 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)

def test_avg(text_lines): # Averages the Flesch-Kincaid Grade of a list of lines.
    scores = [flesch_kincaid_test(line) for line in text_lines if line.strip()]
    if not scores:
        return 0
    return sum(scores) / len(scores)

if __name__ == "__main__":
    # Usage: python OpenResponseAnalysis.py <filename> -w(hole document) || -l(ine breakdown)
    if len(sys.argv) < 3 or sys.argv[2] not in ("-w", "-l"):
        print("Usage: python FleschKincaidTest.py <filename> -w|-l") # Provide either the filename (if in the same directory), relative path, or absolute path.
        sys.exit(1)

    filename = sys.argv[1]
    mode = sys.argv[2]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        if mode == "-w":
            score = flesch_kincaid_test(content)
            print(f"Whole Document Flesch-Kincaid Grade Level: {score:.2f}")
        elif mode == "-l":
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            avg_score = test_avg(lines)
            print(f"Average Flesch-Kincaid Grade Level (by line): {avg_score:.2f}")
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")