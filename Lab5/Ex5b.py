sentence = input("Enter a sentence: ")

words = sentence.split()  # Split the sentence into words
words.reverse()

reversed_sentence = ' '.join(words)  # Join the reversed words back into a sentence
print("Reversed sentence:", reversed_sentence)
