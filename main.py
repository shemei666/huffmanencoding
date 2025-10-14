import heapq


class Node:
    def __init__(self, char, freq, left, right):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, o):
        return self.freq < o.freq

    def __str__(self):
        if self.char:
            return self.char
        return f"[{self.left.__str__()},{self.right.__str__()}]"


with open("alice29.txt", "r") as f:
    t = f.read()


def get_frequency_heap(text):
    freq_dict = {}
    heap = []
    for char in text:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
    for char, freq in freq_dict.items():
        node = Node(char, freq, None, None)
        heapq.heappush(heap, node)
    return heap


def huffman_tree(text):
    min_heap = get_frequency_heap(text)
    if not min_heap:
        return None
    while len(min_heap) > 1:
        l1 = heapq.heappop(min_heap)
        l2 = heapq.heappop(min_heap)
        new_node = Node("", l1.freq + l2.freq, l1, l2)
        heapq.heappush(min_heap, new_node)

    return min_heap[0]


def huffman_dict(node):
    if node.char:
        return {node.char: ""}
    return {
        **{char: "1" + code for char, code in huffman_dict(node.left).items()},
        **{char: "0" + code for char, code in huffman_dict(node.right).items()},
    }


def huffman_encode(text, dict):
    encoded = ""
    for char in text:
        encoded += dict[char]
    return encoded


def huffman_decode(code, dict):
    invert_dict = {value: key for key, value in dict.items()}
    decoded = ""
    buffer = ""
    for bit in code:
        buffer += bit
        if buffer in invert_dict:
            decoded += invert_dict[buffer]
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
