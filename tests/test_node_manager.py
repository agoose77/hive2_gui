import pytest

import sys
sys.path.append("D:/pycharmprojects/hive2_gui")

@pytest.fixture
def node_manager():
    from hive2_gui.node_manager import NodeManager
    from hive2_gui.history import CommandLogManager
    history = CommandLogManager()
    return NodeManager(history)


def test_node_manager(node_manager):
    print(node_manager)