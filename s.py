---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\matplotlib\axes\_axes.py:4618, in Axes._parse_scatter_color_args(c, edgecolors, kwargs, xsize, get_next_color_func)
   4617 try:  # Is 'c' acceptable as PathCollection facecolors?
-> 4618     colors = mcolors.to_rgba_array(c)
   4619 except (TypeError, ValueError) as err:

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\matplotlib\colors.py:512, in to_rgba_array(c, alpha)
    511 else:
--> 512     rgba = np.array([to_rgba(cc) for cc in c])
    514 if alpha is not None:

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\matplotlib\colors.py:314, in to_rgba(c, alpha)
    313 if rgba is None:  # Suppress exception chaining of cache lookup failure.
--> 314     rgba = _to_rgba_no_colorcycle(c, alpha)
    315     try:

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\matplotlib\colors.py:400, in _to_rgba_no_colorcycle(c, alpha)
    399 if len(c) not in [3, 4]:
--> 400     raise ValueError("RGBA sequence should have length 3 or 4")
    401 if not all(isinstance(x, Real) for x in c):
    402     # Checks that don't work: `map(float, ...)`, `np.array(..., float)` and
    403     # `np.array(...).astype(float)` would all convert "0.5" to 0.5.

ValueError: RGBA sequence should have length 3 or 4
...
        .base_values =
        -2.569764127744216

        .data =
        19.29664850785879  ]], dtype=object)
