import random

# Constants for file handling
WORD_LIST_PATH = "assets/words_alpha.txt"

# Global variables to store all loaded words
MASTER_WORD_LIST = []


def load_words():
    """
    Reads the dictionary file and stores all words in a list.
    Returns True if successful, False otherwise.
    """
    print("Loading words...")
    try:
        with open(WORD_LIST_PATH, "r") as file:
            # Read every line, strip whitespace, and make uppercase
            for line in file:
                word = line.strip().upper()
                # Only store words made of letters (avoids empty lines or numbers)
                if word.isalpha():
                    MASTER_WORD_LIST.append(word)

        if not MASTER_WORD_LIST:
            print(f"[!] Error: No words found in {WORD_LIST_PATH}.")
            return False

        print(f"Dictionary loaded successfully ({len(MASTER_WORD_LIST)} words).")
        return True

    except FileNotFoundError:
        print(f"[!] Error! File not found at: {WORD_LIST_PATH}")
        print("[!] Please ensure the 'assets' folder and text file exist.")
        return False


def select_difficulty():
    """
    Allows the user to choose a difficulty level.
    Returns a tuple: (word_length, max_tries)
    """
    print("\n--- Select Difficulty ---")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Custom")

    while True:
        choice = input("Enter choice (1-4): ").strip()

        if choice == '1':
            return 4, 8
        elif choice == '2':
            return 5, 6
        elif choice == '3':
            return 6, 5
        elif choice == '4':
            # Custom difficulty
            try:
                l = int(input("Enter desired word length (3-10): "))
                t = int(input("Enter number of tries (1-20): "))
                if 3 <= l <= 10 and 1 <= t <= 20:
                    return l, t
                else:
                    print("Invalid numbers. Keeping default bounds.")
            except ValueError:
                print("Please enter valid numbers.")
        else:
            print("Invalid selection. Please try again.")


def filter_words(length):
    """
    Creates a list of words that match the specific game length.
    """
    filtered = [w for w in MASTER_WORD_LIST if len(w) == length]
    return filtered


def get_feedback(guess, target_word):
    """
    Compares the guess to the target word.
    Returns a list of strings (Chophy, Storts, Bascat).
    """
    length = len(target_word)
    feedback = ["Bascat"] * length

    # Convert target to a list of characters to handle duplicates safely
    # We use a frequency map or a temporary list to track available letters
    target_temp = list(target_word)

    # PASS 1: Check for "Chophy" (Correct letter, Correct spot)
    for i in range(length):
        if guess[i] == target_word[i]:
            feedback[i] = "Chophy"
            # Remove the letter from target_temp so it can't be used for a Storts later
            target_temp[i] = None

            # PASS 2: Check for "Storts" (Correct letter, Wrong spot)
    for i in range(length):
        # Only check if we haven't already marked it as Chophy
        if feedback[i] != "Chophy":
            if guess[i] in target_temp:
                feedback[i] = "Storts"
                # Remove the FIRST occurrence of this letter from temp to prevent double counting
                target_temp[target_temp.index(guess[i])] = None

    return feedback


def main():
    print("Welcome to Storts, Chophy, Bascat!")

    # 1. Load words once at the start
    if not load_words():
        return

    play_again = True

    while play_again:
        # 2. Set Difficulty
        word_len, max_tries = select_difficulty()

        # 3. Get words for this specific length
        game_words = filter_words(word_len)
        if not game_words:
            print(f"[!] No words found with length {word_len}. Please pick a different difficulty.")
            continue

        # 4. Select Target Word
        target_word = random.choice(game_words)
        tries_left = max_tries
        game_over = False

        print(f"\n--- New Game Started ---")
        print(f"Guessing a {word_len}-letter word. You have {max_tries} tries.")

        # 5. Game Loop
        while not game_over:
            print(f"\n[Tries left: {tries_left}]")
            guess = input("Guess: ").strip().upper()

            # Validation 1: Length
            if len(guess) != word_len:
                print(f"[!] Invalid length. Your guess must be {word_len} letters long.")
                continue

            # Validation 2: Is it a real word? (Extra Credit)
            if guess not in MASTER_WORD_LIST:
                print(f"[!] '{guess}' is not in the dictionary list.")
                continue

            # Win Condition
            if guess == target_word:
                print(f"\n*** You got it! ***")
                print(f"The word was: {target_word}")
                print("Result: WIN")
                game_over = True

            else:
                tries_left -= 1
                feedback = get_feedback(guess, target_word)

                print("Feedback:")
                # Display nicely formatted feedback
                for i in range(word_len):
                    print(f" {guess[i]} : {feedback[i]}")

            # Loss Condition
            if tries_left == 0 and not game_over:
                print(f"\n--- You're out of tries! ---")
                print(f"The correct word was: {target_word}")
                print("Result: LOSS")
                game_over = True

        # 6. Play Again Loop
        while True:
            user_choice = input("\nPlay Again? (Y/N): ").strip().upper()
            if user_choice == 'Y':
                break  # Breaks the small loop, goes back to top of big loop
            elif user_choice == 'N':
                print("Thanks for playing!")
                play_again = False  # Stops the big loop
                break
            else:
                print("Please enter 'Y' or 'N'.")


if __name__ == "__main__":
    main()
