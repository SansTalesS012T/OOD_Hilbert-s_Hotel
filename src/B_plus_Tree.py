import math

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

    def set_key_at(self, i, key):
        self.__keys[i] = key

    def remove_key_at(self, index):
        return self.__keys.pop(index)

    def get_children(self):
        return list(self.__children)

    def get_child_at(self, i):
        return self.__children[i]
    
    def get_children_size(self):
        return len(self.__children)

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

    def is_empty(self) -> bool:
        return len(self.__keys) == 0

    def is_full(self) -> bool:
        return len(self.__keys) >= self.__order

    def is_root(self) -> bool:
        return self.__parent is None
    
    # Compare key mode
    
    def compare_key_at_mode(self, key, index, mode):
        match (mode):
            case 0:
                return key < self.__keys[index]
            case 1:
                return key <= self.__keys[index]
            case 2:
                return key == self.__keys[index]
            case 3:
                return key >= self.__keys[index]
            case 4:
                return key > self.__keys[index]
            
    def compare_key_size_at_mode(self, size, mode):
        match (mode):
            case 0:
                return size < self.get_keys_size()
            case 1:
                return size <= self.get_keys_size()
            case 2:
                return size == self.get_keys_size()
            case 3:
                return size >= self.get_keys_size()
            case 4:
                return size > self.get_keys_size()
            
    def get_key_size_with_ratio(self, ratio, mode = 0):
        match(mode):
            case 0:
                return self.get_keys_size() * ratio 
            case 1:
                return math.floor(self.get_keys_size() * ratio)
            case 2:
                return math.ceil(self.get_keys_size() * ratio)
            case 3:
                return round(self.get_keys_size() * ratio)
            
    def is_underflow(self):
        return self.get_keys_size() < math.ceil((self.__order - 1) / 2)

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
            while node.compare_key_size_at_mode(i, 0) and node.compare_key_at_mode(key, i, 3):
                i += 1
            node = node.get_child_at(i)
        return node

    # Insert key/value in leaf node
    def __insert_in_leaf(self, leaf: BPTreeLeafNode, key, value):
        i = 0
        while leaf.compare_key_size_at_mode(i, 0) and leaf.compare_key_at_mode(key, i, 4):
            i += 1
        leaf.insert_key_at(i, key)
        leaf.insert_child_at(i, value)

    def __split_leaf(self, leaf: BPTreeLeafNode):
        order = leaf.get_order()
        # mid = leaf.get_keys_size()//2
        mid = leaf.get_key_size_with_ratio(0.5, 1)

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

        parent: BPTreeNode = node.get_parent() 
        # Find index to insert key  
        indx = 0
        # compare (indx < parent key size) and (key > parent key[indx])
        while parent.compare_key_size_at_mode(indx, 0) and parent.compare_key_at_mode(key, indx, 4):
            indx += 1

        parent.insert_key_at(indx, key)
        parent.insert_child_at(indx + 1, new_node)
        new_node.set_parent(parent)

        # If parent overflow, split recursively
        if parent.is_full():
            self.__split_internal(parent)

    # Split an internal node
    def __split_internal(self, node: BPTreeInternalNode):
        order       = node.get_order()
        # mid = len(node.get_keys()) // 2
        mid         = node.get_key_size_with_ratio(0.5, 1)
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


    #Deletion (Excecute -> Borrow(if possible), Merge)
    def delete(self, key):
        leaf = self.__find_leaf(key)

        try:
            indx = leaf.get_keys().index(key)
        except ValueError:
            return # Key not found

        # Remove key and Values
        leaf.remove_key_at(indx)
        leaf.remove_child_at(indx)

        # print("\n======Debugger======")
        # self.display_tree_ascii()
        # print("====================\n")

        # Underflow - size go lower than min
        if leaf != self.__root and leaf.is_underflow():
            # print("\n======Debugger======")
            # print("Under Flow") 
            # print("====================\n")
            self.__rebalance(leaf)
        else:
            self.__update_parent_keys(leaf)

    def __update_parent_keys(self, node: BPTreeNode):
        parent = node.get_parent()
        if not parent:
            return

        children = parent.get_children()
        for i in range(parent.get_keys_size()):
            # Update each key to the first key of the right child
            parent.set_key_at(i, children[i + 1].get_key_at(0))



    def __rebalance(self, node: BPTreeNode):
        parent = node.get_parent()
        # print("\n======Debugger======")
        # print(parent.get_keys()) 
        # print("====================\n")       
        if not parent:                                                      # Root case
            if not node.is_leaf() and node.is_empty():            # Root internal node with one child -> promote that child
                self.__root = node.get_child_at(0)
                self.__root.set_parent(None)
            return

        children = parent.get_children()
        indx = children.index(node)

        # print("\n======Debugger======")
        # print(children[0].get_keys()) 
        # print("====================\n")   

        left_sibling:  BPTreeNode  = children[indx - 1] if indx > 0 else None
        right_sibling: BPTreeNode = children[indx + 1] if (indx + 1) < parent.get_children_size() else None

        min_keys = math.ceil((self.__order - 1)/2)  #min rule

        # Borrow from left sibling
        if left_sibling and left_sibling.compare_key_size_at_mode(min_keys, 0):
            # print("\n======Debugger======")
            # print(node.get_keys()) 
            # print("====================\n")   

            if node.is_leaf():
                # Move last key/value from left leaf to front of node
                last_i = left_sibling.get_keys_size() - 1
                key = left_sibling.get_key_at(last_i)
                value = left_sibling.get_child_at(last_i)
                left_sibling.remove_key_at(last_i)
                left_sibling.remove_child_at(last_i)

                node.insert_key_at(0, key)
                node.insert_child_at(0, value)

                parent.set_key_at(indx - 1, node.get_key_at(0)) # Update parent separator to the new first key of node
            else:
                # Internal node borrowing:
                # Move parent's separator down into node, move left_sibling's last key up into parent,
                # and move left_sibling's last child to be node's first child.
                borrow_key_indx = left_sibling.get_keys_size() - 1
                borrow_key = left_sibling.get_key_at(borrow_key_indx)
                # left_sibling's last child index = left_sibling.get_keys_size()
                borrow_child = left_sibling.get_child_at(left_sibling.get_keys_size())

                left_sibling.remove_key_at(borrow_key_indx)
                left_sibling.remove_child_at(left_sibling.get_keys_size())

                # parent separator goes down into node at front
                node.insert_key_at(0, parent.get_key_at(indx - 1))
                node.insert_child_at(0, borrow_child)
                borrow_child.set_parent(node)

                # replace parent's separator with borrow_key
                parent.set_key_at(indx - 1, borrow_key)
            return

        # Borrow from right sibling
        if right_sibling and right_sibling.compare_key_size_at_mode(min_keys, 0):

            # print("\n======Debugger======")
            # print(node.get_keys()) 
            # print("====================\n")   


            if node.is_leaf():
                # Move first key/value from right sibling to end of node
                key = right_sibling.get_key_at(0)
                value = right_sibling.get_child_at(0)
                right_sibling.remove_key_at(0)
                right_sibling.remove_child_at(0)

                node.append_key(key)
                node.append_child(value)

                parent.set_key_at(indx, right_sibling.get_key_at(0))  # Update parent separator  equal right_sibling's new first key
            else:
                # Internal node borrowing from right sibling:
                borrow_key = right_sibling.get_key_at(0)
                borrow_child : BPTreeNode = right_sibling.get_child_at(0)

                right_sibling.remove_key_at(0)
                right_sibling.remove_child_at(0)

                # parent's separator goes down into node as new last key
                node.append_key(parent.get_key_at(indx))
                node.append_child(borrow_child)
                borrow_child.set_parent(node)

                # replace parent's separator with borrow_key
                parent.set_key_at(indx, borrow_key)
            return

        #Merge with sibling if borrowing not possible
        if left_sibling:
            self.__merge_nodes(left_sibling, node, parent, indx - 1) # merge left_sibling (left) with node (right) separator index = indx - 1
        elif right_sibling:            
            self.__merge_nodes(node, right_sibling, parent, indx) # merge node (left) with right_sibling (right); separator index = indx
 

    def __merge_nodes(self, left_node : BPTreeNode, right_node : BPTreeNode, parrent_node : BPTreeNode, sep_indx):
        if left_node.is_leaf():
            for i in range(right_node.get_keys_size()):
                left_node.append_key(right_node.get_key_at(i))
                left_node.append_child(right_node.get_child_at(i))

            # Fix leaf chain
            left_node.set_next(right_node.get_next())
            
        else:# Internal node merge:
            sep_key = parrent_node.get_key_at(sep_indx)         # Bring down separator key from parent into left
            left_node.append_key(sep_key)

            # Append all keys and children from right into left
            for i in range(right_node.get_keys_size()):
                left_node.append_key(right_node.get_key_at(i))\

            for child in right_node.get_children():
                left_node.append_child(child)
                child.set_parent(left_node)

        #Remove Reference from parrent after merge
        parrent_node.remove_key_at(sep_indx)
        parrent_node.remove_child_at(sep_indx + 1)


        # If parent underflows, recurse rebalance
        if parrent_node.is_root() and parrent_node.is_empty():
            # Parent is root and became empty → promote left as new root
            self.__root = left_node
            left_node.set_parent(None)
        elif not parrent_node.is_root() and parrent_node.get_keys_size() < math.ceil((self.__order - 1)/2):
            self.__rebalance(parrent_node)

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