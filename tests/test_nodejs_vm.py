"""Tests for the utilities.nodejs model component object."""

import importlib
import sys
import types
from pathlib import Path


def _load_nodejs_module(monkeypatch):
    linux = types.ModuleType("linux")
    linux_ubuntu = types.ModuleType("linux.ubuntu")
    firewheel = types.ModuleType("firewheel")
    control = types.ModuleType("firewheel.control")
    experiment_graph = types.ModuleType("firewheel.control.experiment_graph")

    class UbuntuHost:
        pass

    class require_class:  # noqa: N801
        def __init__(self, _required_class):
            pass

        def __call__(self, graph_object):
            return graph_object

    linux_ubuntu.UbuntuHost = UbuntuHost
    experiment_graph.require_class = require_class
    monkeypatch.setitem(sys.modules, "linux", linux)
    monkeypatch.setitem(sys.modules, "linux.ubuntu", linux_ubuntu)
    monkeypatch.setitem(sys.modules, "firewheel", firewheel)
    monkeypatch.setitem(sys.modules, "firewheel.control", control)
    monkeypatch.setitem(sys.modules, "firewheel.control.experiment_graph", experiment_graph)
    module_name = "firewheel_repo_utilities.nodejs_vm.model_component_objects"
    sys.modules.pop(module_name, None)
    return importlib.import_module(module_name)


def test_nodejs_symlink_install_exposes_paths_for_downstream_components(monkeypatch):
    module = _load_nodejs_module(monkeypatch)

    class RecordingNodeJSVM(module.NodeJSVM):
        def __init__(self):
            self.commands = []
            self.unpacked = []
            super().__init__(node_version="18.13.0", symlink=True)

        def unpack_tar(self, time, archive, options="-xzf", directory=None, vm_resource=False):
            self.unpacked.append((time, archive, options, directory, vm_resource))

        def run_executable(self, time, executable, arguments=None, vm_resource=False):
            self.commands.append((time, executable, arguments, vm_resource))

    vm = RecordingNodeJSVM()

    assert vm.node_bin == Path("/opt/node-v18.13.0-linux-x64/bin")
    assert vm.node_lib == Path("/opt/node-v18.13.0-linux-x64/lib/node_modules")
    assert vm.bash_node_prefix == (
        "PATH=$PATH:/opt/node-v18.13.0-linux-x64/bin "
        "NODE_PATH=/opt/node-v18.13.0-linux-x64/lib/node_modules"
    )
    assert vm.unpacked == [(-100, "node-v18.13.0-linux-x64.tar.xz", "-xf", Path("/opt"), True)]
    assert (-99, "ln", "-sf /opt/node-v18.13.0-linux-x64/bin/node /usr/local/bin/node", False) in vm.commands
    assert (-99, "ln", "-sf /opt/node-v18.13.0-linux-x64/bin/npm /usr/local/bin/npm", False) in vm.commands
    assert (-99, "ln", "-sf /opt/node-v18.13.0-linux-x64/bin/npx /usr/local/bin/npx", False) in vm.commands
    assert (-50, "npm", ["config", "set", "offline=true"], False) in vm.commands

    vm.install_node_package_bundle(-63, "web3js-quorum-node-modules.tgz")

    assert vm.unpacked[-1] == (
        -63,
        "web3js-quorum-node-modules.tgz",
        "-x --strip-components=1 -f",
        Path("/opt/node-v18.13.0-linux-x64/lib/node_modules"),
        True,
    )
