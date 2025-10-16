import heapq
import os
import math
import time
import shutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ============================
# Node for Huffman Tree
# ============================
class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq


# ============================
# Step 1 — Frequency Table
# ============================
def get_freq(text):
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


# ============================
# Step 2 — Build Huffman Tree
# ============================
def build_tree(text):
    freq = get_freq(text)
    heap = [Node(ch, fr) for ch, fr in freq.items()]
    heapq.heapify(heap)
    if not heap:
        return None
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, Node(None, a.freq + b.freq, a, b))
    return heap[0]


# ============================
# Step 3 — Generate Huffman Codes
# ============================
def get_codes(node, prefix="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if not node:
        return {}
    if node.ch is not None:
        code_dict[node.ch] = prefix or "0"
    else:
        get_codes(node.left, prefix + "0", code_dict)
        get_codes(node.right, prefix + "1", code_dict)
    return code_dict


# ============================
# Step 4 — Encode & Decode
# ============================
def encode(text, code_dict):
    return ''.join(code_dict[ch] for ch in text)

def decode(encoded, code_dict):
    inv = {v: k for k, v in code_dict.items()}
    buf, dec = "", ""
    for bit in encoded:
        buf += bit
        if buf in inv:
            dec += inv[buf]
            buf = ""
    return dec


# ============================
# Step 5 — Process each file
# ============================
def run_huffman(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"\nProcessing: {filename} ({len(text)} chars)")
    if not text.strip():
        print("⚠️ Skipping empty file.")
        return None

    # Folder setup
    base_name = os.path.splitext(os.path.basename(filename))[0]
    folder = os.path.join(os.getcwd(), base_name)
    os.makedirs(folder, exist_ok=True)

    # Copy original text inside folder
    shutil.copy(filename, os.path.join(folder, os.path.basename(filename)))

    # Build Huffman
    freq = get_freq(text)
    start = time.time()
    tree = build_tree(text)
    code_dict = get_codes(tree)
    encoded = encode(text, code_dict)
    decoded = decode(encoded, code_dict)
    end = time.time()

    ok = decoded == text
    uniq = len(freq)
    ascii_bits = len(text) * 8
    fixed_bits = len(text) * math.ceil(math.log2(uniq))
    huff_bits = len(encoded)
    runtime = end - start
    ratio_ascii = huff_bits / ascii_bits
    ratio_fixed = huff_bits / fixed_bits

    # Save encoded text
    with open(os.path.join(folder, f"encoded_{base_name}.txt"), "w", encoding="utf-8") as f:
        f.write(encoded)

    # Frequency–Length table
    rows = []
    for ch, fr in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        show = "\\n" if ch == "\n" else (f"CTRL({ord(ch)})" if ord(ch) < 32 or ord(ch) == 127 else ch)
        code = code_dict.get(ch, "")
        rows.append([show, fr, len(code), code])
    df = pd.DataFrame(rows, columns=["Character", "Frequency", "Code Length", "Huffman Code"])

    # Save frequency-length table image
    fig_h = max(2, 0.4 * len(df))
    fig, ax = plt.subplots(figsize=(8, fig_h))
    ax.axis("off")
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)
    ax.set_title(f"Frequency–Code Length Table — {base_name}\n(Runtime: {runtime:.4f}s | Unique Chars: {uniq})",
                 fontsize=11, weight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(folder, f"freq_length_table_{base_name}.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # Local compression summary (bar)
    labels = ["ASCII (8 bits)", "Fixed-Length", "Huffman"]
    values = [ascii_bits, fixed_bits, huff_bits]
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=["skyblue", "orange", "lightgreen"])
    plt.ylabel("Total Bits Used")
    plt.title(f"Compression Summary — {base_name}\nRuntime: {runtime:.4f}s")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, f"compression_summary_{base_name}.png"), dpi=300)
    plt.close()

    # Local summary text
    with open(os.path.join(folder, f"summary_{base_name}.txt"), "w", encoding="utf-8") as f:
        f.write(f"=== Huffman Compression Summary: {base_name} ===\n\n")
        f.write(f"File size: {len(text)} characters\n")
        f.write(f"Unique characters: {uniq}\n")
        f.write(f"Runtime: {runtime:.4f} seconds\n")
        f.write(f"Decoded correctly: {ok}\n\n")
        f.write(f"ASCII bits: {ascii_bits:,}\n")
        f.write(f"Fixed bits: {fixed_bits:,}\n")
        f.write(f"Huffman bits: {huff_bits:,}\n\n")
        f.write(f"Compression ratio (Huffman/ASCII): {ratio_ascii:.4f}\n")
        f.write(f"Compression ratio (Huffman/Fixed): {ratio_fixed:.4f}\n")

    return {
        "file": base_name,
        "ascii_bits": ascii_bits,
        "fixed_bits": fixed_bits,
        "huffman_bits": huff_bits,
        "runtime": runtime,
        "ratio_ascii": ratio_ascii,
        "ratio_fixed": ratio_fixed,
        "decoded_ok": ok
    }


