import pytest
import torch
from torch_sparse.tensor import SparseTensor

from .utils import devices

try:
    torch.ops.torch_sparse.partition
    with_metis = True
except RuntimeError:
    with_metis = False


@pytest.mark.skipif(not with_metis, reason='Not compiled with METIS support')
@pytest.mark.parametrize('device', devices)
def test_metis(device):
    value1 = torch.randn(6 * 6, device=device).view(6, 6)
    value2 = torch.arange(6 * 6, dtype=torch.long, device=device).view(6, 6)
    value3 = torch.ones(6 * 6, device=device).view(6, 6)

    for value in [value1, value2, value3]:
        mat = SparseTensor.from_dense(value)

        _, partptr, perm = mat.partition(num_parts=2, recursive=False,
                                         weighted=True)
        assert partptr.numel() == 3
        assert perm.numel() == 6

        _, partptr, perm = mat.partition(num_parts=2, recursive=False,
                                         weighted=False)
        assert partptr.numel() == 3
        assert perm.numel() == 6

        _, partptr, perm = mat.partition(num_parts=1, recursive=False,
                                         weighted=True)
        assert partptr.numel() == 2
        assert perm.numel() == 6
