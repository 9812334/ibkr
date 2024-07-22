import argparse

def main():
    parser = argparse.ArgumentParser(description='My Python Script')
    parser.add_argument('--option1', type=str, help='Option 1', default='Hello')
    parser.add_argument('--option2', type=int, help='Option 2', default=42)
    parser.add_argument('--option3', type=float, help='Option 3', default=3.14)
    parser.add_argument('--option4', type=bool, help='Option 4', default=False)

    args = parser.parse_args()

    print(f'Option 1: {args.option1}')
    print(f'Option 2: {args.option2}')
    print(f'Option 3: {args.option3}')
    print(f'Option 4: {args.option4}')

if __name__ == '__main__':
    main()