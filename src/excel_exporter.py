"""Excel导出工具。

将测试用例导出为格式化的Excel文档。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


# 列定义
COLUMNS = [
    {"header": "用例编号", "key": "id", "width": 12},
    {"header": "用例标题", "key": "title", "width": 40},
    {"header": "优先级", "key": "priority", "width": 8},
    {"header": "用例类型", "key": "type", "width": 10},
    {"header": "所属模块", "key": "module", "width": 15},
    {"header": "来源", "key": "source", "width": 20},
    {"header": "前置条件", "key": "preconditions", "width": 30},
    {"header": "操作步骤", "key": "steps", "width": 50},
    {"header": "预期结果", "key": "expected_result", "width": 40},
    {"header": "关联需求", "key": "related_requirement", "width": 20},
]

# 样式
HEADER_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
P1_FILL = PatternFill(start_color="FCE4EC", end_color="FCE4EC", fill_type="solid")
THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)


def export_to_excel(
    test_cases: list[dict[str, Any]],
    output_path: Path | str,
) -> Path:
    """将测试用例导出为Excel。

    Args:
        test_cases: 测试用例列表
        output_path: 输出文件路径

    Returns:
        输出文件路径
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "测试用例"

    # 写入表头
    for col_idx, col_def in enumerate(COLUMNS, 1):
        cell = ws.cell(row=1, column=col_idx, value=col_def["header"])
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = THIN_BORDER
        ws.column_dimensions[get_column_letter(col_idx)].width = col_def["width"]

    # 冻结首行
    ws.freeze_panes = "A2"

    # 写入数据
    for row_idx, case in enumerate(test_cases, 2):
        for col_idx, col_def in enumerate(COLUMNS, 1):
            value = case.get(col_def["key"], "")

            # 列表类型转换为换行字符串
            if isinstance(value, list):
                value = "\n".join(f"{i+1}. {item}" for i, item in enumerate(value))

            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = THIN_BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=True)

            # P1用例标红背景
            if case.get("priority") == "P1":
                cell.fill = P1_FILL

    # 设置列宽自动调整（近似）
    for col_idx in range(1, len(COLUMNS) + 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = COLUMNS[col_idx - 1]["width"]

    # 添加自动筛选
    ws.auto_filter.ref = ws.dimensions

    wb.save(output_path)
    return output_path