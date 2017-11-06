from __future__ import print_function, division

import heapq
import itertools

class Node:
    @staticmethod
    def from_symbol(symbol, freq):
        new_node = Node()
        new_node.symbol = symbol
        new_node.left_child = new_node.right_child = None
        new_node.freq = freq
        return new_node

    @staticmethod
    def from_nodes(left_node, right_node):
        new_node = Node()
        new_node.symbol = None
        new_node.left_node = left_node
        new_node.right_node = right_node
        new_node.freq = left_node.freq + right_node.freq
        return new_node

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return str((self.symbol, self.freq))

    def _codes(self, parent_code, code_list):
        if self.symbol is None:
            self.left_node._codes(parent_code + [0], code_list)
            self.right_node._codes(parent_code + [1], code_list)
        else:
            code_list.append((self.symbol, parent_code))

    def codes(self):
        code_list = []
        self._codes([], code_list)
        return code_list

def compression_ratio(freqs, codes):
    uncompressed_size = 8 * sum(map((lambda char: char[1]), freqs.items()))
    compressed_size = sum(map((lambda code: len(code[1]) * freqs[code[0]]), codes))
    return uncompressed_size / compressed_size

def test_prefixes(codes):
    for code1, code2 in itertools.product(codes, codes):
        if code1 == code2[:len(code1)]:
            print(code1)
            print(code2)
            raise Exception('AAAAAAA')

def test(text):
    freqs = {}
    for char in text:
        if char not in freqs:
            freqs[char] = 1
        else:
            freqs[char] += 1
    heap = [Node.from_symbol(char, freq) for char, freq in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left_node = heapq.heappop(heap)
        right_node = heapq.heappop(heap)
        parent = Node.from_nodes(left_node, right_node)
        heapq.heappush(heap, parent)
    codes = sorted(heap[0].codes(), key=lambda x: len(x[1]))
    #test_prefixes(map(lambda x: x[1], codes))
    for code in codes:
        print(code)
    print('Odnos kompresije: ' + str(compression_ratio(freqs, codes)))


#test('Algoritam Shannon - Fanovog kodiranja je jednostavan za implementirati.')
test('algoritam shannon fanovog kodiranja je jednostavan za implementirati.')
#test('EACAEAABAAEDAEA')
#test('Da bi student mogao implementirati algoritam potrebno je da procita predavanja iz predmeta MMS.')
#test('Za svaku od ovih recenica potrebno je izracunati stepen kompresije ako se za nekomprimirani tekst koristi bitna reprezentacija ASCII vrijednosti simbola.')
