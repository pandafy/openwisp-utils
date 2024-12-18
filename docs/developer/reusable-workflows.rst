Re-usable GitHub Workflows
==========================

Replicate Commits to Version Branch
-----------------------------------

This re-usable workflow replicates commits from the ``master`` branch to a
version branch. The version branch name is derived from the version of the
Python package specified in your project.

You can invoke this workflow from another workflow using the following
example:

.. code-block:: yaml

    name: Replicate Commits to Version Branch

    on:
      push:
        branches:
          - master

    jobs:
      version-branch:
        uses: openwisp/openwisp-utils/.github/workflows/reusable-version-branch.yml@master
        with:
          module_name: openwisp_utils

.. note::

    If the ``master`` branch is force-pushed, this workflow will fail due
    to conflicts. To resolve this, you must manually synchronize the
    version branch with the ``master`` branch.
