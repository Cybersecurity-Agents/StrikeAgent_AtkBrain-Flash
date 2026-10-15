"""漏洞页不能停在「正在撰写」：任务引用要保住，写失败要落到 failed。"""
from __future__ import annotations

import asyncio
import unittest
from unittest.mock import AsyncMock, patch


class ParsePiPageTests(unittest.TestCase):
    def test_braces_inside_strings_stay_in_the_page(self):
        from atkbrain.report.pi_finding_page import parse_pi_page

        raw = (
            '按事实写：\n'
            '{"summary": "入口 a {b} c", "impact": "已证明读到配置", '
            '"rating": "高 critical，二次验证打到了文件", '
            '"repro": "1. 打开入口\\n2. 提交参数\\n3. 看到文件\\n4. 判定成功", '
            '"fix": "收紧该接口鉴权"}'
        )
        spec = parse_pi_page(raw)
        self.assertEqual(spec["report_summary"], "入口 a {b} c")
        self.assertIn("收紧", spec["report_fix"])


class PageProgressTests(unittest.TestCase):
    def test_failed_progress_is_not_still_writing(self):
        from atkbrain.report.finding_report import prepare_finding_report

        out = prepare_finding_report(
            {"secondary_verified": 1, "title": "t", "severity": "high", "category": "rce"},
            progress="failed",
        )
        self.assertEqual(out["report_state"], "failed")
        self.assertNotIn("正在撰写", out["impact"])

    def test_schedule_holds_the_task_and_records_failure(self):
        from atkbrain.report import pi_finding_page as page

        async def go():
            page._SCHEDULED.clear()
            page._FAILED.clear()
            page._PAGE_TASKS.clear()
            row = {"id": "f1", "project_id": "p1", "secondary_verified": 1}
            with patch.object(page.db, "fetchone", new=AsyncMock(return_value=row)), \
                 patch("atkbrain.projects.get_project", new=AsyncMock(return_value={"id": "p1"})), \
                 patch.object(page, "ensure_pi_page", new=AsyncMock(return_value=row)):
                page.schedule_pi_page("p1", "f1")
                self.assertTrue(page._PAGE_TASKS, "撰写任务必须被强引用，避免事件循环提前回收")
                self.assertEqual(page.page_activity("f1"), "writing")
                await next(iter(page._PAGE_TASKS))
            self.assertEqual(page.page_activity("f1"), "failed")
            self.assertNotIn("f1", page._SCHEDULED)
            page.clear_page_failure("f1")
            self.assertEqual(page.page_activity("f1"), "idle")

        asyncio.run(go())


if __name__ == "__main__":
    unittest.main()
