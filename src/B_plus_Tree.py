#======================================================================
class BPTreeNode:
    def __init__(self, order):
        self.__order = order
        self.__parent: "BPTreeNode" = None
        self.__keys = []
        self.__children = []  # children for internal, data for leaves

    # -------- Encapsulation Getters/Setters --------
    def get_order(self) -> int:
        return self.__order

    def get_parent(self):
        return self.__parent

    def set_parent(self, parent: "BPTreeNode"):
        self.__parent = parent

    def get_keys(self):
        return list(self.__keys)

    def get_key_at(self, i):
        return self.__keys[i]

    def get_keys_size(self) -> int:
        return len(self.__keys)

    def set_keys(self, keys: list):
        self.__keys = list(keys)

    def append_key(self, key):
        self.__keys.append(key)

    def insert_key_at(self, index, key):
        self.__keys.insert(index, key)

    def remove_key_at(self, index):
        return self.__keys.pop(index)

    def get_children(self):
        return list(self.__children)

    def get_child_at(self, i):
        return self.__children[i]

    def set_children(self, children: list):
        self.__children = list(children)

    def append_child(self, child):
        self.__children.append(child)

    def insert_child_at(self, index, child):
        self.__children.insert(index, child)

    def remove_child_at(self, index):
        return self.__children.pop(index)

    # Utils
    def is_leaf(self) -> bool:
        return False  # overridden in Leaf subclass
    
    def get_size(self) -> int:
        return len(self.__keys)

    def is_empty(self) -> bool:
        return len(self.__keys) == 0

    def is_full(self) -> bool:
        return len(self.__keys) >= self.__order

    def is_root(self) -> bool:
        return self.__parent is None

#======================================================================
class BPTreeInternalNode(BPTreeNode):
    def __init__(self, order: int):
        super().__init__(order)

    def is_leaf(self) -> bool:
        return False

#======================================================================
class BPTreeLeafNode(BPTreeNode):
    def __init__(self, order: int):
        super().__init__(order)
        self.__next: "BPTreeLeafNode" = None  # link to next leaf

    def is_leaf(self) -> bool:
        return True

    def get_next(self):
        return self.__next

    def set_next(self, nxt: "BPTreeLeafNode"):
        self.__next = nxt

#======================================================================
class BPTree:
    def __init__(self, order: int):
        self.__order = order
        self.__root: BPTreeNode = BPTreeLeafNode(order)

    def get_root(self):
        return self.__root

    # Insert
    def insert(self, key, value):
        leaf = self.__find_leaf(key)
        self.__insert_in_leaf(leaf, key, value)
        if leaf.is_full():
            self.__split_leaf(leaf)

    # Find the leaf node where key belongs
    def __find_leaf(self, key) -> BPTreeLeafNode:
        node = self.__root
        while not node.is_leaf():
            i = 0
            while i < node.get_keys_size() and key >= node.get_key_at(i):
                i += 1
            node = node.get_child_at(i)
        return node

    # Insert key/value in leaf node
    def __insert_in_leaf(self, leaf: BPTreeLeafNode, key, value):
        i = 0
        while i < leaf.get_keys_size() and key > leaf.get_key_at(i):
            i += 1
        leaf.insert_key_at(i, key)
        leaf.insert_child_at(i, value)

    def __split_leaf(self, leaf: BPTreeLeafNode):
        order = leaf.get_order()
        mid = leaf.get_keys_size()//2

        # Create new right leaf
        new_leaf = BPTreeLeafNode(order)
        new_leaf.set_keys(leaf.get_keys()[mid:])
        new_leaf.set_children(leaf.get_children()[mid:])
        leaf.set_keys(leaf.get_keys()[:mid])
        leaf.set_children(leaf.get_children()[:mid])

        # Update leaf chain
        new_leaf.set_next(leaf.get_next())
        leaf.set_next(new_leaf)

        # Promote first key of new leaf
        promote_key = new_leaf.get_key_at(0)
        self.__insert_in_parent(leaf, promote_key, new_leaf)


    # Recursive parent insertion
    def __insert_in_parent(self, node, key, new_node):
        if node.is_root():
            # Create new root
            new_root = BPTreeInternalNode(self.__order)
            new_root.set_keys([key])
            new_root.set_children([node, new_node])
            node.set_parent(new_root)
            new_node.set_parent(new_root)
            self.__root = new_root
            return

        parent = node.get_parent()
        # Find index to insert key
        idx = 0
        while idx < parent.get_keys_size() and key > parent.get_key_at(idx):
            idx += 1

        parent.insert_key_at(idx, key)
        parent.insert_child_at(idx + 1, new_node)
        new_node.set_parent(parent)

        # If parent overflow, split recursively
        if parent.is_full():
            self.__split_internal(parent)

    # Split an internal node
    def __split_internal(self, node: BPTreeInternalNode):
        order = node.get_order()
        mid = len(node.get_keys()) // 2
        promote_key = node.get_key_at(mid)

        # Create new internal node
        new_node = BPTreeInternalNode(order)
        new_node.set_keys(node.get_keys()[mid+1:])
        new_node.set_children(node.get_children()[mid+1:])
        for child in new_node.get_children():
            child.set_parent(new_node)

        # Update left node
        node.set_keys(node.get_keys()[:mid])
        node.set_children(node.get_children()[:mid+1])

        self.__insert_in_parent(node, promote_key, new_node)


    #Deletion
    def delete(self, key):
        leaf = self.__find_leaf(key)
        
        try:
            idx = leaf.get_keys().index(key)
        except ValueError:
            return # Key not found

        # Remove key and Values
        leaf.remove_key_at(idx)
        leaf.remove_child_at(idx)

        # Underflow - size go lower than min
        if leaf != self.__root and leaf.get_keys_size() < (self.__order + 1)//2:
            self.__rebalance(leaf)


    def __rebalance(self, node: BPTreeNode):
        pass


    # Search
    def search(self, key):
        leaf = self.__find_leaf(key)
        for i, k in enumerate(leaf.get_keys()):
            if k == key:
                return leaf.get_child_at(i)
        return None

    # Display --For Debugging
    def display_tree_ascii(self):
        from collections import deque           #Go make dequeue plz This just for debugging.
        if self.__root is None:
            print("Empty tree")
            return

        queue = deque([(self.__root, 0)])
        prev_level = -1
        level_str = ""

        while queue:
            node, level = queue.popleft()
            if level != prev_level:
                if prev_level != -1:
                    print(level_str)
                level_str = f"Level {level}: "
                prev_level = level

            if node.is_leaf():
                level_str += "[" + ",".join(map(str, node.get_keys())) + "] -> "
            else:
                level_str += "(" + ",".join(map(str, node.get_keys())) + ") "

            if not node.is_leaf():
                for child in node.get_children():
                    queue.append((child, level + 1))

        print(level_str)

    def display_leaves_horizontal(self):
        print("Leaf chain: ", end="")
        node = self.__root
        while not node.is_leaf():
            node = node.get_child_at(0)
        while node:
            print("[" + ",".join(map(str, node.get_keys())) + "] -> ", end="")
            node = node.get_next()
        print("None")
