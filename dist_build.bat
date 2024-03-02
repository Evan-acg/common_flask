rmdir /q/s build
rmdir /q/s dist
rmdir /q/s common_flask_utils.egg-info

python setup.py sdist bdist_wheel