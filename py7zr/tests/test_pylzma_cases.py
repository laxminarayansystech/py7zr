import py7zr
import os
from py7zr.tests import utils


testdata_path = os.path.join(os.path.dirname(__file__), 'data')

def test_archive():
    test_archive_files = ['non_solid.7z',  'solid.7z']
    for f in test_archive_files:
        archive = py7zr.Archive(open(os.path.join(testdata_path, '%s' % f), 'rb'))
        utils.check_archive(archive)

def test_copy():
    # test loading of copy compressed files
    utils.check_archive(py7zr.Archive(open(os.path.join(testdata_path,'copy.7z'),'rb')))


def test_empty():
    # decompress empty archive
    archive = py7zr.Archive(open(os.path.join(testdata_path,'empty.7z'), 'rb'))
    assert archive.getnames() == []

def test_github_14():
    archive = py7zr.Archive(open(os.path.join(testdata_path, 'github_14.7z'), 'rb'))
    assert archive.getnames() == ['github_14']
    cf = archive.getmember('github_14')
    assert cf != None
    data = cf.read()
    assert len(data) == cf.uncompressed
    assert data == bytes('Hello GitHub issue #14.\n', 'ascii')
    # accessing by name returns an arbitrary compressed streams
    # if both don't have a name in the archive
    archive = py7zr.Archive(open(os.path.join(testdata_path, 'github_14_multi.7z'), 'rb'))
    assert archive.getnames() == ['github_14_multi', 'github_14_multi']
    cf = archive.getmember('github_14_multi')
    assert cf != None
    data = cf.read()
    assert len(data) == cf.uncompressed
    assert (data in (bytes('Hello GitHub issue #14 1/2.\n', 'ascii'), bytes('Hello GitHub issue #14 2/2.\n', 'ascii'))) == True
    # accessing by index returns both values
    cf = archive.getmember(0)
    assert cf != None
    data = cf.read()
    assert len(data) == cf.uncompressed
    assert data == bytes('Hello GitHub issue #14 1/2.\n', 'ascii')
    cf = archive.getmember(1)
    assert cf != None
    data = cf.read()
    assert len(data) == cf.uncompressed
    assert data == bytes('Hello GitHub issue #14 2/2.\n', 'ascii')

def test_github_37():
    archive = py7zr.Archive(open(os.path.join(testdata_path, 'github_37_dummy.7z'), 'rb'))
    utils.check_archive(archive)

def _test_umlaut_archive(filename):
    archive = py7zr.Archive(open(os.path.join(testdata_path, filename), 'rb'))
    assert sorted(archive.getnames()) == ['t\xe4st.txt']
    assert archive.getmember('test.txt') == None
    cf = archive.getmember('t\xe4st.txt')
    assert cf.read() == bytes('This file contains a german umlaut in the filename.', 'ascii')
    cf.reset()
    assert cf.read() == bytes('This file contains a german umlaut in the filename.', 'ascii')

def test_non_solid_umlaut():
    # test loading of a non-solid archive containing files with umlauts
    _test_umlaut_archive('umlaut-non_solid.7z')

def test_solid_umlaut():
    # test loading of a solid archive containing files with umlauts
    _test_umlaut_archive('umlaut-solid.7z')