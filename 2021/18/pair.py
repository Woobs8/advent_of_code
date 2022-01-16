import math

class Pair:
    def __init__(self, value, left, right, parent):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def get_magnitude(self) -> int:
        return self._get_left_magnitude() + self._get_right_magnitude()

    def _get_left_magnitude(self) -> int:
        if not self.left.value is None:
            return 3 * self.left.value
        else:
            return 3 * self.left.get_magnitude()

    def _get_right_magnitude(self) -> int:
        if not self.right.value is None:
            return 2 * self.right.value
        else:
            return 2 * self.right.get_magnitude()

    def get_depth(self) -> int:
        depth = 0
        pair = self
        while not pair.parent is None:
            depth += 1
            pair = pair.parent
        return depth

    def get_position(self) -> int:
        position = 0
        pair = self
        while not pair.parent is None:
            parent = pair.parent 
            if parent.right is pair:
                position += parent.left.get_length()
            pair = parent
        return position

    def get_length(self) -> int:
        if not self.value is None:
            return 1
        else:
            return self.left.get_length() + self.right.get_length()

    def explode(self):
        left_adjacent = self._get_left_adjacent_pair()
        if not left_adjacent is None:
            left_adjacent.value += self.left.value
        right_adjacent = self._get_right_adjacent_pair()
        if not right_adjacent is None:
            right_adjacent.value += self.right.value
        self.left = None
        self.right = None
        self.value = 0
        return left_adjacent, right_adjacent

    def _get_left_adjacent_pair(self):
        left_adjacent_pair = None
        parent = self
        while not parent is None:
            next_parent = parent.parent
            if not next_parent is None and next_parent.right is parent:
                return self._get_rightmost_child(next_parent.left)
            parent = next_parent
        return left_adjacent_pair

    def _get_rightmost_child(self, pair):
        rightmost_element = pair
        while not rightmost_element.right is None:
            rightmost_element = rightmost_element.right
        return rightmost_element

    def _get_right_adjacent_pair(self):
        right_adjacent_pair = None
        parent = self
        while not parent is None:
            next_parent = parent.parent
            if (not next_parent is None) and (next_parent.left is parent):
                return self._get_leftmost_child(next_parent.right)
            parent = next_parent
        return right_adjacent_pair

    def _get_leftmost_child(self, pair):
        leftmost_element = pair
        while not leftmost_element.left is None:
            leftmost_element = leftmost_element.left
        return leftmost_element

    def split(self):
        self.left = Pair(self.value // 2, None, None, self)
        self.right = Pair(math.ceil(self.value / 2), None, None, self)
        self.value = None

    def copy(self):
        if not self.value is None:
            return Pair(self.value, None, None, None)
        else:
            clone = Pair(None, None, None, None)
            clone.left = self.left.copy()
            clone.left.parent = clone
            clone.right = self.right.copy()
            clone.right.parent = clone
            return clone

    def __str__(self):
        return self._print_pair(self)

    def _print_pair(self, pair) -> str:
        print_string = ''
        if not pair.value is None:
            print_string += str(pair.value)
        else:
            left = self._print_pair(pair.left)
            right = self._print_pair(pair.right)
            print_string += '[' + left + ',' + right + ']'
        return print_string