from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='bonniebully',
      version='2.0.0',
      url='https://github.com/delvidioneto/bonniebully',
      license='MIT License',
      author='Delvidio Demarchi Neto',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='delvidio.neto@outlook.com.br',
      keywords='datas date year month day bussiness day dia util',
      description=u'This package was developed to simplify date manipulation.',
      packages=['bonniebully'],
      install_requires=['holidays'],)
