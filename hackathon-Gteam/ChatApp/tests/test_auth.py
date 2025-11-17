import pytest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


#新規登録
def test_signup_success(client):
    """正常な新規登録のテスト"""
    response = client.post('/auth/signup', data={
        'email': 'testuser@example.com',
        'password': 'password123',
        'password_second': 'password123',
        'nickname': 'テストユーザー'
    })
    assert response.status_code == 302  # リダイレクト
    assert response.headers["Location"].endswith("/auth/login")

def test_signup_password_mismatch(client):
    """パスワード不一致のテスト"""
    response = client.post('/auth/signup', data={
        'email': 'testuser@example.com',
        'password': 'password123',
        'password_second': 'different',
        'nickname': 'テストユーザー'
    }) 
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/signup")  # 失敗時


def test_signup_email_same(client):
    """同じユーザーの登録"""
    response = client.post('/auth/signup', data={
        'email': 'test@gmail.com',
        'password': 'password123',
        'password_second': 'password123',
        'nickname': 'テストユーザー'
    }) 
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/signup")  # 失敗時


def test_signup_password_mismatch(client):
    """メール形式の確認"""
    response = client.post('/auth/signup', data={
        'email': 'uer_test_example_com',
        'password': 'password123',
        'password_second': 'password123',
        'nickname': 'テストユーザー'
    }) 
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/signup")  # 失敗時


def test_signup_password_mismatch(client):
    """パスワードの文字数の制限"""
    response = client.post('/auth/signup', data={
        'email': 'testuser@example.com',
        'password': 'password',
        'password_second': 'password',
        'nickname': 'テストユーザー'
    }) 
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/signup")  # 失敗時

#ログイン処理
def test_login_success(client):
    """正常なログインのテスト"""
    response = client.post('/auth/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'

    })
    assert response.status_code == 302  # リダイレクト
    assert response.headers["Location"].endswith("/room/index")


def test_login_miss(client):
    """パスワード間違いのテスト"""
    response = client.post('/auth/login', data={
        'email': 'testuser@example.com',
        'password': 'different_password'

    })
    assert response.status_code == 302  # リダイレクト
    assert response.headers["Location"].endswith("/auth/login")


#パスワード変更画面 
def test_reset_password_success(client):
    """正常なパスワードの変更のテスト"""
    response = client.post('/auth/password_reset', data={
        'email': 'testuser@example.com',
        'current_password': 'password123',
        'new_password': 'newpassword123',
        'new_password_second': 'newpassword123',
    })
    assert response.status_code == 302  # リダイレクト
    assert response.headers["Location"].endswith("/auth/login")


def test_reset_password_miss_login(client):
    """現在のパスワードの間違い"""
    response = client.post('/auth/password_reset', data={
        'email': 'testuser@example.com',
        'current_password': 'mismatch',
        'new_password': 'new_password',
        'new_password_second': 'new_password',
    })
    assert response.status_code == 302  # リダイレクト
    assert response.headers["Location"].endswith("/auth/password_reset")

def test_reset_password_mismatch(client):
    """一回目と二回目のパスワードの間違い"""
    response = client.post('/auth/password_reset', data={
        'email': 'testuser@example.com',
        'current_password': 'password123',
        'new_password': 'new_password',
        'new_password_second': 'different',
    })
    assert response.status_code == 302  # リダイレクト
    assert response.headers["Location"].endswith("/auth/password_reset")


def test_reset_password_len(client):
    """パスワードの文字数不足"""
    response = client.post('/auth/password_reset', data={
        'email': 'testuser@example.com',
        'current_password': 'password123',
        'new_password': 'min',
        'new_password_second': 'min',
    })
    assert response.status_code == 302  # リダイレクト
    assert response.headers["Location"].endswith("/auth/password_reset")


def test_delete_account(client):
    response = client.post('/auth/login', data={
        'email': 'testuser@example.com',
        'password': 'newpassword123'

    })
    assert response.status_code == 302  # リダイレクト
    assert response.headers["Location"].endswith("/room/index")
    response = client.post('/auth/delete_account')
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/signup")


for rule in app.url_map.iter_rules():
    print(rule, rule.endpoint)
