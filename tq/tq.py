NUM_QUESTIONS = 20

def main():
    win = False
    for i in range(NUM_QUESTIONS):
        try:
            response = raw_input('Is it a thing? ')
        except EOFError:
            print('\n\nBye!')
            return

        if response == 'yes':
            win = True
            break
    if win:
        print('I win!')
    else:
        print("You win! But I'm not happy about it...")
