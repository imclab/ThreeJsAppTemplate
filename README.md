ThreeJsAppTemplate
==================

* Python script to create a simple Three.js based WebGL app that you can use as a starting point for your next masterpiece.

* Creates an index.html file containing example [Three.js](https://github.com/mrdoob/three.js/), [dat.GUI](https://code.google.com/p/dat-gui/), [Stats](https://github.com/mrdoob/stats.js) and [Tween.js](https://github.com/sole/tween.js/) code.

* All source is downloaded and stored in the directory specified.

Usage: 

    ./ThreeJsAppTemplate.py

    -h, --help
    Show this help message and exit

    -min, --minified
    Fetch the minified version of libraries

    -nomin, --no-minified
    Fetch the non-minified version of libraries (useful for debugging)

    -tv <ver>, --three_version <ver>
    Specify version of Three.js to fetch (defaults to latest)

    -od <dir>, --output_dir <dir>
    Specify name of directory to write files (defaults to './three_js_app')

    -v, --version
    Display the version number of this script
