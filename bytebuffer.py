#!/usr/bin/env python
# vim: fileencoding=utf-8 et ts=4 sts=4 sw=4 tw=0 fdm=marker fmr=#{,#}

from io import BytesIO


class ByteBuffer(object):  #{
    """ A buffer object for convenient parsing
    """
    def __init__(self, data=b'', max_size=16384):  #{
        """
        >>> a = ByteBuffer()
        >>> a._total == 0
        True
        >>> a._pos == 0
        True
        >>> a = ByteBuffer(b'abcdef')
        >>> a._total == 6
        True
        >>> a._pos == 0
        True
        """
        assert isinstance(data, bytes)
        self._pos   = 0
        self._total = len(data)
        self._max   = max_size
        self._bytes = BytesIO(data)
    #}
    def __len__(self):  #{
        """
        >>> len(ByteBuffer()) == 0
        True
        >>> len(ByteBuffer(b'abc')) == 3
        True
        """
        return self._total - self._pos
    #}
    def __repr__(self):  #{
        """
        >>> a = ByteBuffer(b'abc')
        >>> a
        <ByteBuffer size=3, total=3>
        >>> a.consume(2)
        >>> a
        <ByteBuffer size=1, total=3>
        """
        return '<%s size=%s, total=%s>' % \
               (self.__class__.__name__, len(self), self._total)
    #}

    def read(self, size=None, consume=False):  #{
        """
        >>> ByteBuffer().read() == b''
        True
        >>> a = ByteBuffer(b'abcdef')
        >>> a.read() == b'abcdef'
        True
        >>> a.read(3) == b'abc'
        True
        >>> a.read(4) == b'abcd'
        True
        >>> a.read(100) == b'abcdef'
        True
        >>> a.read(4, consume=True) == b'abcd'
        True
        >>> a.read(100, consume=True) == b'ef'
        True
        >>> a.read(consume=True) == b''
        True
        """
        _bytes = self._bytes
        _bytes.seek(self._pos)
        data = _bytes.read(size)
        if consume:
            self.consume(size)
        return data
    #}
    def read_until(self, delim, consume=False):  #{
        """
        >>> a = ByteBuffer()
        >>> a.read_until(b'\\r\\n') is None
        True
        >>> a.write(b'abcdef') == 6
        True
        >>> a.read_until(b'\\r\\n') is None
        True
        >>> a.write(b'123\\r\\n') == 5
        True
        >>> a.read_until(b'\\r\\n') == b'abcdef123'
        True
        >>> a.read_until(b'\\r\\n', consume=True) == b'abcdef123'
        True
        >>> a.read_until(b'\\r\\n') is None
        True
        >>> a = ByteBuffer(b'123')
        >>> a.read_until(b'123', consume=True) == b''
        True
        >>> a.read_until(b'123') is None
        True
        """
        data  = self.read()
        idx   = data.find(delim)
        value = data[:idx] if idx >= 0 else None
        if consume and value is not None:
            self.consume(len(value)+len(delim))
        return value
    #}

    __bytes__ = read  # for Python 2.x
    __str__   = read  # for Python 3.x

    def consume(self, size=None):  #{
        """
        >>> a = ByteBuffer(b'abcdef123', max_size=30)
        >>> bytes(a) == b'abcdef123'
        True
        >>> a.consume(3)
        >>> bytes(a) == b'def123'
        True
        >>> len(a) == 6
        True
        >>> a.consume(500)
        >>> bytes(a) == b''
        True
        >>> len(a) == 0
        True
        >>> a.write(b'Z'*100) == 100
        True
        >>> a.consume(100)
        >>> len(a) == 0
        True
        >>> a._total == 0
        True
        """
        if size is None:
            size = self._total
        assert isinstance(size, int)
        total = self._total
        pos   = min(self._pos+size, total)
        if pos == total and total > self._max:
            self._pos, self._total = 0, 0
            self._bytes = BytesIO()
        else:
            self._pos = pos
            self._bytes.seek(pos)
    #}
    def write(self, data):  #{
        """
        >>> a = ByteBuffer(b'123')
        >>> a.write(b'abcdef') == 6
        True
        >>> bytes(a) == b'123abcdef'
        True
        >>> a.consume(3)
        >>> bytes(a) == b'abcdef'
        True
        >>> a.write(b'XYZ') == 3
        True
        >>> bytes(a) == b'abcdefXYZ'
        True
        >>> len(a) == 9
        True
        >>> a._total == 12
        True
        """
        assert isinstance(data, bytes)
        self._total += len(data)
        _bytes = self._bytes
        _bytes.seek(0, 2)
        return _bytes.write(data)
    #}
#}

def perform_tests():  #{
    from doctest import testmod
    failed, total = testmod()
    if not failed:
        print('OK, %d test(s) passed' % total)
#}

if __name__ == '__main__':
    perform_tests()

