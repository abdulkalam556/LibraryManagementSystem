import sys
import re
from red_black_tree import RedBlackTree

# this function executes the input file line by line
def execute_command(library, command_line):
    # Find the command and the arguments part of the command line
    match = re.match(r'(\w+)\((.*)\)', command_line.strip())
    if not match:
        return  # Invalid command format

    command = match.group(1)
    args_part = match.group(2)

    # Use regular expression to split arguments while considering quoted strings as reffernce
    args = re.findall(r'(?:[^,"]|"(?:\\.|[^"])*")+', args_part)

    # Clean and convert arguments
    cleaned_args = []
    for arg in args:
        arg = arg.strip()
        if arg[0] == '"' and arg[-1] == '"':  # It's a string argument
            cleaned_args.append(arg[1:-1])
        else:  # It's an integer argument
            cleaned_args.append(int(arg))


    if command == "PrintBook":
        # Call InsertBook function with appropriate arguments
        bookID = cleaned_args[0]
        library.print_book(book_id=bookID)
    elif command == "PrintBooks":
        # Call PrintBooks function
        bookID1 = cleaned_args[0]
        bookID2 = cleaned_args[1]
        library.print_books(book_id1=bookID1, book_id2=bookID2)
    elif command == "InsertBook":
        # Call InsertBook function
        bookID = cleaned_args[0]
        bookName = cleaned_args[1]
        authorName = cleaned_args[2]
        availabilityStatus = cleaned_args[3]
        library.insert_book(book_id=bookID, book_name=bookName, author_name=authorName, availability_status=availabilityStatus)
    elif command == "BorrowBook":
        # Call BorrowBook function
        patronID = cleaned_args[0]
        bookID = cleaned_args[1]
        patronPriority = cleaned_args[2]
        library.borrow_book(patron_id=patronID, book_id=bookID, patron_priority=patronPriority)
    elif command == "ReturnBook":
        # Call ReturnBook function
        patronID = cleaned_args[0]
        bookID = cleaned_args[1]
        library.return_book(patron_id=patronID, book_id=bookID)
    elif command == "DeleteBook":
        # Call DeleteBook function
        bookID = cleaned_args[0]
        library.delete_book(book_id=bookID)
    elif command == "FindClosestBook":
        # Call FindClosestBook function
        targetID = cleaned_args[0]
        library.find_closest_book(target_id=targetID)
    elif command == "ColorFlipCount":
        # Call color_flip function function
        library.color_flip_count_tree()
    elif command == "Quit":
        print("Program Terminated!!")
        sys.exit() # terminate program
    else:
        print("Incorrect command line:")
        print(command_line)
    # ... handle other commands similarly ...


def main(input_file, output_file = 'output.txt'):
    # Redirect standard output to the output file
    sys.stdout = open(output_file, 'w')

    # library forms the tree
    library = RedBlackTree()

    # process input file
    with open(input_file, 'r') as file:
        for line in file:
            execute_command(library, line)

    # Close the output file and reset standard output
    sys.stdout.close()
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    # check for wrong input arguments
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <inputfile_name> optional:<outputfile>", file=sys.stderr)
        sys.exit(1)

    # get output file from the input file name
    input_file = sys.argv[1]
    output_file = input_file.replace('.txt', '_output_file.txt')

    # call to start our main program
    main(input_file, output_file)
