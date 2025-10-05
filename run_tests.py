#!/usr/bin/env python3
"""
ユニットテスト実行スクリプト（__pycache__無効化対応）
"""

import sys
import unittest
import os

# __pycache__ 生成を無効化
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():
    """全てのテストを実行"""
    print("🧪 LLM じゃんけんゲーム - ユニットテスト実行")
    print("=" * 50)
    
    # テストディスカバリー
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # テスト実行
    runner = unittest.TextTestRunner(
        verbosity=2,
        buffer=True,
        stream=sys.stdout
    )
    
    result = runner.run(suite)
    
    # 結果サマリー
    print("\n" + "=" * 50)
    print("📊 テスト結果サマリー")
    print(f"実行したテスト: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失敗: {len(result.failures)}")
    print(f"エラー: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ 失敗したテスト:")
        for test, trace in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n💥 エラーが発生したテスト:")
        for test, trace in result.errors:
            print(f"  - {test}")
    
    if result.wasSuccessful():
        print("\n✅ 全てのテストが成功しました！")
        return 0
    else:
        print("\n❌ テストに失敗がありました。")
        return 1

def run_specific_test(test_module):
    """特定のテストモジュールを実行"""
    print(f"🧪 テストモジュール '{test_module}' を実行")
    print("=" * 50)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f"tests.{test_module}")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

def main():
    """メイン関数"""
    if len(sys.argv) > 1:
        test_module = sys.argv[1]
        return run_specific_test(test_module)
    else:
        return run_all_tests()

if __name__ == "__main__":
    sys.exit(main())