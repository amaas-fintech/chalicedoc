"""Unit tests."""
import os
import sys

import chalicedoc


def test_get_doc_content():
    """Test get_doc_content for correct doc + line numbers."""
    tests = [
        ('create_user', 11, 33),
        ('get_user', 9, 52),
        ('no_doc', 0, None),
        ('xref', 7, 72),
    ]
    pdir = os.path.join(os.path.dirname(__file__), 'test-project', 'sample')
    fname = os.path.join(pdir, 'app.py')
    sys.path.insert(0, pdir)
    try:
        with chalicedoc.isolated_import('app') as app:
            for name, linecount, startline in tests:
                func = getattr(app, name)
                block = chalicedoc.get_doc_content(func)
                block.pprint()
                assert len(block) == linecount
                if startline is not None:
                    assert block.info(0) == (fname, startline)

    finally:
        sys.path.pop(0)
