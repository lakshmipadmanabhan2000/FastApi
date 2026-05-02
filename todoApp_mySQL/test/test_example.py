import pytest
#integers
def test_equal_or_not_equal():
    assert 3==3
    assert 3!=1
#instances
def test_is_instance():
    assert isinstance('this is a str',str)
    assert not isinstance('10',int)
#boolean
def test_boolean():
    validated=True
    assert validated is True
    assert ('hello' == 'world') is False
#type
def test_type():
    assert type('hello') is str
    assert type('world') is not int
#integers
def test_greater_or_less_than():
    assert 7>3
    assert 4<10
#lists
def test_list():
    num_list=[1,2,3,4,5]
    any_list=[False,False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, fname:str, lname:str, major:str, years:int):
        self.fname=fname
        self.lname=lname
        self.major=major
        self.years=years

'''def test_person_initialization():
    p=Student('John','Doe','Computer Science',3)
    assert p.fname=='John','First name should be John'
    assert p.lname=='Doe','Last name should be Doe'
    assert p.major=='Computer Science'
    assert p.years==3 '''

# enhance using pytest fixture
@pytest.fixture
def default_student():
    return Student('John','Doe','Computer Science',3)

def test_person_initialization(default_student):
    assert default_student.fname=='John','First name should be John'
    assert default_student.lname=='Doe','Last name should be Doe'
    assert default_student.major=='Computer Science'
    assert default_student.years==3