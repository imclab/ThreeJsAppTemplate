#!/usr/bin/python

###############################################################################
#
#   https://github.com/callumprentice/ThreeJsAppTemplate
#   callum@gmail.com
#
###############################################################################
import argparse
import os
import re
import sys
import textwrap
import urllib2

version_number = "1"

###############################################################################
def getThreeJSRevision(js_url):

    print '\nGetting Three.js revision'

    response = urllib2.urlopen(js_url)
    js = response.read()

    revision = 'unk'
    match = re.search(r'{REVISION:"(.*?)"}', js)
    if match:
        revision = match.group(1)

    match = re.search(r"{ REVISION: '(.*?)' }", js)
    if match:
        revision = match.group(1)

    return revision

###############################################################################
def getJSFile(js_name, base_dir, js_url, use_three_js_revision, rev_number):

    print '\nGetting ' + js_name

    js_filename = js_url.split('/')[-1]

    response = urllib2.urlopen(js_url)
    js = response.read()

    directory = base_dir + '/js'
    if use_three_js_revision:
        directory += '/three.r' + rev_number

    print '    Writing to directory ' + directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = directory + '/' + js_filename
    js_file = open(filename, 'w')
    js_file.write(js)
    js_file.close()

    print '    ' + js_name + ' retrieved into ' + filename


###############################################################################
def writeCode(base_dir, rev_number):

    source_filename = 'index.html'
    filename = base_dir + '/' + source_filename
    source_file = open(filename, 'w')

    source_file.write( textwrap.dedent("""\
        <!DOCTYPE html>
        <html>
            <head>
            <title>Three.js Sample Template</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <meta name="Generator" content="https://github.com/callumprentice/ThreeJsAppTemplate">
                <style type="text/css">
                    body {
                        background-color: #000;
                        color: #ff0;
                        margin: 0;
                        overflow: hidden;
                    }
                </style>
            </head>
            <body>
                    """) )

    source_file.write('        <script type="text/javascript" src="js/three.r' + rev_number +'/' + threejs_filename + '"></script>\n')
    source_file.write('        <script type="text/javascript" src="js/three.r' + rev_number +'/TrackballControls.js"></script>\n')
    source_file.write('        <script type="text/javascript" src="js/three.r' + rev_number +'/Detector.js"></script>\n')
    source_file.write('        <script type="text/javascript" src="js/' + dat_gui_filename + '"></script>\n')
    source_file.write('        <script type="text/javascript" src="js/' + tween_filename + '"></script>\n')
    source_file.write('        <script type="text/javascript" src="js/' + stats_filename + '"></script>\n')

    source_file.write( textwrap.dedent("""\
            <script type="text/javascript">
                var camera, scene, renderer;
                var controls, stats;
                var mesh;
                var auto_spin = true;
                var spin_speed = 1.0;
                var translucent = false;
                var color = 0x337873;

                init();
                animate();

                function init() {
                    if ( ! Detector.webgl )
                        Detector.addGetWebGLMessage();

                    renderer = new THREE.WebGLRenderer( { antialias: true });
                    renderer.setClearColor( 0x333366, 1.0 );
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    document.body.appendChild(renderer.domElement);

                    scene = new THREE.Scene();

                    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
                    camera.position.z = 400;

                    var ambient_light = new THREE.AmbientLight(0xcccccc);
                    scene.add(ambient_light);

                    var geometry = new THREE.IcosahedronGeometry(200, 3);

                    var materials = [
                        new THREE.MeshBasicMaterial({
                            color: color,
                            transparent: true
                        }),
                        new THREE.MeshBasicMaterial({
                            color: 0xffffff,
                            wireframe: true,
                            wireframeLinewidth: 2
                        })
                    ];

                    mesh = THREE.SceneUtils.createMultiMaterialObject(geometry, materials);
                    scene.add(mesh);

                    new TWEEN.Tween({ scale: 0 })
                        .to({ scale: 1 }, 2500)
                        .easing(TWEEN.Easing.Elastic.InOut)
                        .onUpdate(function () {
                            mesh.scale.set(this.scale, this.scale, this.scale);
                        }).start();

                    controls = new THREE.TrackballControls(camera, renderer.domElement);
                    controls.rotateSpeed = 0.4;
                    controls.noZoom = false;
                    controls.noPan = false;
                    controls.staticMoving = false;
                    controls.dynamicDampingFactor = 0.4;
                    controls.minDistance = 300;
                    controls.maxDistance = 600;

                    var gui = new dat.GUI();
                    gui.add(this, 'auto_spin', true).name("Auto Spin");
                    gui.add(this, 'spin_speed', -1.2, 1.2).name("Spin Speed");
                    gui.add(this, 'translucent', true).name("Translucent").onChange( function(value) {
                        if ( value )
                            mesh.children[0].material.opacity = 0.8;
                        else
                            mesh.children[0].material.opacity = 1.0;
                    });
                    gui.addColor(this, 'color').name("Object Color").onChange( function(value) {
                        mesh.children[0].material.color.setHex(value);
                    });

                    stats = new Stats();
                    stats.domElement.style.position = 'absolute';
                    stats.domElement.style.bottom = '0px';
                    stats.domElement.style.zIndex = 100;
                    document.body.appendChild(stats.domElement);

                    window.addEventListener( 'resize', onWindowResize, false );
                }

                function onWindowResize() {
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();

                    renderer.setSize( window.innerWidth, window.innerHeight );
                }

                function animate() {
                    requestAnimationFrame(animate);

                    TWEEN.update();
                    controls.update();
                    stats.update();

                    if ( auto_spin ) {
                        mesh.rotation.x = Date.now() * 0.0005 * spin_speed;
                        mesh.rotation.y = Date.now() * 0.0005 * spin_speed;
                    }

                    renderer.render(scene, camera);
                }
            </script>
        </body>
    </html>

        """) )

    print '\nSource file written to ' + filename

    source_file.close()

