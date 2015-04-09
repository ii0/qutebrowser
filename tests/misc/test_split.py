# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2014-2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for qutebrowser.misc.split."""

import pytest

from qutebrowser.misc import split


# Most tests copied from Python's shlex.
# The original test data set was from shellwords, by Hartmut Goebel.

# Format: input/split|output|without|keep/split|output|with|keep/

test_data = r"""
one two/one|two/one| two/
one "two three" four/one|two three|four/one| "two three"| four/
one 'two three' four/one|two three|four/one| 'two three'| four/
one "two\" three" four/one|two" three|four/one| "two\" three"| four/
one 'two'\'' three' four/one|two' three|four/one| 'two'\'' three'| four/
one "two three/one|two three/one| "two three/
one 'two three/one|two three/one| 'two three/
one\/one\/one\/
one "two\/one|two\/one| "two\/
one /one/one| /
open -t i/open|-t|i/open| -t| i/
foo bar/foo|bar/foo| bar/
 foo bar/foo|bar/ foo| bar/
 foo bar /foo|bar/ foo| bar| /
foo   bar    bla     fasel/foo|bar|bla|fasel/foo|   bar|    bla|     fasel/
x y  z              xxxx/x|y|z|xxxx/x| y|  z|              xxxx/
\x bar/x|bar/\x| bar/
\ x bar/ x|bar/\ x| bar/
\ bar/ bar/\ bar/
foo \x bar/foo|x|bar/foo| \x| bar/
foo \ x bar/foo| x|bar/foo| \ x| bar/
foo \ bar/foo| bar/foo| \ bar/
foo "bar" bla/foo|bar|bla/foo| "bar"| bla/
"foo" "bar" "bla"/foo|bar|bla/"foo"| "bar"| "bla"/
"foo" bar "bla"/foo|bar|bla/"foo"| bar| "bla"/
"foo" bar bla/foo|bar|bla/"foo"| bar| bla/
foo 'bar' bla/foo|bar|bla/foo| 'bar'| bla/
'foo' 'bar' 'bla'/foo|bar|bla/'foo'| 'bar'| 'bla'/
'foo' bar 'bla'/foo|bar|bla/'foo'| bar| 'bla'/
'foo' bar bla/foo|bar|bla/'foo'| bar| bla/
blurb foo"bar"bar"fasel" baz/blurb|foobarbarfasel|baz/blurb| foo"bar"bar"fasel"| baz/
blurb foo'bar'bar'fasel' baz/blurb|foobarbarfasel|baz/blurb| foo'bar'bar'fasel'| baz/
""//""/
''//''/
foo "" bar/foo||bar/foo| ""| bar/
foo '' bar/foo||bar/foo| ''| bar/
foo "" "" "" bar/foo||||bar/foo| ""| ""| ""| bar/
foo '' '' '' bar/foo||||bar/foo| ''| ''| ''| bar/
\"/"/\"/
"\""/"/"\""/
"foo\ bar"/foo\ bar/"foo\ bar"/
"foo\\ bar"/foo\ bar/"foo\\ bar"/
"foo\\ bar\""/foo\ bar"/"foo\\ bar\""/
"foo\\" bar\"/foo\|bar"/"foo\\"| bar\"/
"foo\\ bar\" dfadf"/foo\ bar" dfadf/"foo\\ bar\" dfadf"/
"foo\\\ bar\" dfadf"/foo\\ bar" dfadf/"foo\\\ bar\" dfadf"/
"foo\\\x bar\" dfadf"/foo\\x bar" dfadf/"foo\\\x bar\" dfadf"/
"foo\x bar\" dfadf"/foo\x bar" dfadf/"foo\x bar\" dfadf"/
\'/'/\'/
'foo\ bar'/foo\ bar/'foo\ bar'/
'foo\\ bar'/foo\\ bar/'foo\\ bar'/
"foo\\\x bar\" df'a\ 'df"/foo\\x bar" df'a\ 'df/"foo\\\x bar\" df'a\ 'df"/
\"foo/"foo/\"foo/
\"foo\x/"foox/\"foo\x/
"foo\x"/foo\x/"foo\x"/
"foo\ "/foo\ /"foo\ "/
foo\ xx/foo xx/foo\ xx/
foo\ x\x/foo xx/foo\ x\x/
foo\ x\x\"/foo xx"/foo\ x\x\"/
"foo\ x\x"/foo\ x\x/"foo\ x\x"/
"foo\ x\x\\"/foo\ x\x\/"foo\ x\x\\"/
"foo\ x\x\\""foobar"/foo\ x\x\foobar/"foo\ x\x\\""foobar"/
"foo\ x\x\\"\'"foobar"/foo\ x\x\'foobar/"foo\ x\x\\"\'"foobar"/
"foo\ x\x\\"\'"fo'obar"/foo\ x\x\'fo'obar/"foo\ x\x\\"\'"fo'obar"/
"foo\ x\x\\"\'"fo'obar" 'don'\''t'/foo\ x\x\'fo'obar|don't/"foo\ x\x\\"\'"fo'obar"| 'don'\''t'/
"foo\ x\x\\"\'"fo'obar" 'don'\''t' \\/foo\ x\x\'fo'obar|don't|\/"foo\ x\x\\"\'"fo'obar"| 'don'\''t'| \\/
'foo\ bar'/foo\ bar/'foo\ bar'/
'foo\\ bar'/foo\\ bar/'foo\\ bar'/
foo\ bar/foo bar/foo\ bar/
:-) ;-)/:-)|;-)/:-)| ;-)/
áéíóú/áéíóú/áéíóú/
"""

