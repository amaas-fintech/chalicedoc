"""Unit tests."""
import os.path
import sys

import chalicedoc


def test_get_content():
    """Test get_content for correct doc + line numbers."""
    tests = [
        ('create_user', 30, 11, 33),
        ('get_user', 48, 9, 52),
        ('no_doc', 65, 0, None),
        ('xref', 71, 7, 73),
    ]
    pdir = os.path.join(os.path.dirname(__file__), 'test-project', 'sample')
    fname = os.path.join(pdir, 'app.py')
    sys.path.insert(0, pdir)
    try:
        with chalicedoc.isolated_import('app') as app:
            for name, defline, linecount, startline in tests:
                func = getattr(app, name)
                src, doc = chalicedoc.get_content(func)
                src.pprint()
                assert src.info(0) == (fname, defline)
                doc.pprint()
                assert len(doc) == linecount
                if startline is not None:
                    assert doc.info(0) == (fname, startline)

    finally:
        sys.path.pop(0)
