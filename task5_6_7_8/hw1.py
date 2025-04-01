import re
import string
from collections import Counter
from typing import List

def get_longest_diverse_words(file_path: str) -> List[str]:
    """
    Reads the file and returns a list of 10 words that have the largest number 
    of unique characters. The words are normalized to lower-case and duplicates 
    are removed. They are sorted primarily by the count of unique symbols (descending),
    then by word length (descending), then lexicographically.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        List[str]: A list of up to 10 words meeting the criteria.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Extract words (a word is defined as a sequence of alphanumeric characters and underscores)
    words = re.findall(r'\b\w+\b', text)
    # Normalize to lower-case and remove duplicates
    unique_words = set(word.lower() for word in words)
    # Sort by: (1) unique char count (desc), (2) length (desc), (3) alphabetical order
    sorted_words = sorted(unique_words, key=lambda w: (-len(set(w)), -len(w), w))
    return sorted_words[:10]

def get_rarest_char(file_path: str) -> str:
    """
    Finds and returns the character that appears least frequently in the document.
    In case of ties, the character with the smallest Unicode code point is returned.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        str: The rarest character.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    if not text:
        return ""
    counts = Counter(text)
    # Choose the character with the minimal count; if tied, the one with smallest ord value.
    rarest = min(counts.items(), key=lambda x: (x[1], ord(x[0])))
    return rarest[0]

def count_punctuation_chars(file_path: str) -> int:
    """
    Counts every punctuation character in the file.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        int: The total number of punctuation characters.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return sum(1 for ch in text if ch in string.punctuation)

def count_non_ascii_chars(file_path: str) -> int:
    """
    Counts every non-ASCII character in the file.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        int: The total number of non-ASCII characters.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return sum(1 for ch in text if ord(ch) > 127)

def get_most_common_non_ascii_char(file_path: str) -> str:
    """
    Finds the most common non-ASCII character in the document.
    In case of ties, the character with the smallest Unicode code point is returned.
    If there are no non-ASCII characters, returns an empty string.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        str: The most common non-ASCII character.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Filter out only non-ASCII characters.
    non_ascii = [ch for ch in text if ord(ch) > 127]
    if not non_ascii:
        return ""
    counts = Counter(non_ascii)
    # max() with key: first by count then by negative ord value so that in ties the smallest ord wins.
    most_common = max(counts.items(), key=lambda x: (x[1], -ord(x[0])))
    return most_common[0]

# Example usage:
if __name__ == "__main__":
    file_path = "data.txt"  # Adjust path if necessary

    longest_words = get_longest_diverse_words(file_path)
    print("10 longest diverse words:")
    for word in longest_words:
        print(word)

    rarest = get_rarest_char(file_path)
    print("\nRarest character:", repr(rarest))

    punct_count = count_punctuation_chars(file_path)
    print("\nNumber of punctuation characters:", punct_count)

    non_ascii_count = count_non_ascii_chars(file_path)
    print("\nNumber of non-ASCII characters:", non_ascii_count)

    most_common_non_ascii = get_most_common_non_ascii_char(file_path)
    print("\nMost common non-ASCII character:", repr(most_common_non_ascii))
import re
import string
from collections import Counter
from typing import List

def get_longest_diverse_words(file_path: str) -> List[str]:
    """
    Reads the file and returns a list of 10 words that have the largest number 
    of unique characters. The words are normalized to lower-case and duplicates 
    are removed. They are sorted primarily by the count of unique symbols (descending),
    then by word length (descending), then lexicographically.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        List[str]: A list of up to 10 words meeting the criteria.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Extract words (a word is defined as a sequence of alphanumeric characters and underscores)
    words = re.findall(r'\b\w+\b', text)
    # Normalize to lower-case and remove duplicates
    unique_words = set(word.lower() for word in words)
    # Sort by: (1) unique char count (desc), (2) length (desc), (3) alphabetical order
    sorted_words = sorted(unique_words, key=lambda w: (-len(set(w)), -len(w), w))
    return sorted_words[:10]

def get_rarest_char(file_path: str) -> str:
    """
    Finds and returns the character that appears least frequently in the document.
    In case of ties, the character with the smallest Unicode code point is returned.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        str: The rarest character.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    if not text:
        return ""
    counts = Counter(text)
    # Choose the character with the minimal count; if tied, the one with smallest ord value.
    rarest = min(counts.items(), key=lambda x: (x[1], ord(x[0])))
    return rarest[0]

def count_punctuation_chars(file_path: str) -> int:
    """
    Counts every punctuation character in the file.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        int: The total number of punctuation characters.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return sum(1 for ch in text if ch in string.punctuation)

def count_non_ascii_chars(file_path: str) -> int:
    """
    Counts every non-ASCII character in the file.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        int: The total number of non-ASCII characters.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return sum(1 for ch in text if ord(ch) > 127)

def get_most_common_non_ascii_char(file_path: str) -> str:
    """
    Finds the most common non-ASCII character in the document.
    In case of ties, the character with the smallest Unicode code point is returned.
    If there are no non-ASCII characters, returns an empty string.
    
    Args:
        file_path (str): Path to the text file.
    
    Returns:
        str: The most common non-ASCII character.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Filter out only non-ASCII characters.
    non_ascii = [ch for ch in text if ord(ch) > 127]
    if not non_ascii:
        return ""
    counts = Counter(non_ascii)
    # max() with key: first by count then by negative ord value so that in ties the smallest ord wins.
    most_common = max(counts.items(), key=lambda x: (x[1], -ord(x[0])))
    return most_common[0]

# Example usage:
if __name__ == "__main__":
    file_path = "data.txt"  # Adjust path if necessary

    longest_words = get_longest_diverse_words(file_path)
    print("10 longest diverse words:")
    for word in longest_words:
        print(word)

    rarest = get_rarest_char(file_path)
    print("\nRarest character:", repr(rarest))

    punct_count = count_punctuation_chars(file_path)
    print("\nNumber of punctuation characters:", punct_count)

    non_ascii_count = count_non_ascii_chars(file_path)
    print("\nNumber of non-ASCII characters:", non_ascii_count)

    most_common_non_ascii = get_most_common_non_ascii_char(file_path)
    print("\nMost common non-ASCII character:", repr(most_common_non_ascii))
