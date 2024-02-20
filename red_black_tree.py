from book import Book

class RedBlackTree:
    def __init__(self):
        self.TNULL = Book(-1, "", "", False) # This creates Null node
        self.TNULL.color = False             # black for the Null node
        self.root = self.TNULL               # Root of the tree, intially null
        self.color_flip_count = 0            # variable to count color flips
        return

    # print a book
    def print_book(self, book_id):
        # firstly search for the node
        node = self.Search(self.root, book_id)
        # print book if we can find it
        if node != self.TNULL:
            self._print_book_helper(node)
        else:
            print(f"Book {book_id} not found in the Library")
            print('')
        return

    # print books in the range
    def print_books(self, book_id1, book_id2):
        self._print_books_helper(self.root, book_id1, book_id2)
        return

    def insert_book(self, book_id, book_name, author_name, availability_status):
        # firstly create a new node for the new book
        new_book = Book(book_id = book_id, book_name = book_name, author_name = author_name, availability_status= availability_status.lower() == "yes")
        new_book.left = self.TNULL  # mark its left child as NULL
        new_book.right = self.TNULL # mark its right child as NULL

        # Binary Search Tree insertion
        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if new_book.book_id < x.book_id:
                x = x.left
            else:
                x = x.right

        new_book.parent = y
        # root of the tree
        if y is None:
            self.root = new_book
        elif new_book.book_id < y.book_id:
            y.left = new_book
        else:
            y.right = new_book

        new_book.color = True # making sure new node is always red

        # if the new node is root making it black
        if new_book == self.root:
            new_book.color = False

        # Fix the Red-Black Tree
        self._fix_insert(new_book)
        return

    # borrow a book
    def borrow_book(self, patron_id, book_id, patron_priority):
        # search for the book in the tree
        book = self.Search(self.root, book_id)

        if book != self.TNULL:
            # if book was found check for availabilty status
            if book.availability_status:
                book.availability_status = False
                book.borrowed_by = patron_id
                print(f"Book {book_id} Borrowed by Patron {patron_id}")
            else:
                # creating reservation if not available
                book.add_reservation(patron_id, patron_priority)
                print(f"Book {book_id} Reserved by Patron {patron_id}")
        else:
            # if book is not found in the library
            print(f"Book {book_id} not found in the Library")
        print('')
        return
    
    # Return a book
    def return_book(self, patron_id, book_id):
        # firstly search for book in the tree
        book = self.Search(self.root, book_id)
        if book != self.TNULL:
            # book and found and its borrowed by same patron given
            if book.borrowed_by == patron_id:
                next_reservation = book.get_next_reservation()
                if next_reservation:
                    # find and if next reservation exists, allocate respectively
                    book.borrowed_by = next_reservation
                    print(f"Book {book_id} Returned by Patron {patron_id}")
                    print('')
                    print(f"Book {book_id} Allotted to Patron {next_reservation}")
                else:
                    # if there are no reservations, make book available for others
                    book.borrowed_by = None
                    book.availability_status = True  # Book is now available
                    print(f"Book {book_id} Returned by Patron {patron_id}")
            else:
                # if book is found and its borrowed by same other patron than given
                print(f"Book {book_id} can not be returned by the Patron {patron_id}")
        else:
            # if book is not found in the library
            print(f"Book {book_id} not found in the Library")
        print('')
        return

    def delete_book(self, book_id):
        # search for the required node
        book = self.Search(self.root, book_id)

        if book != self.TNULL:
            # delete the node
            self._delete_book_helper(book)

            # notify the reservations if some exists
            if len(book.reservation_heap.heap) == 0:
                print(f"Book {book_id} is no longer available")
            elif len(book.reservation_heap.heap) == 1:
                patron_id = book.get_next_reservation()
                print(f"Book {book.book_id} is no longer available. Reservation made by Patron {patron_id} has been cancelled!")
            else:
                reservations_list = book.reservation_heap.list_patrons()
                print(f"Book {book.book_id} is no longer available. Reservations made by Patrons {', '.join(str(item) for item in reservations_list)} have been cancelled!")
        else:
            # if book is not found in the library
            print(f"Book {book_id} not found in the Library")
        print('')
        return

    def find_closest_book(self, target_id):
        # call for the closest helper
        book1, book2 = self._find_closest_book_helper(self.root, target_id, None, None)
        # if tow books exists, make sure first one has lower id than other
        if book2 and book1.book_id > book2.book_id:
            book1, book2 = book2, book1
        # print the books    
        self._print_book_helper(book1)
        if book2:
            self._print_book_helper(book2)
        return

    def color_flip_count_tree(self):
        # use the colour flip count to print the respective value
        print(f"Colour Flip Count: {self.color_flip_count}")
        print('')
        return

    # helper for print a particular book
    def _print_book_helper(self, node):
        if node != self.TNULL:
            print(f'BookID = {node.book_id}')
            print(f'Title = "{node.book_name}"')
            print(f'Author = "{node.author_name}"')
            print(f'Availability = "{"Yes" if node.availability_status else "No"}"')
            print(f"BorrowedBy = {node.borrowed_by if node.borrowed_by else 'None'}")
            # get list of patrons in the reservation
            reservations_list = node.reservation_heap.list_patrons() 
            print(f"Reservations = [{','.join(str(item) for item in reservations_list)}]")
            print('')
            # Add any other details you wish to print
        else:
            print(f"Book {book_id} not found in the Library")
        return

    def _print_books_helper(self, node, book_id1, book_id2):
        if node == self.TNULL:
            return

        # Traverse the left subtree if needed
        if book_id1 < node.book_id:
            self._print_books_helper(node.left, book_id1, book_id2)

        # Print the node's data if it's within the range
        if book_id1 <= node.book_id <= book_id2:
            self._print_book_helper(node)

        # Traverse the right subtree if needed
        if book_id2 > node.book_id:
            self._print_books_helper(node.right, book_id1, book_id2)

    def _delete_book_helper(self, node_to_delete):
        colour_flip_flag = False # variable to check color is flipped
        y = node_to_delete
        y_original_color = y.color

        # case 1: left child is none
        if node_to_delete.left == self.TNULL:
            x = node_to_delete.right
            self._set_parent_child_pointers(node_to_delete, node_to_delete.right)
        elif node_to_delete.right == self.TNULL:
            # case 2: right child is none
            x = node_to_delete.left
            self._set_parent_child_pointers(node_to_delete, node_to_delete.left)
        else:
            # case 3: both left, right child exists
            # get maximum from left sub tree
            y = self._Maximum(node_to_delete.left)
            y_original_color = y.color
            x = y.left

            # follow the above methods
            if y.parent == node_to_delete:
                x.parent = y
            else:
                self._set_parent_child_pointers(y, y.left)
                y.left = node_to_delete.left
                y.left.parent = y

            self._set_parent_child_pointers(node_to_delete, y)
            y.right = node_to_delete.right
            y.right.parent = y
            
            if y.color != node_to_delete.color:
                colour_flip_flag = True
                self.color_flip_count = self.color_flip_count + 1
                
            y.color = node_to_delete.color

        if x.color == True:
            x.color = False
            self.color_flip_count = self.color_flip_count + 1
            return

        # call rebalancing only when deleted node is black 
        if y_original_color == False:
            self._fix_delete(x)

        # check for the color flip flag and set the count
        if colour_flip_flag and y.color != node_to_delete.color:
            self.color_flip_count = self.color_flip_count - 2
            colour_flip_flag = False

        return

    def _fix_insert(self, k):
        # Red-Black tree fix-up logic
        while k != self.root and k.parent.color == True:
            if k.parent == k.parent.parent.right:
                uncle = k.parent.parent.left
                if uncle.color == True:
                    # case XYr
                    uncle.color = False
                    k.parent.color = False
                    k.parent.parent.color = True
                    k = k.parent.parent
                    self.color_flip_count = self.color_flip_count + 3
                else:
                    if k == k.parent.left:
                        # case LRb
                        k = k.parent
                        self._right_rotate(k)
                    # case LLb
                    k.parent.color = False
                    k.parent.parent.color = True
                    self._left_rotate(k.parent.parent)
                    self.color_flip_count = self.color_flip_count + 2
            else:
                uncle = k.parent.parent.right
                # case XYr
                if uncle.color == True:
                    uncle.color = False
                    k.parent.color = False
                    k.parent.parent.color = True
                    k = k.parent.parent
                    self.color_flip_count = self.color_flip_count + 3
                else:
                    if k == k.parent.right:
                        #case LRb
                        k = k.parent
                        self._left_rotate(k)
                    #case LLb
                    k.parent.color = False
                    k.parent.parent.color = True
                    self._right_rotate(k.parent.parent)
                    self.color_flip_count = self.color_flip_count + 2
        
        if self.root.color == True:
            self.color_flip_count = self.color_flip_count - 1
        # set root color
        self.root.color = False
        return

    def _fix_delete(self, x):
        while x != self.root and x.color == False:
            # self.print_tree(self.root, '', True)
            # print(x.book_id)
            
            if x == x.parent.right:
                sibiling = x.parent.left
                if sibiling.color == False:
                    # RB cases
                    # Rb0
                    if sibiling.left.color == False and sibiling.right.color == False:
                        if x.parent.color == False: # case 1 py is balck
                            sibiling.color = True
                            x = sibiling.parent
                            self.color_flip_count = self.color_flip_count + 1
                            continue
                        else: # case 2 py is red
                            sibiling.color = True
                            x.parent.color = False
                            self.color_flip_count = self.color_flip_count + 2
                            break
                    elif sibiling.right.color == True:
                        # Rb2, Rb1 case 2
                        self._left_rotate(sibiling)
                        self._right_rotate(x.parent)
                        if sibiling.parent.color != x.parent.color:
                            self.color_flip_count = self.color_flip_count + 1
                        sibiling.parent.color = x.parent.color
                        if x.parent.color:
                            self.color_flip_count = self.color_flip_count + 1
                        x.parent.color = False
                        break
                    else:
                        # Rb1 case 1
                        self._right_rotate(x.parent)
                        sibiling.left.color = False
                        self.color_flip_count = self.color_flip_count + 1
                        if sibiling.color != x.parent.color:
                            self.color_flip_count = self.color_flip_count + 1
                        sibiling.color = x.parent.color
                        if x.parent.color:
                            self.color_flip_count = self.color_flip_count + 1
                        x.parent.color = False
                        break
                else:
                    # Rr cases
                    w = sibiling.right

                    if w.left == self.TNULL and w.right == self.TNULL:
                        # Rr(0)
                        self._right_rotate(x.parent)
                        x.parent.left = True
                        sibiling.color = False
                        self.color_flip_count = self.color_flip_count + 2
                        break
                    elif w.right.color == True:
                        # Rr(2), Rr(1) case 2
                        self._left_rotate(w)
                        self._left_rotate(sibiling)
                        self._right_rotate(x.parent)
                        sibiling.parent.color = False
                        self.color_flip_count = self.color_flip_count + 1
                        break
                    else:
                        # Rr(1) case 1
                        self._left_rotate(sibiling)
                        self._right_rotate(x.parent)
                        sibiling.right.color = False
                        self.color_flip_count = self.color_flip_count + 1
                        break
            else:
                sibiling = x.parent.right
                if sibiling.color == False:
                    # LB cases
                    # Lb0
                    if sibiling.right.color == False and sibiling.left.color == False:
                        if x.parent.color == False: # case 1 py is balck
                            sibiling.color = True
                            x = sibiling.parent
                            self.color_flip_count = self.color_flip_count + 1
                            continue
                        else: # case 2 py is red
                            sibiling.color = True
                            x.parent.color = False
                            self.color_flip_count = self.color_flip_count + 2
                            break
                    elif sibiling.left.color == True:
                        # Rb2, Rb1 case 2
                        self._right_rotate(sibiling)
                        self._left_rotate(x.parent)
                        if sibiling.parent.color != x.parent.color:
                            self.color_flip_count = self.color_flip_count + 1
                        sibiling.parent.color = x.parent.color
                        if x.parent.color:
                            self.color_flip_count = self.color_flip_count + 1
                        x.parent.color = False
                        break
                    else:
                        # Rb1 case 1
                        self._left_rotate(x.parent)
                        sibiling.right.color = False
                        self.color_flip_count = self.color_flip_count + 1
                        if sibiling.color != x.parent.color:
                            self.color_flip_count = self.color_flip_count + 1
                        sibiling.color = x.parent.color
                        if x.parent.color:
                            self.color_flip_count = self.color_flip_count + 1
                        x.parent.color = False
                        break
                else:
                    # Rr cases
                    w = sibiling.left
                    
                    if w.right == self.TNULL and w.left == self.TNULL:
                        # Rr(0)
                        self._left_rotate(x.parent)
                        x.parent.right.color = True
                        sibiling.color = False
                        self.color_flip_count = self.color_flip_count + 2
                        break
                    elif w.left.color == True:
                        # Rr(2), Rr(1) case 2
                        self._right_rotate(w)
                        self._right_rotate(sibiling)
                        self._left_rotate(x.parent)
                        sibiling.parent.color = False
                        self.color_flip_count = self.color_flip_count + 1
                        break
                    else:
                        # Rr(1) case 1
                        self._right_rotate(sibiling)
                        self._left_rotate(x.parent)
                        sibiling.left.color = False
                        self.color_flip_count = self.color_flip_count + 1
                        break

        if self.root.color:
            self.color_flip_count = self.color_flip_count + 1

        # set the root colour
        self.root.color = False
        return

    def _find_closest_book_helper(self, node, target_id, closest, second_closest):
        if node == self.TNULL:
            # in case of tie, return both nodes
            if second_closest and abs(target_id - closest.book_id) == abs(target_id - second_closest.book_id):
                return closest, second_closest
            else:
                return closest, None

        # find the differences
        current_diff = abs(target_id - node.book_id)
        closest_diff = abs(target_id - closest.book_id) if closest else float('inf')
        second_closest_diff = abs(target_id - second_closest.book_id) if second_closest else float('inf')

        # Update closest and second closest nodes
        if current_diff < closest_diff:
            second_closest = closest
            closest = node
        elif current_diff == closest_diff:
            second_closest = node

        if node.book_id < target_id:
            return self._find_closest_book_helper(node.right, target_id, closest, second_closest)
        else:
            return self._find_closest_book_helper(node.left, target_id, closest, second_closest)


    # search for a key in subtree rooted at node
    def Search(self, node, key):
        if node == self.TNULL or key == node.book_id:
            return node
        elif key < node.book_id:
            return self.Search(node.left, key)
        else:
            return self.Search(node=node.right, key=key)

    # finding maximum of subtree rooted at node
    def _Maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def _set_parent_child_pointers(self, node_to_be_deleted, replacing_node):
        # used in delete operation
        # to transfer set parent and child pointers of node_to_be_deleted to replacing_node when node_to_be_deleted is deleted
        if node_to_be_deleted.parent is None:
            self.root = replacing_node
        elif node_to_be_deleted == node_to_be_deleted.parent.left:
            node_to_be_deleted.parent.left = replacing_node
        else:
            node_to_be_deleted.parent.right = replacing_node
        
        replacing_node.parent = node_to_be_deleted.parent
        return

    def _left_rotate(self, node):
        # left rotate tree, i.e make node left child of its rights child
        y = node.right
        node.right = y.left

        if y.left != self.TNULL:
            y.left.parent = node

        y.parent = node.parent

        if node.parent is None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        
        y.left = node
        node.parent = y
        return

    def _right_rotate(self, node):
        # right rotate tree, i.e make node right child of its lefts child
        y = node.left
        node.left = y.right

        if y.right != self.TNULL:
            y.right.parent = node

        y.parent = node.parent

        if node.parent is None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        
        y.right = node
        node.parent = y
        return

    def print_tree(self, node, indent, last):
        # Prints the tree structure on the console for debugging
        if node != self.TNULL:
            print(indent, end = '')

            if last:
                print("R----", end = '')
                indent += "|     "
            else:
                print("L----", end = '')
                indent += "|     "

            s_color = "RED" if node.color else "Black"
            print(f'{node.book_id}({s_color})')

            self.print_tree(node=node.left, indent=indent, last=False)
            self.print_tree(node=node.right, indent=indent, last=True)
        return
            