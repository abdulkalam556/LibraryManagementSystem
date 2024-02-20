from min_heap import MinHeap

class Book:
    def __init__(self, book_id, book_name, author_name, availability_status):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = None           # id of the person borrowed
        self.color = True                 # Red color (True for red color, False for the black color)
        self.left = None
        self.right = None
        self.parent = None
        self.reservation_heap = MinHeap()  # Using your MinHeap

    def add_reservation(self, patron_id, priority):
        self.reservation_heap.insert(patron_id, priority)
        return

    def get_next_reservation(self):
        if len(self.reservation_heap.heap) > 0:
            return self.reservation_heap.pop()
        return None
