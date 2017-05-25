from setuptools import setup

def readme():
    with open('Readme.md', 'r') as f:
        return f.read()

setup(name='ROctopus-client',
      version='0.0.1',
      description='The client for ROctopus',
      long_description=readme(),
      url='https://github.com/ROctopus/ROctopus-client',
      author='Oğuzhan Öğreden',
      author_email='oguzhanogreden@gmail.com',
      license='XXX',
      packages=['ROctopus_client'],
      install_requires=[
      'PyQt5', 'socketIO-client', 'requests'
      ],
      zip_safe=False)
