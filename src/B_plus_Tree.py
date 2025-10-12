import math
from collections import deque

#======================================================================
# BPTreeNode and Subclasses
#======================================================================
class BPTreeNode:
    def __init__(self, order):
        self.__order = order
        self.__parent: "BPTreeNode" = None
        self.__keys = []
        self.__children = []

    # --- CORE FIX: Return direct references for modification ---
    def get_keys(self):
        return self.__keys
    def get_children(self):
        return self.__children

    # --- Other Getters/Setters ---
    def get_order(self) -> int: return self.__order
    def get_parent(self): return self.__parent
    def set_parent(self, parent: "BPTreeNode"): self.__parent = parent
    def get_key_at(self, i): return self.__keys[i]
    def get_keys_size(self) -> int: return len(self.__keys)
    def set_keys(self, keys: list): self.__keys = list(keys)
    def get_child_at(self, i): return self.__children[i]
    def get_children_size(self): return len(self.__children)
    def set_children(self, children: list): self.__children = list(children)
    
    # --- Utility Methods ---
    def is_leaf(self) -> bool: return False
    def is_root(self) -> bool: return self.__parent is None
    def is_full(self) -> bool: return len(self.__keys) >= self.__order - 1

class BPTreeInternalNode(BPTreeNode):
    def __init__(self, order: int): super().__init__(order)
    def is_leaf(self) -> bool: return False

class BPTreeLeafNode(BPTreeNode):
    def __init__(self, order: int):
        super().__init__(order)
        self.__next: "BPTreeLeafNode" = None
    def is_leaf(self) -> bool: return True
    def get_next(self): return self.__next
    def set_next(self, nxt: "BPTreeLeafNode"): self.__next = nxt

#======================================================================
# B+ Tree Main Class
#======================================================================
class BPTree:
    def __init__(self, order: int):
        self.__order = order
        self.__root: BPTreeNode = BPTreeLeafNode(order)

    def get_root(self):
        return self.__root

    def _binary_search_left(self, arr, x):
        low, high = 0, len(arr)
        while low < high:
            mid = (low + high) // 2
            if arr[mid] < x: low = mid + 1
            else: high = mid
        return low

    def _binary_search_right(self, arr, x):
        low, high = 0, len(arr)
        while low < high:
            mid = (low + high) // 2
            if x < arr[mid]: high = mid
            else: low = mid + 1
        return low

    def __find_leaf(self, key) -> BPTreeLeafNode:
        node = self.__root
        while not node.is_leaf():
            index = self._binary_search_right(node.get_keys(), key)
            node = node.get_child_at(index)
        return node

    def insert(self, key, value):
        leaf = self.__find_leaf(key)
        index = self._binary_search_left(leaf.get_keys(), key)
        if index < leaf.get_keys_size() and leaf.get_key_at(index) == key:
            return
        leaf.get_keys().insert(index, key)
        leaf.get_children().insert(index, value)
        if leaf.is_full():
            self.__split(leaf)

    def __split(self, node: BPTreeNode):
        mid_index = self.__order // 2
        new_node = BPTreeLeafNode(self.__order) if node.is_leaf() else BPTreeInternalNode(self.__order)
        new_node.set_parent(node.get_parent())

        if node.is_leaf():
            promote_key = node.get_key_at(mid_index)
            new_node.set_keys(node.get_keys()[mid_index:])
            new_node.set_children(node.get_children()[mid_index:])
            node.set_keys(node.get_keys()[:mid_index])
            node.set_children(node.get_children()[:mid_index])
            new_node.set_next(node.get_next())
            node.set_next(new_node)
        else:
            promote_key = node.get_keys().pop(mid_index)
            new_node.set_keys(node.get_keys()[mid_index:])
            new_node.set_children(node.get_children()[mid_index + 1:])
            for child in new_node.get_children():
                child.set_parent(new_node)
            node.set_keys(node.get_keys()[:mid_index])
            node.set_children(node.get_children()[:mid_index + 1])
        
        self.__insert_in_parent(node, promote_key, new_node)

    def __insert_in_parent(self, left_node, key, right_node):
        parent = left_node.get_parent()
        if parent is None:
            new_root = BPTreeInternalNode(self.__order)
            new_root.get_keys().append(key)
            new_root.get_children().append(left_node)
            new_root.get_children().append(right_node)
            left_node.set_parent(new_root)
            right_node.set_parent(new_root)
            self.__root = new_root
            return
        
        index = self._binary_search_right(parent.get_keys(), key)
        parent.get_keys().insert(index, key)
        parent.get_children().insert(index + 1, right_node)
        right_node.set_parent(parent)

        if parent.is_full():
            self.__split(parent)

    def search(self, key):
        leaf = self.__find_leaf(key)
        index = self._binary_search_left(leaf.get_keys(), key)
        if index < leaf.get_keys_size() and leaf.get_key_at(index) == key:
            return leaf.get_child_at(index)
        return None

    def bulk_load(self, data: list):
        if not data:
            self.__root = BPTreeLeafNode(self.__order)
            return
        
        leaves = []
        current_leaf = BPTreeLeafNode(self.__order)
        leaves.append(current_leaf)

        for key, value in data:
            if current_leaf.get_keys_size() >= self.__order - 1:
                new_leaf = BPTreeLeafNode(self.__order)
                current_leaf.set_next(new_leaf)
                new_leaf.set_parent(current_leaf.get_parent())
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
                if new_parent.get_children_size() >= self.__order:
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