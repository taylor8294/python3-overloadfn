from setuptools import setup

def readme():
    with open('README.md', encoding="utf8") as f:
        return f.read()

setup(name='overloadfn',
      version='0.1',
      description='Simple @overload decorator implemented in Python',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='overload overloading polymorphism polymorphic function functions decorator',
      url='http://github.com/taylor8294/overloadfn',
      author='Alex Taylor',
      author_email='alex@taylrr.co.uk',
      license='GPLv3',
      packages=['overloadfn'],
      zip_safe=False,
      install_requires=[
            'typing',
            'typeguard'
      ],
      include_package_data=True)