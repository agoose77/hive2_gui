from setuptools import setup

setup(name='hive2_gui',
      version=0.1,
      description='Hive Nodal Logic GUI',
      author='Sjoerd De Vries & Angus Hollands',
      author_email='goosey15+hive2_gui@gmail.com',
      url='https://github.com/agoose77/hive2_gui',
      packages=['hive2_gui'],
      include_package_data=True,
      scripts=['run_qt_gui.py'],

      # Project uses reStructuredText, so ensure that the docutils get
      # installed or upgraded on the target machine
      install_requires=['PyQt5', 'pygments', 'qdarkstyle', 'hive2', 'python_jsonschema_objects', 'pytest'],
)
