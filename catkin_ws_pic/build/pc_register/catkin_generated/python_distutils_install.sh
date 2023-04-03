#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/ruan/catkin_ws_pic/src/pc_register"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/ruan/catkin_ws_pic/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/ruan/catkin_ws_pic/install/lib/python3/dist-packages:/home/ruan/catkin_ws_pic/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/ruan/catkin_ws_pic/build" \
    "/usr/bin/python3" \
    "/home/ruan/catkin_ws_pic/src/pc_register/setup.py" \
     \
    build --build-base "/home/ruan/catkin_ws_pic/build/pc_register" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/ruan/catkin_ws_pic/install" --install-scripts="/home/ruan/catkin_ws_pic/install/bin"
