# OverloadFn

_Simple implementation of a `@Overload` decorator to enable function overloading ("polymorphism") in Python 3.8+_

## Install

### Download

``` bash
git clone https://github.com/taylor8294/python3-overloadfn.git overloadfn
cd overloadfn
python3 -m pip install -e .
```

## License

### Commercial license

If you want to use OverloadFn to develop commercial sites, tools, projects, or applications, the Commercial license is the appropriate license. With this option, your source code is kept proprietary. To acquire a OverloadFn Commercial License please [contact me](https://www.taylrr.co.uk/).

### Open source license

If you are creating an open source application under a license compatible with the [GNU GPL license v3](https://www.gnu.org/licenses/gpl-3.0.html), you may use OverloadFn under the terms of the GPLv3.

## Usage

OverloadFn is very simple to use: just `import` the the `@Overload()` decorator and use it on your first function definition, the use `@<function_name>.overload()` thereafter.

You can either specify the argument types in the decorator itself, like this

``` python
from numbers import Real
from overloadfn import Overload

@Overload(Real)
def area(radius):
    import math
    return math.pi * radius*radius

@area.overload(Real, Real)
def area(len, breath):
    calc = len * breath
    return calc

class Animal(object):
    def sound(self):
        return 'moo!'

class Dog(Animal):
    @Overload()
    def sound(self):
        return 'bark!'
    
    @sound.overload(Real)
    def sound(self, i):
        return 'woof, {} math!'.format(i)
  
print(area(1))    # 3.141519
print(area(2,3))  # 6
d = Dog()
print(d.sound())  # bark!
print(d.sound(1)) # woof, 1 math!

```

Notice both top-level functions and class methods are supported.

**Or** you may use type-hints (make sure to still include the brackets after the decorator though!), like this

``` python
from typing import Union, List, Dict
from numbers import Real
from overloadfn import Overload

@Overload()
def area(radius:Real) -> Real:
    import math
    return math.pi * radius*radius

@area.overload()
def area(len:Real, breath:Real) -> Real:
    calc = len * breath
    return calc

@area.overload()
def area(arg:Union[List,Dict]) -> str:
    return 'You\'ve passed a List or a Dict argument'

print(area(1))   # 3.141519
print(area(2,3)) # 6
print(area([]))  # 'You\'ve passed a List or a Dict argument'
```

Yes you can even use `Union`! Providing no explicit type for an argument in the `@Overload()` or `@<function_name>.overload()` decorators (as well as no type-hints) will behave the same as passing in `typing.Any` for that argument. 

## Tests

There are some basic unit tests included in the package, you can run these from the root of the package (the same directory as `setup.py`) by running
``` bash
python3 -m pip --install nose
nosetests --verbose
```

## Warnings / To Do

Do note
* The overloading is based on the position **and** type of the arguments, therefore you should not use keyword arguments when calling overloaded function (the behaviour will not be well defined).

I welcome any feedback or pull requests.

---

By [Taylor8294 🌈🐻](https://www.taylrr.co.uk/)