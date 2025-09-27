from B_plus_Tree import BPTree

def test_bptree():
    print("=== B+ Tree Test ===")
    order = 3
    bptree = BPTree(order)

    # ---------------------------
    # Insertion tests
    # ---------------------------
    data = [
        (5, "A"),
        (10, "B"),
        (15, "C"),
        (20, "D"),
        (25, "E"),
        (30, "F"),
        (3, "G"),
        (8, "H"),
    ]

    for key, value in data:
        print(f"\nInsert ({key}, {value})")
        bptree.insert(key, value)
        # bptree.display_tree_ascii()
        # print("Leaves horizontal:")
        # bptree.display_leaves_horizontal()

    # ---------------------------
    # Search tests
    # ---------------------------
    # search_keys = [3, 8, 10, 25, 100]
    # print("\n=== Search Test ===")
    # for key in search_keys:
    #     result = bptree.search(key)
    #     print(f"Search {key}: {result}")

    # ---------------------------
    # Deletion tests
    # ---------------------------
    print("\n=== Deletion Test ===")

    print("Before")
    bptree.display_tree_ascii()


    delete_keys = [10, 25, 5, 3]  # includes merges and borrows
    for key in delete_keys:
        print(f"\nDelete {key}")
        bptree.delete(key)
        bptree.display_tree_ascii()
        print("Leaves horizontal:")
        bptree.display_leaves_horizontal()


if __name__ == "__main__":
    test_bptree()
