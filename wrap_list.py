#!/usr/bin/env python

try:
    from sys import maxint as MAXINT
except:
    MAXINT = None;

class WraparoundList(list):
    """A list whose index wraps around when out of bounds.

    A `WraparoundList` is the same as an ordinary `list`, 
    except that out-of-bounds indexing causes the index 
    value to wrap around. The wrapping behavior is as if
    after reaching the last element, one returned to the 
    other end of the list and continued counting.

    >>> x = WraparoundList('abcd')
    >>> x
    ['a', 'b', 'c', 'd']
    >>> x[3]
    'd'
    >>> x[4] # wraps to x[0]
    'a'
    >>> x[-6] = 'Q' # wraps to x[-2]
    >>> x
    ['a', 'b', 'Q', 'd']
    >>> del x[7] # wraps to x[3]
    >>> x 
    ['a', 'b', 'Q']

    Indices used in out-of-range slices also wrap around.
    If the slice's `start` or `stop` is out-of-bounds, it 
    gets wrapped around.

    >>> x = WraparoundList('abcd')
    >>> x
    ['a', 'b', 'c', 'd']
    >>> x[:10] # wraps to x[:2]
    ['a', 'b']
    >>> x[-7:3] # wraps to x[-3:3]
    ['b', 'c']

    The one way in which slicing a `WraparoundList` differs 
    from slicing an ordinary `list` is the case of using the
    list length as the upper limit.

    >>> x = WraparoundList('abcd')
    >>> x
    ['a', 'b', 'c', 'd']
    >>> x[2:]
    ['c', 'd']
    >>> x[2:4] # wraps to x[2:0]
    []

    Initializing a `WraparoundList` with a nested iterable
    does not cause inner indices to wrap. To have a multi-
    dimensional `WraparoundList`, all the elements of the 
    outer `WraparoundList` must also be `WraparoundList`s.

    >>> x = WraparoundList([list('abc'), list('def')])
    >>> x
    [['a', 'b', 'c'], ['d', 'e', 'f']]
    >>> x[3]
    ['d', 'e', 'f']
    >>> x[3][5]
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    IndexError: list index out of range
    >>> y = WraparoundList([WraparoundList(i) for i in x])   
    >>> y[3][5]
    'f'
    """
    def __getitem__(self, i):
        """x.__getitem__(i) <=> x[i]"""
        if isinstance(i, slice):
            return list.__getitem__(self, self._wrap_slice(i))
        else:
            return list.__getitem__(self, self._wrap_index(i))

    def __getslice__(self, i, j):
        """x.__getslice__(i, j) <=> x[i:j]"""
        return self.__getitem__(slice(i, j, None))

    def __setitem__(self, i, y):
        """x.__setitem__(i, y) <=> x[i] = y"""
        if isinstance(i, slice):
            list.__setitem__(self, self._wrap_slice(i), y)
        else:
            list.__setitem__(self, self._wrap_index(i), y)

    def __setslice__(self, i, j):
        """x.__setslice__(i, j) <=> x[i:j] = y"""
        self.__setitem__(slice(i, j, None))

    def __delitem__(self, i):
        """x.__delitem__(i, y) <=> del x[i]"""
        if isinstance(i, slice):
            list.__delitem__(self, self._wrap_slice(i))
        else:
            list.__delitem__(self, self._wrap_index(i))

    def __delslice__(self, i, j):
        """x.__delslice__(i, j) <=> del x[i:j]"""
        self.__delitem__(slice(i, j, None))

    def _wrap_index(self, i):
        _len = len(self)
        if i >= _len:
            return i % _len
        elif i < -_len:
            return i % (-_len)
        else:
            return i

    def _wrap_slice(self, slc):
        if slc.start is None:
            start = None
        else:
            start = self._wrap_index(slc.start) 
        if slc.stop is None:
            stop = None
        elif MAXINT is not None and slc.stop == MAXINT:
            # __*slice__ methods treat absent upper bounds as sys.maxint, which would
            # wrap around to a system-dependent (and probably unexpected) value. Setting 
            # to `None` in this case forces the slice to run to the end of the list.
            stop = None
        else:
            stop = self._wrap_index(slc.stop)
        step = slc.step
        return slice(start, stop, step)

def main():
    pass

if __name__ == '__main__':
    main()