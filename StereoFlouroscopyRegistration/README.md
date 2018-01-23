# Organization of StereoFlouroscopyRegistration
```bash
.
├── cli
├── io
├── pipelines
└── util
```

### cli
The command line interface. This provides a structured way of creating tools and
using StereoFlouroscopyRegistration. [Click](http://click.pocoo.org/5/) is used
to create the CLI. An entry point is defined in `setup.py`. The script `sfr.py`
can be used when running the package locally.

### io
Various code for input and output. Presently, this contains both VTK and ITK
input/output helpers.

### pipelines
When developing medical image processing and visualization code, many pipelines
are used over and over again. Such pipelines are instantiated as classes which
can be directly inserted into graphical programs for command line tools.

### util
Various utility functions. Most files should be self explanatory.
