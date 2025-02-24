#Author: Adam Laboissonniere (laboissa@bc.edu)
import os
import random

def load_flashcards(filename):
    """Load flashcards from a text file."""
    flashcards = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if '%' in line:
                    front, back = line.strip().split('%', 1)
                    flashcards[front.strip()] = back.strip()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' could not be found. Please check the file path.")
    return flashcards

def create_deck():
    """Create a new flashcard deck and save it to a file."""
    decks = [file for file in os.listdir() if file.endswith('.txt')]
    while True:
        filename = input("Enter the name for the new deck file (e.g., 'new_deck.txt'): ")
        if filename in decks:
            print(f"Error. There is already a deck with the name {filename}")
        else:
            break
    flashcards = {}
    while True:
        front = input("Enter the front of the flashcard (or type 'quit' to stop): ").strip()
        if front.lower() == "quit":
            break
        back = input("Enter the back of the flashcard: ").strip()
        flashcards[front] = back
        more = input("Would you like to add another flashcard? (yes/no): ").strip().lower()
        if more != "yes":
            break

    # Saves the flashcards to a new file
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for front, back in flashcards.items():
                file.write(f"{front} % {back}\n")
        print(f"Deck saved to {filename}")
    except Exception as e:
        print(f"Error saving the deck: {e}")
    return filename, flashcards

def quiz_user(flashcards):
    """Quiz the user on the flashcards."""
    n = 0
    i = 0
    total_terms = list(flashcards.keys())
    deck_length = len(total_terms)
    print("Flashcard Quiz: If given the term, write the correct definition, and if given the definition, write the correct term.")
    print("Type 'quit' to stop at any time.\n")
    while True:
        try:
            n = int(input(f"Enter the number of cards to be quizzed on. Total number is {deck_length}: "))
            if n <= deck_length and n > 0:
                break
            print(f"Please enter a number less than or equal to {deck_length}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    terms = list(flashcards.keys())
    random.shuffle(terms)
    terms = terms[:n]
    correct = 0
    incorrect = 0
    user_quit = False
    for term in terms:
        while i < n:
            term = terms.pop(0)
            if random.choice([True, False]):  # Randomly decides which side to show
                prompt, answer = term, flashcards[term]
                print(f"Term: {prompt}")
            else:
                prompt, answer = flashcards[term], term
                print(f"Definition: {prompt}")
            
            user_input = input("Your answer: ").strip()
            if user_input.lower() == "quit":
                user_quit = True
                break
            if user_input.lower() == answer.lower():
                print("Correct!\n")
                correct += 1
            else:
                print(f"Incorrect. The correct answer was: {answer}\n")
                incorrect += 1
                terms.append(term) # If answered incorrectly, the program keeps the card in the deck for further practive
                i -= 1
            i += 1
        if user_quit:
            break
    print(f"Number answered correctly: {correct}")
    print(f"Number answered incorrectly: {incorrect}\n")

def list_decks():
    """List all the .txt flashcard decks in the current directory."""
    decks = [file for file in os.listdir() if file.endswith('.txt')]
    if not decks:
        print("No flashcard decks found.")
        return None
    print("Available flashcard decks:")
    for idx, deck in enumerate(decks, 1):
        print(f"{idx}. {deck}")
    return decks

def main():
    print("Welcome to this flashcard program")
    while True:
        print(f"Type the number of the option you would like to choose. To quit the program, type '0'.\n[1] Quiz Deck\n[2] Change Deck\n[3] Create Deck\n")
        choice = 0
        viable_options = [0, 1, 2, 3]
        while True:
            try:
                choice = int(input(""))
                if choice in viable_options:
                    break
                print("Please enter a viable option.")
            except ValueError:
                print("Please enter a viable option.")
        if choice == 0:
            break
        elif choice == 1:
            list_decks()
            filename = input("Enter the flashcard file name: ")
            flashcards = load_flashcards(filename)
            if not flashcards:
                print("No flashcards found. Make sure the file is formatted correctly.")
                return
            quiz_user(flashcards)
        elif choice == 2:
            list_decks()
            filename = input("Enter the flashcard file name: ")
            flashcards = load_flashcards(filename)
        elif choice == 3:
            filename, flashcards = create_deck()

if __name__ == "__main__":
    main()
