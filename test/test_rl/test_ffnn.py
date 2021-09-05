import pytest
import torch as T

from rl.ffnn import FFNN


@pytest.fixture
def one_hidden_layer():
    return FFNN([(3, 2), (2, 4), (4, 1)])

def test_ffnn_structure(one_hidden_layer):
    assert(len(one_hidden_layer.layers()) == 3)
    assert(one_hidden_layer.layer_sizes()[0] == T.Size([2, 3]))
    assert(one_hidden_layer.layer_sizes()[1] == T.Size([4, 2]))
    assert(one_hidden_layer.layer_sizes()[2] == T.Size([1, 4]))


def test_ffnn_set_layer_data(one_hidden_layer):
    one_hidden_layer.set_layer_data([T.zeros(2, 3), T.zeros(4, 2), T.zeros(1, 4)])

def test_forward_in_zeros(one_hidden_layer):
    one_hidden_layer.set_layer_data([T.zeros(2, 3), T.zeros(4, 2), T.zeros(1, 4)])
    assert(one_hidden_layer.forward(T.reshape(T.tensor([1,2,3,4,5,6], dtype=T.float), (2, 3))))