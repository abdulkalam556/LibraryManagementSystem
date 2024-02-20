# GatorLibrary Management System

## Overview

The GatorLibrary Management System is designed for the GatorLibrary, a fictional library, to efficiently manage its books, patrons, and borrowing operations. It utilizes a Red-Black tree data structure for optimal management of book records, ensuring high efficiency and performance. Additionally, the system employs Binary Min-heaps for managing book reservations, enabling a priority-queue mechanism that handles patron reservations effectively.

## Features

- **Red-Black Tree for Book Management**: Ensures efficient book management by utilizing the Red-Black tree data structure, optimizing search, insertion, and deletion operations for book records.
- **Binary Min-Heap for Reservations**: Implements a priority-queue mechanism using Binary Min-heaps, managing book reservations with a focus on patron priorities and ensuring fair and efficient handling of waitlists.
- **Comprehensive Book and Patron Operations**: Supports a variety of operations including printing book details, adding and deleting books, borrowing and returning books, and managing reservations based on patron priority.
- **Analytics and Monitoring**: Includes an analytics tool to monitor and analyze the frequency of color flips in the Red-Black tree, providing insights into the tree's balance and performance.

## Getting Started

### Prerequisites

- Python 3.8 or later

### Installation and Execution

1. Clone the project repository.
2. Ensure Python 3.8 or later is installed.
3. Prepare your input file with the desired operations, please refer to the [Input Instructions](#input-instructions) section below.
4. Run the system using the command: python3 gatorLibrary.py `<inputFileName.txt>`
5. Output will be generated in `<inputFileName_output_file.txt>`.

## Input Instructions

To operate the GatorLibrary Management System, users must provide input in a specific format. The system accepts input files (.txt) containing commands for various operations such as adding books, deleting books, borrowing, returning, and querying book details.

### Input File Format

- Each line in the input file represents a distinct operation.
- Commands should be formatted as follows: `COMMAND [arguments...]` where `COMMAND` is the operation (e.g., ADD, DELETE, BORROW) and `[arguments...]` are the parameters required by the operation.

### Example

ADD ISBN12345 "Book Title" "Author Name"
DELETE ISBN12345
BORROW ISBN12345 PatronID
RETURN ISBN12345 PatronID

### Running the System with Input File

1. Prepare your input file with the desired operations.
2. Execute the system by running `python gatorLibrary.py inputFileName.txt`, replacing `inputFileName.txt` with the name of your input file.
3. The system will process each command in the input file and perform the corresponding operations, outputting the results to the console or a specified output file.

Ensure your input file is correctly formatted according to the instructions for the system to process your requests accurately.

## Project Structure

- **gatorLibrary.py**: Main script for library operations.
- **red_black_tree.py**: Implements the Red-Black Tree.
- **book.py**: Defines the `Book` class with reservation handling.
- **min_heap.py**: Implements the MinHeap class for reservations.

## Development Insights

- The system was developed using Python, leveraging its powerful `re` and `time` packages for input parsing and timestamp generation, respectively.
- Extensive testing confirmed the project's effectiveness in matching expected outputs across various test cases.

## Contributing

Contributions are welcome! Please refer to the contributing guidelines for more information.

## Acknowledgments

- Special thanks to the data structures and algorithms that underpin this system's efficiency and reliability.
