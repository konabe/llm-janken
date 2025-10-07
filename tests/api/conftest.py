"""
E2Eテスト用設定とユーティリティ
"""
import pytest


def pytest_configure(config):
    """Pytestの設定"""
    config.addinivalue_line(
        "markers", 
        "e2e: E2Eテストのマーカー（統合テスト用）"
    )


@pytest.fixture(autouse=True)
def setup_test_environment():
    """テスト環境セットアップ"""
    # テスト用環境変数の設定などがあれば追加
    yield
    # クリーンアップ処理