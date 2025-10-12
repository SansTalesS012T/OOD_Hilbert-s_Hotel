import math

class BPTreeNode:
    def __init__(self, order):
        self.__order = order
        self.__parent: "BPTreeNode" = None
        self.__keys = []
        self.__children = []

    def get_order(self): return self.__order
    def get_parent(self): return self.__parent
    def set_parent(self, parent): self.__parent = parent
    def get_keys(self): return self.__keys
    def get_key_at(self, i): return self.__keys[i]
    def get_keys_size(self): return len(self.__keys)
    def set_keys(self, keys): self.__keys = keys
    def get_children(self): return self.__children
    def get_child_at(self, i): return self.__children[i]
    def get_children_size(self): return len(self.__children)
    def set_children(self, children): self.__children = children
    def is_leaf(self): return False
    def is_root(self): return self.__parent is None
    def is_full(self): return len(self.__keys) >= self.__order - 1

class BPTreeInternalNode(BPTreeNode):
    def __init__(self, order):
        super().__init__(order)
    def is_leaf(self): return False

class BPTreeLeafNode(BPTreeNode):
    def __init__(self, order):
        super().__init__(order)
        self.__next: "BPTreeLeafNode" = None
    def is_leaf(self): return True
    def get_next(self): return self.__next
    def set_next(self, nxt): self.__next = nxt

class BPTree:
    def __init__(self, order: int):
        self.__order = order
        self.__root: BPTreeNode = BPTreeLeafNode(order)

    def _binary_search_left(self, arr, x):
        low = 0
        high = len(arr)
        while low < high:
            mid = (low + high) // 2
            if arr[mid] < x:
                low = mid + 1
            else:
                high = mid
        return low

    def _binary_search_right(self, arr, x):
        low = 0
        high = len(arr)
        while low < high:
            mid = (low + high) // 2
            if x < arr[mid]:
                high = mid
            else:
                low = mid + 1
        return low

    def get_root(self):
        return self.__root

    def bulk_load(self, data: list):
        if not data:
            self.__root = BPTreeLeafNode(self.__order)
            return
        data.sort(key=lambda x: x[0])
        
        leaves = []
        current_leaf = BPTreeLeafNode(self.__order)
        leaves.append(current_leaf)

        for key, value in data:
            if len(current_leaf.get_keys()) >= self.__order - 1:
                new_leaf = BPTreeLeafNode(self.__order)
                current_leaf.set_next(new_leaf)
                current_leaf = new_leaf
                leaves.append(current_leaf)
            current_leaf.get_keys().append(key)
            current_leaf.get_children().append(value)
        
        current_level = leaves
        while len(current_level) > 1:
            parents = []
            new_parent = BPTreeInternalNode(self.__order)
            parents.append(new_parent)
            
            for node in current_level:
                if len(new_parent.get_children()) >= self.__order:
                    new_parent = BPTreeInternalNode(self.__order)
                    parents.append(new_parent)
                
                if not new_parent.get_children():
                    new_parent.get_children().append(node)
                else:
                    promote_key = node.get_key_at(0)
                    new_parent.get_keys().append(promote_key)
                    new_parent.get_children().append(node)
                node.set_parent(new_parent)
            
            current_level = parents
        
        self.__root = current_level[0]
        self.__root.set_parent(None)

    def __find_leaf(self, key) -> BPTreeLeafNode:
        node = self.__root
        while not node.is_leaf():

            index = self._binary_search_right(node.get_keys(), key)
            node = node.get_child_at(index)
        return node

    def insert(self, key, value):
        leaf = self.__find_leaf(key)
        
        index = self._binary_search_left(leaf.get_keys(), key)

        if index < len(leaf.get_keys()) and leaf.get_key_at(index) == key:
            print(f"Key {key} already exists. Update not performed.")
            return

        leaf.get_keys().insert(index, key)
        leaf.get_children().insert(index, value)

        if len(leaf.get_keys()) >= self.__order:
            self.__split(leaf)

    def search(self, key):
        leaf = self.__find_leaf(key)

        index = self._binary_search_left(leaf.get_keys(), key)
        
        if index < len(leaf.get_keys()) and leaf.get_key_at(index) == key:
            return leaf.get_child_at(index)
        
        return None

    def __split(self, node):
        mid_index = self.__order // 2
        promote_key = node.get_keys()[mid_index]
        new_node = BPTreeLeafNode(self.__order) if node.is_leaf() else BPTreeInternalNode(self.__order)
        new_node.set_parent(node.get_parent())

        if node.is_leaf():
            new_node.set_keys(node.get_keys()[mid_index:])
            new_node.set_children(node.get_children()[mid_index:])
            node.set_keys(node.get_keys()[:mid_index])
            node.set_children(node.get_children()[:mid_index])
            new_node.set_next(node.get_next())
            node.set_next(new_node)
        else:
            new_node.set_keys(node.get_keys()[mid_index + 1:])
            new_node.set_children(node.get_children()[mid_index + 1:])
            for child in new_node.get_children():
                child.set_parent(new_node)
            node.set_keys(node.get_keys()[:mid_index])
            node.set_children(node.get_children()[:mid_index + 1])

        self.__insert_in_parent(node, promote_key, new_node)

    def __insert_in_parent(self, left_child, key, right_child):
        parent = left_child.get_parent()
        if parent is None:
            new_root = BPTreeInternalNode(self.__order)
            new_root.set_keys([key])
            new_root.set_children([left_child, right_child])
            left_child.set_parent(new_root)
            right_child.set_parent(new_root)
            self.__root = new_root
            return

        index = self._binary_search_right(parent.get_keys(), key)
        parent.get_keys().insert(index, key)
        parent.get_children().insert(index + 1, right_child)
        
        if len(parent.get_keys()) >= self.__order:
            self.__split(parent)

    def get_all_values(self) -> list:
        all_values = []
        if not self.__root: return all_values
        node = self.__root
        while not node.is_leaf():
            node = node.get_child_at(0)
        while node:
            all_values.extend(node.get_children())
            node = node.get_next()
        return all_values