"""会话管理服务。

管理测试用例生成过程中的中间状态。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SessionService:
    """测试用例生成会话管理。

    管理以下中间状态：
    - business_tree.json — 业务树
    - review_result.json — 评审结果
    - outline.json — 测试大纲
    - test_cases.json — 测试用例
    """

    def __init__(self, project_dir: Path | str = ".test-case") -> None:
        self.project_dir = Path(project_dir)

    def ensure_project_dir(self) -> None:
        """确保项目目录存在。"""
        self.project_dir.mkdir(parents=True, exist_ok=True)

    def save_constitution(self, content: str) -> Path:
        """保存宪法文件。"""
        self.ensure_project_dir()
        path = self.project_dir / "constitution.md"
        path.write_text(content, encoding="utf-8")
        return path

    def load_constitution(self) -> str | None:
        """加载宪法文件。"""
        path = self.project_dir / "constitution.md"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None

    def save_business_tree(self, tree: dict[str, Any]) -> Path:
        """保存业务树。"""
        self.ensure_project_dir()
        path = self.project_dir / "business_tree.json"
        path.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load_business_tree(self) -> dict[str, Any] | None:
        """加载业务树。"""
        path = self.project_dir / "business_tree.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def save_review_result(self, result: dict[str, Any]) -> Path:
        """保存评审结果。"""
        self.ensure_project_dir()
        path = self.project_dir / "review_result.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load_review_result(self) -> dict[str, Any] | None:
        """加载评审结果。"""
        path = self.project_dir / "review_result.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def save_outline(self, outline: dict[str, Any]) -> Path:
        """保存测试大纲。"""
        self.ensure_project_dir()
        path = self.project_dir / "outline.json"
        path.write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load_outline(self) -> dict[str, Any] | None:
        """加载测试大纲。"""
        path = self.project_dir / "outline.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def save_test_cases(self, cases: dict[str, Any]) -> Path:
        """保存测试用例。"""
        self.ensure_project_dir()
        path = self.project_dir / "test_cases.json"
        path.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load_test_cases(self) -> dict[str, Any] | None:
        """加载测试用例。"""
        path = self.project_dir / "test_cases.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def get_status(self) -> dict[str, bool]:
        """获取当前项目状态。"""
        return {
            "has_constitution": (self.project_dir / "constitution.md").exists(),
            "has_business_tree": (self.project_dir / "business_tree.json").exists(),
            "has_review_result": (self.project_dir / "review_result.json").exists(),
            "has_outline": (self.project_dir / "outline.json").exists(),
            "has_test_cases": (self.project_dir / "test_cases.json").exists(),
        }

    def reset(self) -> None:
        """重置项目（删除所有文件）。"""
        import shutil
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir)