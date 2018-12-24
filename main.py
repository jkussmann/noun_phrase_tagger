"""
This module is used to call the functions of the noun phrase tagger
"""

import sys
from sys import executable

import socket
import time

from subprocess import Popen, CREATE_NEW_CONSOLE

import noun_phrase_tagger as npt


def get_input():
    """
    This function gets the input from the user
    """
    line = ""

    # Start the Stanford CoreNLP server if it isn't running
    result = core_nlp_status()
    if result != 0:
        Popen(
            [executable, "core_nlp.py"],
            cwd="c:\stanford-corenlp-full-2018-02-27",
            creationflags=CREATE_NEW_CONSOLE,
        )
        print(
            "Initializing CoreNLP...."
        )  # Give CoreNLP some time to get going before accepting input.
        time.sleep(30)

    try:
        while line != "end":
            line = input("\r\n" + "Enter a sentence: ")
            if line == "end":
                print("Ending Program ...")
                sys.exit()
            else:
                print("")
                print("Stanford Noun Phrases: ")
                formatted_string = ", ".join(
                    [str(np) for np in npt.get_stanford_nps(line)]
                )
                print(formatted_string)
                print("")
                print("NLTK Noun Phrases: ")
                formatted_string = ", ".join([str(np) for np in npt.get_nltk_nps(line)])
                print(formatted_string)
                print("")
                print("Spacy Noun Phrases: ")
                formatted_string = ", ".join(
                    [str(np) for np in npt.get_spacy_nps(line)]
                )
                print(formatted_string)
                print("")
                print("Consolidated Noun Phrases: ")
                formatted_string = ", ".join(
                    [str(np) for np in npt.get_noun_phrases(line)]
                )
                print(formatted_string)

    except KeyboardInterrupt:
        sys.exit()


def core_nlp_status():
    """
    This function gets the status of Stanford core NLP
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("localhost", 9000))

    return result


def main():
    """
	This is the main entry point for the program
	"""

    get_input()


if __name__ == "__main__":
    main()
