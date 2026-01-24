#!/usr/bin/env python3
"""
同步验证脚本
检查 main 分支和 gh-pages 分支之间的关键文件是否保持一致
"""

import sys
import subprocess
from pathlib import Path
import hashlib
import json

# 定义需要同步的关键目录和文件
SYNC_DIRECTORIES = [
    'crawler',
    'processor',
    'publisher',
    'scripts',
    'config',
]

SYNC_FILES = [
    'requirements.txt',
    'README.md',
]


def run_command(cmd, capture_output=True):
    """运行 shell 命令"""
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def verify_directory_sync(branch, directory):
    """验证目录是否在指定分支中存在并同步"""
    returncode, stdout, stderr = run_command(
        f'git ls-tree -r --name-only {branch} | grep "^{directory}/" | wc -l'
    )
    if returncode != 0:
        return False, f"Failed to check {directory} on {branch}: {stderr}"
    return int(stdout) > 0, f"{directory} has {stdout} files on {branch}"


def verify_file_sync(branch, filepath):
    """验证文件是否在指定分支中存在"""
    returncode, stdout, stderr = run_command(
        f'git ls-tree -r --name-only {branch} | grep "^{filepath}$"'
    )
    if returncode != 0:
        return False, f"Failed to check {filepath} on {branch}: {stderr}"
    return len(stdout) > 0, f"{filepath} exists: {len(stdout) > 0}"


def verify_gh_pages_config():
    """验证 gh-pages 分支的配置文件"""
    checks = []

    # 检查 .nojekyll 文件
    nojekyll_exists = Path('.nojekyll').exists()
    checks.append({
        'check': '.nojekyll file exists',
        'status': 'PASS' if nojekyll_exists else 'FAIL',
        'message': '.nojekyll file found' if nojekyll_exists else '.nojekyll file missing'
    })

    # 检查 CNAME 文件
    cname_exists = Path('CNAME').exists()
    checks.append({
        'check': 'CNAME file exists',
        'status': 'PASS' if cname_exists else 'WARN',
        'message': 'CNAME file found' if cname_exists else 'CNAME file not found (optional)'
    })

    # 检查 Hugo 配置
    hugo_config = Path('blog/config.toml')
    checks.append({
        'check': 'Hugo config exists',
        'status': 'PASS' if hugo_config.exists() else 'FAIL',
        'message': 'Hugo config found' if hugo_config.exists() else 'Hugo config missing'
    })

    return checks


def main():
    """主函数"""
    print("=" * 80)
    print("🔍 同步验证脚本")
    print("=" * 80)

    all_checks = []
    failures = 0

    # 获取当前分支
    returncode, current_branch, stderr = run_command('git rev-parse --abbrev-ref HEAD')
    if returncode != 0:
        print(f"❌ Failed to get current branch: {stderr}")
        return 1

    print(f"\n📍 当前分支: {current_branch}")

    # 检查 main 分支是否存在
    returncode, stdout, stderr = run_command('git rev-parse --verify main')
    main_exists = returncode == 0

    if not main_exists:
        print("\n⚠️  main 分支不存在，跳过同步验证")
        print("   这是首次部署或 main 分支尚未创建")
        return 0

    # 验证关键目录
    print(f"\n📂 验证关键目录同步...")
    for directory in SYNC_DIRECTORIES:
        success, message = verify_directory_sync('main', directory)
        status = 'PASS' if success else 'FAIL'
        all_checks.append({
            'check': f'{directory} on main',
            'status': status,
            'message': message
        })
        if not success:
            failures += 1

    # 验证关键文件
    print(f"\n📄 验证关键文件同步...")
    for filepath in SYNC_FILES:
        success, message = verify_file_sync('main', filepath)
        status = 'PASS' if success else 'WARN'
        all_checks.append({
            'check': f'{filepath} on main',
            'status': status,
            'message': message
        })
        if not success:
            print(f"   ⚠️  {message}")

    # 如果在 gh-pages 分支，验证配置
    if current_branch == 'gh-pages':
        print(f"\n⚙️  验证 gh-pages 配置...")
        config_checks = verify_gh_pages_config()
        all_checks.extend(config_checks)
        for check in config_checks:
            if check['status'] == 'FAIL':
                failures += 1

    # 输出验证结果
    print(f"\n{'=' * 80}")
    print("📊 验证结果汇总")
    print(f"{'=' * 80}\n")

    for check in all_checks:
        icon = '✅' if check['status'] == 'PASS' else '⚠️' if check['status'] == 'WARN' else '❌'
        print(f"{icon} {check['check']}: {check['message']}")

    # 统计
    total = len(all_checks)
    passed = sum(1 for c in all_checks if c['status'] == 'PASS')
    warnings = sum(1 for c in all_checks if c['status'] == 'WARN')
    failed = failures

    print(f"\n{'=' * 80}")
    print(f"总计: {total} | 通过: {passed} | 警告: {warnings} | 失败: {failed}")
    print(f"{'=' * 80}")

    # 生成 JSON 报告
    report = {
        'total': total,
        'passed': passed,
        'warnings': warnings,
        'failed': failed,
        'checks': all_checks,
        'status': 'PASS' if failed == 0 else 'FAIL'
    }

    report_path = Path('sync_verification_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 详细报告已保存到: {report_path}")

    # 返回退出码
    return 1 if failed > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
