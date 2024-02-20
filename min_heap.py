import time

class MinHeap:
    def __init__(self):
        self.heap = []

    # get parent of pos
    def parent(self, pos):
        return (pos - 1) // 2

    # get left child of pos
    def left_child(self, pos):
        return 2 * pos + 1

    # get right child of pos
    def right_child(self, pos):
        return 2 * pos + 2

    # check if we have a parent
    def has_parent(self, pos):
        return self.parent(pos) >= 0

    # check if we have a left child
    def has_left_child(self, pos):
        return self.left_child(pos) < len(self.heap)

    # check if we have a right child
    def has_right_child(self, pos):
        return self.right_child(pos) < len(self.heap)

    # swap nodes
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        return

    # heap insert
    def insert(self, patron_id, priority):
        timestamp = time.time()
        self.heap.append((priority, timestamp, patron_id))
        # heapify to set the tree
        self.heapify_up(len(self.heap) - 1)
        return

    # heapify to set the min heap property from bottom, new inserted node to root
    def heapify_up(self, pos):
        while self.has_parent(pos) and self.heap[pos] < self.heap[self.parent(pos)]:
            self.swap(pos, self.parent(pos))
            pos = self.parent(pos)
        return

    # return min root
    def pop(self):
        if len(self.heap) == 0:
            raise IndexError("Pop from empty heap")
        root = self.heap[0]
        # fill the root with last element
        self.heap[0] = self.heap[-1]
        self.heap.pop() # delete the last element
        self.heapify_down(0) # heapify
        return root[2] # we need only the patron_id

    # heapify to set the min heap property from top, new root to the leafs
    def heapify_down(self, i):
        while self.has_left_child(i):
            smaller_child_index = self.left_child(i)
            if self.has_right_child(i) and self.heap[self.right_child(i)] < self.heap[smaller_child_index]:
                smaller_child_index = self.right_child(i)

            if self.heap[i] < self.heap[smaller_child_index]:
                break
            else:
                self.swap(i, smaller_child_index)
            i = smaller_child_index
        return

    # return a list of patron ids, for printing in the book
    def list_patrons(self):
        return [p[2] for p in self.heap]

    # print the heap for the debugging
    def print(self):
        print (*self.heap, sep=",")
        return
