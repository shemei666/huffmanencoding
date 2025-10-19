import heapq


class Node:
    """
    Represents a node in the Huffman tree.
    """

    def __init__(self, char, freq, left, right):
        """
        Initializes a Node.

        :param char: The character the node represents (None for internal nodes).
        :param freq: The frequency (weight) of the character or subtree.
        :param left: The left child node.
        :param right: The right child node.
        """
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, o):
        """
        Comparison method used by the heapq module.
        Nodes are compared based on their frequency (for min-heap behavior).

        :param o: The other node to compare against.
        :return: True if this node's frequency is less than the other node's frequency.
        """
        return self.freq < o.freq

    def __str__(self):
        """
        String representation of the node for debugging.
        Shows the character if it's a leaf node, or the structure of its children if it's an internal node.
        """
        if self.char:
            return self.char
        return f"[{self.left.__str__()},{self.right.__str__()}]"


def get_frequency_table(text):
    """
    Calculates the frequency of each character in the text and creates a min-heap
    of leaf Node objects, one for each unique character.

    :param text: The input string.
    :return: A min-heap (list) of Node objects sorted by frequency.
    """
    freq_dict = {}
    heap = []
    # Count character frequencies
    for char in text:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
    return freq_dict


def huffman_tree(text):
    """
    Constructs the full Huffman tree from the input text.

    :param text: The input string.
    :return: The root Node of the final Huffman tree, or None if the text is empty.
    """
    # Creates frequency table then heapifies it.
    min_heap = get_frequencytable(text)
    heapq.heapify(min_heap)
    if not min_heap:
        return None  # Handle empty input text

    # Continue until only the root node remains in the heap
    while len(min_heap) > 1:
        # 1. Extract the two nodes with the minimum frequencies
        l1 = heapq.heappop(min_heap)
        l2 = heapq.heappop(min_heap)
        # 2. Create a new internal node
        # The new node's frequency is the sum of the two extracted nodes' frequencies.
        # It has no character and its children are l1 and l2.
        new_node = Node("", l1.freq + l2.freq, l1, l2)
        # 3. Insert the new internal node back into the heap
        heapq.heappush(min_heap, new_node)

    # The last remaining node is the root of the Huffman tree
    return min_heap[0]


def huffman_dict(node):
    """
    Generates the Huffman coding dictionary from the constructed Huffman tree
    using a recursive approach.

    :param node: The current node in the tree (starts with the root).
    :return: A dictionary mapping characters to their Huffman codes (e.g., {'a': '101', 'b': '0'}).
    """
    # Base case: If it's a leaf node, the code is an empty string (to be concatenated later)
    if node.char:
        return {node.char: ""}

    # Recursive step: Combine dictionaries from left and right children
    # Codes for the left child are prefixed with '0'
    # Codes for the right child are prefixed with '1'
    return {
        **{char: "0" + code for char, code in huffman_dict(node.left).items()},
        **{char: "1" + code for char, code in huffman_dict(node.right).items()},
    }


def huffman_encode(text, dict):
    """
    Encodes the input text using the provided Huffman coding dictionary.

    :param text: The original string to encode.
    :param dict: The Huffman code dictionary (char -> code).
    :return: The encoded binary string.
    """
    encoded = ""
    for char in text:
        # Append the code for each character
        encoded += dict[char]
    return encoded


def huffman_decode(code, dict):
    """
    Decodes a Huffman encoded binary string using the coding dictionary.

    :param code: The encoded binary string.
    :param dict: The Huffman code dictionary (char -> code).
    :return: The decoded original string.
    """
    # Invert the dictionary for fast lookup of code -> char
    invert_dict = {value: key for key, value in dict.items()}
    decoded = ""
    buffer = ""
    # Iterate through the encoded binary string bit by bit
    for bit in code:
        buffer += bit
        # Check if the current buffer matches a valid Huffman code
        if buffer in invert_dict:
            # If a match is found, append the corresponding character
            decoded += invert_dict[buffer]
            # Reset the buffer for the next character's code
            buffer = ""
    return decoded


tree = huffman_tree(t)
print(tree)


dict = huffman_dict(tree)
print(dict)

encoded = huffman_encode(t, dict)
print(encoded, len(encoded))
decoded = huffman_decode(encoded, dict)
# print(decoded)
