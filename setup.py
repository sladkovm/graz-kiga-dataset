from setuptools import setup

setup(name='etl',
      version='0.1',
      description='Graz kiga dataset',
      url='http://github.com/sladkovm/xxx',
      author='Maksym Sladkov',
      author_email='sladkovm@gmail.com',
      license='MIT',
      py_modules=['etl'],
      install_requires=['bonobo', 'requests_html'],
      zip_safe=False)