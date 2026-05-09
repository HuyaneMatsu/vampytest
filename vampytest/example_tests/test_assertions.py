import vampytest


def test_equality_assertions():
    a = 2
    b = 2
    
    c = 'a'
    d = 'b'
    
    # Asserts a == b
    vampytest.assert_eq(a, b)
    
    # Asserts c != d
    vampytest.assert_ne(c, d)


def test_boolean_assertions():
    e = 'a'
    f = ''
    
    # Asserts bool(e)
    vampytest.assert_true(e)
    
    # Asserts not bool(f)
    vampytest.assert_false(f) 


def test_container_assertions():
    g = 5
    h = [5, 6]
    
    i = 3
    j = [4, 6]
    
    # Asserts g in h
    vampytest.assert_in(g, h)
    
    # Asserts i not in j
    vampytest.assert_not_in(i, j)


def test_identity_assertions():
    k = object()
    l = k
    
    m = object()
    n = object()
    
    # Asserts k is l
    vampytest.assert_is(k, l)
    
    # Asserts m is not n
    vampytest.assert_is_not(m, n)


def test_exception_assertions():
    # Asserts that the code inside the context manager raises the defined exception
    with vampytest.assert_raises(ValueError):
        raise ValueError
    
    # Asserts that the code inside the context manager raises an equal exception to the defined one.
    with vampytest.assert_raises(ValueError('aya')):
        raise ValueError('aya')
    
    # Also asserts whether the given condition is satisfied
    with vampytest.assert_raises(ValueError, where = lambda e: 'aya' in repr(e)):
        raise ValueError('ayaya')


def test_type_assertions():
    o = ''
    q = None
    r = ''
    
    s = str
    t = None
    
    # Asserts isinstance(o, str)
    vampytest.assert_instance(o, str)
    
    # Asserts q is None or isinstance(q, str)
    vampytest.assert_instance(q, str, nullable = True)
    
    # Asserts type(r) is str
    vampytest.assert_instance(r, str, accept_subtypes = False)
    
    # Asserts isinstance(s, type) and issubclass(s, str)
    vampytest.assert_subtype(s, str)
    
    # Asserts t is None or isinstance(t, type) and issubclass(t, str)
    vampytest.assert_subtype(t, str, nullable = True)


def test_reversed_assertions():
    u = 1
    v = 2
    
    w = 3
    
    # Assert not u == v
    vampytest.assert_eq(u, v, reverse = True)
    
    # Asserts not isinstance(w, str)
    vampytest.assert_instance(w, str, reverse = True)
