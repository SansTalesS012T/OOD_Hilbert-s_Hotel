from B_plus_Tree import BPTree

def test_bptree():
    print("=== B+ Tree Test ===")
    order = 4
    bptree = BPTree(order)

    # Insert some key/value pairs
    data = [
        (5, "A"),
        (10, "B"),
        (15, "C"),
        (20, "D"),
        (25, "E"),
        (30, "F"),
        (3, "G"),
        (8, "H")
    ]

    for key, value in data:
        print(f"\nInsert ({key}, {value})")
        bptree.insert(key, value)
        bptree.display_tree_ascii()
        print("Leaves horizontal:")
        bptree.display_leaves_horizontal()

    # Test search
    search_keys = [5, 15, 25, 100]
    print("\n=== Search Test ===")
    for key in search_keys:
        result = bptree.search(key)
        print(f"Search {key}: {result}")

if __name__ == "__main__":
    test_bptree()

#     Something Like This
#            [15]
#          /      \
#    [5,10]       [15,20,25]
#    ["A","B"]    ["C","D","E"]


# The Child of leaf node contain the value of key