from typing import Dict, List, Type
import unittest


class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = dict()

    def add(self, k: str):
        if k in self.children:
            return self.children[k]
        self.children[k] = TrieNode()
        return self.children[k]

    def is_leaf(self):
        return 0 == len(self.children)


class Trie:
    def __init__(self):
        self.__root = TrieNode()

    def add(self, addr: str):
        tmp = self.__root
        for i in range(len(addr)):
            c = addr[i]
            tmp = tmp.add(c)

    def __all_leaf(self, n: TrieNode, result: List, prefix: str):
        if n.is_leaf():
            result.append(prefix)
            return
        for k, v in n.children.items():
            self.__all_leaf(v, result, prefix + k)

    def all_ec(self):
        result = []
        self.__all_leaf(self.__root, result, '')
        return result


class TestTrie(unittest.TestCase):
    def test_trie1(self):
        x = Trie()
        x.add('01')
        x.add('001')
        x.add('1')
        x.add('100')
        result = x.all_ec()
        self.assertEqual(len(result), 3)
        self.assertIn('01', result)
        self.assertIn('100', result)
        self.assertIn('001', result)

    def test_trie2(self):
        x = Trie()
        x.add('0000001')
        x.add('1')
        x.add('1')
        x.add('0')
        x.add('100')
        x.add('0')
        result = x.all_ec()
        self.assertEqual(len(result), 2)
        self.assertIn('100', result)
        self.assertIn('0000001', result)

    def test_trie3(self):
        x = Trie()
        x.add('')
        result = x.all_ec()
        self.assertEqual(len(result), 1)
        self.assertIn('', result)


if __name__ == "__main__":
    unittest.main()
