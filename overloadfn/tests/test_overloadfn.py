import unittest
from overloadfn import Overload
from typing import Union, List, Dict
from numbers import Real
import logging

logging.basicConfig(level=logging.INFO)

@Overload(int)
def area(radius):
    import math
    return math.pi * radius*radius

@area.overload(int, int)
def area(leng, breath):
    calc = leng * breath
    return calc

class Animal(object):
    def sound():
        return 'noise!'

class Dog(Animal):
    @Overload()
    def sound(self):
        return 'bark!'
    
    @sound.overload(int)
    def sound(self, i):
        return 'numbers!'

@Overload(Animal)
def whatsthis(f):
    return 'This is a Animal'

@whatsthis.overload(bool)
def whatsthis(b):
    return 'This is a Boolean'

class TestOverload(unittest.TestCase):
    def test_circle(self):
        a = area(1)
        self.assertTrue(a >= 3.14 and a < 3.142)
        
    def test_rect(self):
        a = area(2,3)
        self.assertTrue(a >= 5.99 and a < 6.01)
        
    def test_method(self):
        with self.subTest(0):
            a = Dog().sound(1)
            self.assertEqual(a, 'numbers!')
        with self.subTest(1):
            a = Dog().sound()
            self.assertEqual(a, 'bark!')
        
    def test_bool(self):
        a = whatsthis(True)
        self.assertEqual(a, 'This is a Boolean')
        
    def test_subclass(self):
        a = whatsthis(Dog())
        self.assertEqual(a, 'This is a Animal')
