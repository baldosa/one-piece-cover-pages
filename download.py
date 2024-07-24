"""
Modified from https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5
"""

import os
from urllib.request import urlretrieve
from tqdm import tqdm


def dl_hook(tqdm_instance):
    """Wraps tqdm instance.
    Don't forget to close() or __exit__()
    the tqdm instance once you're done with it (easiest using `with` syntax).
    Example
    -------
    >>> with tqdm(...) as t:
    ...     reporthook = my_hook(t)
    ...     urllib.urlretrieve(..., reporthook=reporthook)
    """
    last_b = [0]

    def update_to(b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            tqdm_instance.total = tsize
        tqdm_instance.update((b - last_b[0]) * bsize)
        last_b[0] = b

    return update_to


def download(url, save_dir, filename):

    with tqdm(
        unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=filename
    ) as t:
        urlretrieve(
            url,
            filename=os.path.join(save_dir, filename),
            reporthook=dl_hook(t),
            data=None,
        )
