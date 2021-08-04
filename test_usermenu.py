import pytest
from usermenu import UserMenu 
from datastore import Datastore
from customer_account import CustomerAccount

user_menu = UserMenu()
ds = Datastore()


@pytest.fixture
def list():
   return ds.customer_accounts_list

def test_validate_name():
    assert user_menu.validate_name("Maria") == "Maria"
    
def test_validate_name_exception():
    with pytest.raises(Exception):
        assert user_menu.validate_name("123")

def test_validate_surname():
    assert user_menu.validate_surname("Walsh") == "Walsh"
    
def test_validate_surname_exception():
    with pytest.raises(Exception):
        assert user_menu.validate_surname("")        

def test_validate_ppsn():
    assert user_menu.validate_ppsn("1234567qq") == "1234567qq"
    assert user_menu.validate_ppsn("1234567q") == "1234567q"

def test_validate_ppsn_exception():
    with pytest.raises(Exception):
        assert user_menu.validate_ppsn("1234")

def test_validate_ppsn_format():
    assert user_menu.validate_ppsn("qq1234567") == "Entered PPSN is not valid"

def test_load_customer_account(list):
    assert user_menu.load_customer_account("10203000", list) == list[0]

def test_load_customer_account_invalid_input(list):
    assert user_menu.load_customer_account("123", list) == "Account not found"