test_data_lines = test_data.strip().splitlines()


class TestSplit:

    """Test split."""

    @pytest.mark.parametrize('cmd, out',
                             [case.split('/')[:-2]
                              for case in test_data_lines])
    def test_split(self, cmd, out):
        """Test splitting."""
        items = split.split(cmd)
        assert items == out.split('|')

    @pytest.mark.parametrize('cmd',
                             [case.split('/')[0]
                              for case in test_data_lines])
    def test_split_keep_original(self, cmd):
        """Test if splitting with keep=True yields the original string."""
        items = split.split(cmd, keep=True)
        assert ''.join(items) == cmd

    @pytest.mark.parametrize('cmd, _mid, out',
                             [case.split('/')[:-1]
                              for case in test_data_lines])
    def test_split_keep(self, cmd, _mid, out):
        """Test splitting with keep=True."""
        items = split.split(cmd, keep=True)
        assert items == out.split('|')


class TestSimpleSplit:

    """Test simple_split."""

    TESTS = {
        ' foo bar': [' foo', ' bar'],
        'foobar': ['foobar'],
        '   foo  bar baz  ': ['   foo', '  bar', ' baz', '  '],
        'f\ti\ts\th': ['f', '\ti', '\ts', '\th'],
        'foo\nbar': ['foo', '\nbar'],
    }

    @pytest.mark.parametrize('test', TESTS)
    def test_str_split(self, test):
        """Test if the behavior matches str.split."""
        assert split.simple_split(test) == test.rstrip().split()

    def test_str_split_maxsplit_1(self):
        """Test if the behavior matches str.split with maxsplit=1."""
        s = "foo bar baz"
        actual = split.simple_split(s, maxsplit=1)
        expected = s.rstrip().split(maxsplit=1)
        assert actual == expected

    def test_str_split_maxsplit_0(self):
        """Test if the behavior matches str.split with maxsplit=0."""
        s = "  foo bar baz  "
        actual = split.simple_split(s, maxsplit=0)
        expected = s.rstrip().split(maxsplit=0)
        assert actual == expected

    @pytest.mark.parametrize('test, expected', TESTS.items())
    def test_split_keep(self, test, expected):
        """Test splitting with keep=True."""
        assert split.simple_split(test, keep=True) == expected
