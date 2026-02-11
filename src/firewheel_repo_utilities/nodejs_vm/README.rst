.. _utilities.nodejs_mc:

#################
utilities.nodejs
#################


*Provides an implementation of Node.js on a virtual machine.*

*****
Usage
*****

This model component provides a decorator for adding Node.js to a virtual machine.
Multiple versions of Node are provided as VM resources, each with a version specifier (e.g., ``node-v20.12.2-linux-x64``), and the Node version to use in an experiment can be provided by passing the version number as an argument to the decorator upon instantiation:

.. code-block:: python

            # ... plugin setup ...

            vertex.decorate(NodeJSVM, init_kwargs={"node_version": "20.12.2"})

Other less commonly used parameters may also be configured via the decorator, including the method of installation for the Node binaries (directly into ``/usr/local/bin`` or symlinked there) and whether or not ``npm`` should operate in offline mode (set to work offline by default).
See the :py:meth:`decorator constructor documentation <utilties.nodejs.NodeJSVM.__init__>` for more details.


**********************************************************
Extending the Model Component with New Versions of Node.js
**********************************************************

The supported versions of Node are listed below in the `VM Resources`_ section.
To use a different version of Node in the model component, download the binary from a source repository (e.g., `nodejs.org <https://nodejs.org/en/download/prebuilt-binaries>`_) and either add it to the ``vm_resources`` directory directory, or preferably, configure the MC to source the binary from a remote location.

.. note::

   Node.js binaries should not be distributed with this MC repository, and binaries that are to be permanently included with the MC should not be committed directly to the ``vm_resources`` directory.
   Instead, follow the instructions for preparing a :ref:`mc_install` to download the new binary from its source or a trusted repository.
   To determine the checksum of a Node binary to provide in an ``INSTALL`` script, run:

   .. code-block:: bash

      shasum -a 256 <node-binary>

Following Node custom, ensure that the binary is a ``*.tar.xz`` archive with a filename following the format ``node-v<Major>.<minor>.<patch>-linux-x64.tar.xz``.
This filename structure is the default for all binaries downloaded from the official Node.js repository and is required by the installer.
Also note that only Linux binaries can be used, since the ``NodeJSVM`` decorator requires that the VM be an instance of ``UbuntuHost`` provided by the ``linux.ubuntu`` model component.

Once downloaded to the ``vm_resources`` directory, new versions of Node should be available as an argument to the decorator as described above (the ``MANIFEST`` already supports arbitrary ``.tar.xz`` VM resources and so should not need modification).


******************************************************
Downloading Packages for Use in VMs Supoorting Node.js
******************************************************

This model component facilitates preparation of a VM to offer a supported version of Node.js.
However, when subsequent downstream model components rely on this MC so that they can use a Node package in a FIREWHEEL experiment, those downstream MCs will need to provide any additional package dependencies.
Since FIREWHEEL experiments typically operate offline, those package dependencies will likely be required to have been downloaded in advance.
The recommended approach for generating these dependencies is to acquire all necessary dependency content using the :ref:`VM Builder <helper_vm_builder>` utility in ``launch`` mode.
Then, using an Internet connection in the VM builder:

#. Install the appropriate version of Node.js. Ideally, this is the exact same version as the experiment.
#. Install the package dependencies using ``npm`` (installed with Node.js).
#. [Optional] Zip dependency files (e.g., ``package.json``, ``package-lock.json`` and ``node_modules`` files and directories) into a tar archive.
#. Use SCP to copy the files from the VM builder machine to the ``vm_resources`` directory in the model component repository on the machine being used for MC development. (Hint: Use the ``ip addr`` command on the builder VM to get the IP address of that machine.)
#. Indicate how the model component should handle the files. This may include updating the ``MANIFEST``, using the :py:meth:`linux.base_objects.LinuxHost.unpack_tar` or :py:meth:`base_objects.VMEndpoint.drop_file` methods. Packages may be dropped anywhere on the file system, with global packages typically stored in ``/usr/local/lib/node`` or ``/usr/local/lib/node_modules`` and local packages stored in any other directory of choice.


**Attribute Provides:**
    * ``nodejs``


**Model Component Dependencies:**
    * :ref:`linux.ubuntu`


************
VM Resources
************

* ``node-v18.13.0-linux-x64.tar.xz``
* ``node-v20.12.2-linux-x64.tar.xz``
* ``node-v24.13.1-linux-x64.tar.xz``


*****************
Available Objects
*****************

.. automodule:: utilities.nodejs
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__

