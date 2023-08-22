from __future__ import annotations

from collections import deque
from itertools import islice
from typing import TYPE_CHECKING, TypeAlias, Iterable, Iterator


if TYPE_CHECKING:
    TrieDict: TypeAlias = dict[str | bool, 'TrieDict' | str]


def extract_keywords_from_trie(trie: TrieDict) -> Iterator[str]:
    """
    ...

    Examples:

    >>> ...

    :param trie:
    :return:
    """
    nodes = deque([trie])
    while nodes:

        current_node = nodes.popleft()
        for key, val in current_node.items():

            if key is True:
                yield val
            elif isinstance(val, dict):
                nodes.append(val)


class Autocomplete:
    def __init__(self, words: Iterable[str] = (), case_sensitive: bool = False) -> None:
        """
        ...

        Examples:

        >>> Autocomplete()

        :param words:
        :param case_sensitive:
        """
        self.trie: TrieDict = {}
        self.case_sensitive = case_sensitive

        self.insert_words(words=words)

    def insert_words(self, words: Iterable[str]) -> None:
        """
        ...

        Examples:

        >>> ...

        :param words:
        :return:
        """
        if not self.case_sensitive:
            words = (x.lower() for x in words)

        for word in words:
            trie = self.trie
            for c in word:
                trie = trie.setdefault(c, {})

            # add a boolean to mark the last word
            trie[True] = word

    def search_words(self, prefix: str) -> Iterable[str]:
        """
        ...

        Examples:

        >>> ...

        :param prefix:
        :return:
        """
        if not self.case_sensitive:
            prefix = prefix.lower()

        # select the subtree of the trie that begins with that prefix,
        # and start finding the keywords level by level (BFS).
        trie = self.trie
        for c in prefix:
            trie = trie.get(c)

            # if there is no node with that character: return
            if not trie:
                return

        yield from extract_keywords_from_trie(trie=trie)

    def get_words(self, prefix: str, limit: int) -> list[str]:
        """
        ...

        Examples:

        >>> ...

        :param prefix:
        :param limit:
        :return:
        """
        return list(islice(self.search_words(prefix=prefix), limit))