###############################################################################
if __name__ == "__main__":

    print '\nThree.js app template maker - https://github.com/callumprentice/ThreeJsAppTemplate\n'

    parser = argparse.ArgumentParser()
    parser.add_argument('-tv', '--three_version', help='Specify version of Three.js to fetch')
    parser.add_argument('-od', '--output_dir', help='Specify name of directory to write files')
    parser.add_argument('-min', '--minified', dest='minified', action='store_true')
    parser.add_argument('-nomin', '--no-minified', dest='minimied', action='store_false')
    parser.add_argument('-v',  '--version', action='version', version='%(prog)s version: ' + version_number)
    args = parser.parse_args()

    base_dir = 'three_js_app'
    
    if args.output_dir:
        base_dir = args.output_dir

    print 'Project base directory is ' + base_dir

    if args.minified == True:
        threejs_filename = 'three.min.js'
        print "\nFetching minified version of libraries"
    else:
        threejs_filename = 'three.js'
        print "\nFetching non-minified version of libraries"

    if args.three_version:
        revision = args.three_version
    else:
        latest_three_js_url = "http://threejs.org/build/" + threejs_filename
        revision = getThreeJSRevision(latest_three_js_url)

    print "\nRevision number is " + revision

    three_js_url = "https://raw.github.com/mrdoob/three.js/r" + revision + "/build/" + threejs_filename

    getJSFile('Three.js', base_dir, three_js_url, True, revision)
    getJSFile('TrackballControls.js', base_dir, 'https://raw.github.com/mrdoob/three.js/master/examples/js/controls/TrackballControls.js', True, revision)
    getJSFile('Detector.js', base_dir, 'https://raw.github.com/mrdoob/three.js/master/examples/js/Detector.js', True, revision)

    if args.minified == True:
        getJSFile('Stats.js', base_dir, 'https://raw.github.com/mrdoob/stats.js/master/build/stats.min.js', False, '')
        stats_filename = 'stats.min.js'
        getJSFile('Tween.js', base_dir, 'https://raw.github.com/sole/tween.js/master/build/tween.min.js', False, '')
        tween_filename = 'tween.min.js'
        getJSFile('dat-gui', base_dir, 'https://dat-gui.googlecode.com/git/build/dat.gui.min.js', False, '')
        dat_gui_filename = 'dat.gui.min.js'
    else:
        getJSFile('Stats.js', base_dir, 'https://raw.github.com/mrdoob/stats.js/master/src/Stats.js', False, '')
        stats_filename = 'Stats.js'
        getJSFile('Tween.js', base_dir, 'https://raw.github.com/sole/tween.js/master/src/Tween.js', False, '')
        tween_filename = 'Tween.js'
        getJSFile('dat-gui', base_dir, 'https://dat-gui.googlecode.com/git/build/dat.gui.js', False, '')
        dat_gui_filename = 'dat.gui.js'

    writeCode(base_dir, revision)
