XBlock for grouping other XBlocks together into a "unit" of learning.

This is meant to replace most usages of the "vertical" XBlock, which is
part of edx-platform.

Testing with Docker
-------------------

This XBlock comes with a Docker test environment ready to build, based on the xblock-sdk workbench. To build and run it::

        $ make dev.run

The XBlock SDK Workbench, including this XBlock, will be available on the list of XBlocks at http://localhost:8000
