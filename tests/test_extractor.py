from tagsnip import extractor

PATH = "./docs/example.py"

TEXT = """
# tagsnip-start demo
def main():
    x = 1
    y = 2
    print(x + y)

    return 0
# tagsnip-end demo

if __name__ == "__main__":
    import sys
    sys.exit(main())"""

OUT = """def main():
    x = 1
    y = 2
    print(x + y)

    return 0"""

def test_extract_tagged_block():
    snippet, first_line_num, last_line_num = extractor.extract_tagged_block(TEXT, "demo")
    assert snippet == OUT

def test_extract_from_file():
    snippet, first_line_num, last_line_num = extractor.extract_from_file(PATH, "tag1")
    assert snippet == OUT

def test_missing_start_tag():
    text = """
    hello
    # tagsnip-end 1
    """

    try:
        extractor.extract_tagged_block(text, "1")
        assert False, "Expected TagsnipError"
    except extractor.TagsnipError as err:
        assert str(err) == "Start tag not found for '1'"


def test_missing_end_tag():
    text = """
    # tagsnip-start 1
    hello
    """

    try:
        extractor.extract_tagged_block(text, "1")
        assert False, "Expected TagsnipError"
    except extractor.TagsnipError as err:
        assert str(err) == "End tag not found for '1'"


def test_multiple_start_tags():
    text = """
    # tagsnip-start 1
    hello
    # tagsnip-start 1
    world
    # tagsnip-end 1
    """

    try:
        extractor.extract_tagged_block(text, "1")
        assert False, "Expected TagsnipError"
    except extractor.TagsnipError as err:
        assert str(err) == "Multiple start tags found for '1'"

def test_missing_file():
    try:
        extractor.extract_from_file("./does_not_exist.py", "1")
        assert False, "Expected TagsnipError"
    except extractor.TagsnipError:
        pass

def main():
    test_extract_tagged_block()
    test_extract_from_file()
    test_missing_start_tag()
    test_missing_end_tag()
    test_multiple_start_tags()
    test_missing_file()

if __name__ == "__main__":
    main()
