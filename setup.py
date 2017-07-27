from setuptools import setup
import pkgutil

# PyQt5 can not be installed via pip.
if not 'PyQt5' in [i[1] for i in pkgutil.iter_modules()]:
    raise Exception('PyQt5 needs to be installed.')

def readme():
    with open('Readme.md', 'r') as f:
        return f.read()

setup(name='rocto-client',
      version='0.0.1',
      description='The client for rocto.',
      long_description=readme(),
      url='https://github.com/ROctopus/ROctopus-client',
      author='Oğuzhan Öğreden',
      author_email='oguzhanogreden@gmail.com',
      license='XXX',
      packages=['rocto_client'],
      install_requires=[
     'socketIO-client', 'requests', 'urllib3', 'psutil'
      ],
      zip_safe=False)