# ============================
# Step 6 — Compile all results
# ============================
if __name__ == "__main__":
    files = ["alice29.txt", "pride_prej.txt", "DNA_sequence.txt", "wiki_huff.txt", "sample_user.txt"]
    summaries = [run_huffman(f) for f in files if os.path.exists(f)]
    summaries = [s for s in summaries if s]

    if not summaries:
        print("\nNo valid files processed.")
        exit()

    # --- make global summary folder ---
    compiled_folder = os.path.join(os.getcwd(), "compiled_summaries")
    os.makedirs(compiled_folder, exist_ok=True)

    # --- Overall compression bar chart ---
    x = np.arange(len(summaries))
    width = 0.25
    plt.figure(figsize=(10, 5))
    plt.bar(x - width, [s["ascii_bits"] for s in summaries], width, label="ASCII (8 bits)", alpha=0.6)
    plt.bar(x, [s["fixed_bits"] for s in summaries], width, label="Fixed-Length", alpha=0.7)
    plt.bar(x + width, [s["huffman_bits"] for s in summaries], width, label="Huffman", alpha=0.8)
    plt.xticks(x, [s["file"] for s in summaries])
    plt.ylabel("Total Bits Used")
    plt.xlabel("Dataset")
    plt.title("Compression Comparison Across Files")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(compiled_folder, "compression_summary.png"), dpi=300)
    plt.close()

    # --- Summary table across datasets ---
    headers = [
        "File", "ASCII Bits", "Fixed Bits", "Huffman Bits", "Time (s)",
        "Huffman/ASCII", "Huffman/Fixed", "Decoded OK"
    ]
    data = [[
        s["file"], f"{s['ascii_bits']:,}", f"{s['fixed_bits']:,}", f"{s['huffman_bits']:,}",
        f"{s['runtime']:.4f}", f"{s['ratio_ascii']:.4f}", f"{s['ratio_fixed']:.4f}", s["decoded_ok"]
    ] for s in summaries]

    fig_h = 2 + len(summaries) * 0.6
    fig, ax = plt.subplots(figsize=(12, fig_h))
    ax.axis("off")
    table = ax.table(cellText=data, colLabels=headers, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.1, 1.3)
    for k, cell in table.get_celld().items():
        if k[0] == 0:
            cell.set_text_props(weight="bold")
    ax.set_title("Huffman Compression Summary Table", fontsize=13, weight="bold", pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(compiled_folder, "summary_table.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # --- Save CSV summary for analysis ---
    pd.DataFrame(summaries).to_csv(os.path.join(compiled_folder, "summary_data.csv"), index=False)

    print("\n✅ Generated:")
    print(" - compiled_summaries/compression_summary.png")
    print(" - compiled_summaries/summary_table.png")
    print(" - compiled_summaries/summary_data.csv")
    print(" - Individual dataset folders with:")
    print("     * Original text, Encoded text")
    print("     * Frequency–length table")
    print("     * Compression summary chart")
    print("     * Summary text file")
