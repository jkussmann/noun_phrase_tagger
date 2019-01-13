"""
Unit tests for the noun phrase tagger
"""

import unittest
import warnings
from sys import executable
import socket
import time
from subprocess import Popen, CREATE_NEW_CONSOLE
from noun_phrase_tagger import (
    get_stanford_nps,
    get_spacy_nps,
    get_nltk_nps,
    get_noun_phrases,
)


def ignore_warnings(test_func):
    """
    Function to ignore test warnings that are not relevant
    """

    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)

    return do_test


class TestNP(unittest.TestCase):
    """
    Class for testing noun phrase tagging functions
    """

    @ignore_warnings
    def test_stanford(self):
        """
        Test for Stanford function.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("localhost", 9000))

        if result != 0:
            Popen(
                [executable, "core_nlp.py"],
                cwd="c:\stanford-corenlp-full-2018-02-27",
                creationflags=CREATE_NEW_CONSOLE,
            )
            print(
                "Initializing CoreNLP...."
            )  # Give CoreNLP some time to get going before accepting input.
            time.sleep(120)

        self.assertEqual(
            get_stanford_nps(
                "The little yellow dog chased the boy in the red car."
            ),
            ['The little yellow dog', 'the boy', 'the red car'],
        )
        sock.close()

    @ignore_warnings
    def test_spacy(self):
        """
        Test for Spacy
        """
        self.assertEqual(
            get_spacy_nps(
                "The little yellow dog chased the boy in the red car."
            ),
            ['The little yellow dog', 'the boy', 'the red car'],
        )

    @ignore_warnings
    def test_nltk(self):
        """
        Test for NLTK
        """
        self.assertEqual(
            get_nltk_nps(
                "The little yellow dog chased the boy in the red car."
            ),
            ['The little yellow dog', 'the boy', 'the red car'],
        )

    @ignore_warnings
    def test_consolidated(self):
        """
        Test for the consolidation function
        """
        self.assertEqual(
            get_noun_phrases(
                "The little yellow dog chased the boy in the red car."
            ),
            ['The little yellow dog', 'the boy', 'the red car'],
        )


if __name__ == "__main__":
    unittest.main()
