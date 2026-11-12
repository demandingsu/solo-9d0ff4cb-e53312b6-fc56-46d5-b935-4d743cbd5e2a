"""Regression tests for the deadline reconciliation rules.

Run with:  python -m unittest discover -s tests -v
These tests use httpx's in-process mock transport, so no network or demo
container is required.
"""

from __future__ import annotations

import unittest

import httpx

from app.crawler import check_lot, parse_notice_html


def detail(
    project: str,
    section: str,
    type_code: str,
    published: str,
    body: str,
    title: str = "公告",
) -> str:
    return f"""
    <html><body><article
      data-project-no="{project}" data-section-no="{section}"
      data-notice-type="{type_code}" data-publish-time="{published}">
      <h1>{title}</h1>
      <p>项目编号：{project}；标段编号：{section}。</p>
      <p>{body}</p>
    </article></body></html>
    """


def link_list(
    project: str,
    section: str,
    hrefs: list[str],
    next_href: str | None = None,
) -> str:
    rows = "".join(
        f'<li><a class="notice-link" data-project-no="{project}"'
        f' data-section-no="{section}" href="{href}">公告 {href}</a></li>'
        for href in hrefs
    )
    pager = f'<a rel="next" href="{next_href}">下一页</a>' if next_href else ""
    return f"<html><body><main><ul>{rows}</ul>{pager}</main></body></html>"


ORIGINAL = detail(
    "P-001", "01", "original", "2026-10-01 09:00",
    "投标截止时间：2026年11月02日 09:30。", "原公告",
)
EXTENSION = detail(
    "P-001", "01", "extension", "2026-10-10 09:00",
    "原投标截止时间为2026年11月02日 09:30，现延期至：2026年11月09日 09:30。",
    "延期公告",
)
TERMINATION = detail(
    "P-001", "01", "terminated", "2026-10-20 09:00",
    "决定终止本项目采购活动。", "终止公告",
)
OTHER_LOT_EXTENSION = detail(
    "P-001", "02", "extension", "2026-10-12 09:00",
    "投标截止时间由2026年11月03日 09:30延期至2026年11月12日 09:30。",
    "延期公告",
)


class CrawlerTests(unittest.IsolatedAsyncioTestCase):
    def make_factory(self, routes: dict[str, str], failing: set[str] | None = None):
        failing = failing or set()

        def handler(request: httpx.Request) -> httpx.Response:
            path = request.url.path
            if path in failing:
                return httpx.Response(503, text="service unavailable")
            if path not in routes:
                return httpx.Response(404, text="not found")
            return httpx.Response(
                200, text=routes[path], headers={"content-type": "text/html"}
            )

        def factory():
            return httpx.AsyncClient(
                transport=httpx.MockTransport(handler), follow_redirects=True
            )

        return factory

    async def test_termination_wins_and_old_deadline_is_not_valid(self):
        routes = {
            "/list": link_list(
                "P-001", "01", ["/d/original", "/d/extension"], next_href="/list2"
            ),
            "/list2": link_list("P-001", "01", ["/d/termination"]),
            "/d/original": ORIGINAL,
            "/d/extension": EXTENSION,
            "/d/termination": TERMINATION,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes),
            )
        ).as_dict()
        self.assertEqual(result["status"], "terminated")
        self.assertTrue(result["determinable"])
        self.assertIsNone(result["effective_deadline"])
        self.assertEqual(
            [change["type"] for change in result["changes"]],
            ["original", "extension", "terminated"],
        )
        self.assertTrue(all(change["url"] for change in result["changes"]))
        self.assertEqual(len(result["searched_pages"]), 2)

    async def test_other_lot_of_same_project_is_excluded(self):
        routes = {
            "/list": link_list("P-001", "01", ["/d/original", "/d/other-lot"]),
            "/d/original": ORIGINAL,
            "/d/other-lot": OTHER_LOT_EXTENSION,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes),
            )
        ).as_dict()
        self.assertEqual(result["status"], "ongoing")
        self.assertEqual(result["effective_deadline"], "2026-11-02 09:30")
        self.assertEqual(
            [notice["title"] for notice in result["notices"]], ["原公告"]
        )

    async def test_detail_failure_makes_result_indeterminate(self):
        routes = {
            "/list": link_list("P-001", "01", ["/d/original", "/d/extension"]),
            "/d/original": ORIGINAL,
            "/d/extension": EXTENSION,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes, failing={"/d/extension"}),
            )
        ).as_dict()
        self.assertEqual(result["status"], "unknown")
        self.assertFalse(result["determinable"])
        self.assertIsNone(result["effective_deadline"])
        self.assertIn(
            "http://test/d/extension", [f["url"] for f in result["failures"]]
        )

    async def test_missing_original_reports_searched_address(self):
        routes = {
            "/list": link_list("P-001", "01", ["/d/extension"]),
            "/d/extension": EXTENSION,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes),
            )
        ).as_dict()
        self.assertEqual(result["status"], "unknown")
        self.assertIsNone(result["effective_deadline"])
        self.assertEqual(result["failures"][0]["stage"], "missing_original")
        self.assertEqual(result["failures"][0]["url"], "http://test/list")

    async def test_extension_without_explicit_new_deadline_does_not_reuse_old_one(self):
        vague = detail(
            "P-001", "01", "extension", "2026-10-10 09:00",
            "原投标截止时间为2026年11月02日 09:30，因故延期，具体时间另行通知。",
            "延期公告",
        )
        routes = {
            "/list": link_list("P-001", "01", ["/d/original", "/d/vague"]),
            "/d/original": ORIGINAL,
            "/d/vague": vague,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes),
            )
        ).as_dict()
        self.assertEqual(result["status"], "unknown")
        self.assertIsNone(result["effective_deadline"])

    async def test_extension_explicitly_changes_the_deadline(self):
        routes = {
            "/list": link_list("P-001", "01", ["/d/original", "/d/extension"]),
            "/d/original": ORIGINAL,
            "/d/extension": EXTENSION,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes),
            )
        ).as_dict()
        self.assertEqual(result["status"], "extended")
        self.assertEqual(result["effective_deadline"], "2026-11-09 09:30")
        self.assertEqual(
            result["deadline_source_url"], "http://test/d/extension"
        )

    async def test_extension_after_termination_never_restores_deadline(self):
        """终止后又出现载明截止时间的公告：保留来源，但不产生有效时间。"""

        late_extension = detail(
            "P-001", "01", "extension", "2026-10-25 09:00",
            "原投标截止时间为2026年11月09日 09:30，现延期至：2026年11月16日 09:30。",
            "延期公告",
        )
        routes = {
            "/list": link_list(
                "P-001", "01", ["/d/original", "/d/extension"], next_href="/list2"
            ),
            "/list2": link_list(
                "P-001", "01", ["/d/termination"], next_href="/list3"
            ),
            "/list3": link_list("P-001", "01", ["/d/late-extension"]),
            "/d/original": ORIGINAL,
            "/d/extension": EXTENSION,
            "/d/termination": TERMINATION,
            "/d/late-extension": late_extension,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes),
            )
        ).as_dict()
        self.assertEqual(result["status"], "terminated")
        self.assertTrue(result["determinable"])
        self.assertIsNone(result["effective_deadline"])
        # The late notice is retained as a source ...
        self.assertEqual(
            [change["type"] for change in result["changes"]],
            ["original", "extension", "terminated", "extension"],
        )
        late_change = result["changes"][-1]
        # ... but its row must not present any valid deadline.
        self.assertIsNone(late_change["deadline_after"])
        self.assertIn("终止", late_change["summary"])
        self.assertTrue(all(change["url"] for change in result["changes"]))

    async def test_correction_after_pending_deadline_does_not_revive_old_one(self):
        """待定之后只更正非时间事项：旧期限不得恢复，结论仍为无法判定。"""

        pending = detail(
            "P-001", "01", "extension", "2026-10-10 09:00",
            "原投标截止时间为2026年11月02日 09:30，因故延期，具体时间另行通知。",
            "延期公告",
        )
        correction = detail(
            "P-001", "01", "extension", "2026-10-15 09:00",
            "原投标截止时间 2026年11月02日 09:30 仅作背景引用；本公告仅更正投标保证金账户信息。",
            "更正公告",
        )
        routes = {
            "/list": link_list(
                "P-001", "01", ["/d/original"], next_href="/list2"
            ),
            "/list2": link_list("P-001", "01", ["/d/pending"], next_href="/list3"),
            "/list3": link_list("P-001", "01", ["/d/correction"]),
            "/d/original": ORIGINAL,
            "/d/pending": pending,
            "/d/correction": correction,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes),
            )
        ).as_dict()
        self.assertEqual(result["status"], "unknown")
        self.assertFalse(result["determinable"])
        self.assertIsNone(result["effective_deadline"])
        correction_change = result["changes"][-1]
        self.assertIsNone(correction_change["deadline_after"])
        self.assertIn("非时间事项", correction_change["summary"])
        # The pending notice, not the correction, is flagged as the blocker.
        self.assertEqual(
            result["failures"][0]["url"], "http://test/d/pending"
        )

    async def test_explicit_new_deadline_after_pending_restores_it(self):
        """待定之后，只有公告明确给出新时间才能恢复有效期限。"""

        pending = detail(
            "P-001", "01", "extension", "2026-10-10 09:00",
            "原投标截止时间为2026年11月02日 09:30，因故延期，具体时间另行通知。",
            "延期公告",
        )
        confirmed = detail(
            "P-001", "01", "extension", "2026-10-18 09:00",
            "投标截止时间现变更为 2026年11月20日 10:00。",
            "延期公告",
        )
        routes = {
            "/list": link_list(
                "P-001", "01", ["/d/original"], next_href="/list2"
            ),
            "/list2": link_list("P-001", "01", ["/d/pending"], next_href="/list3"),
            "/list3": link_list("P-001", "01", ["/d/confirmed"]),
            "/d/original": ORIGINAL,
            "/d/pending": pending,
            "/d/confirmed": confirmed,
        }
        result = (
            await check_lot(
                "http://test/list", "P-001", "01",
                client_factory=self.make_factory(routes),
            )
        ).as_dict()
        self.assertEqual(result["status"], "extended")
        self.assertTrue(result["determinable"])
        self.assertEqual(result["effective_deadline"], "2026-11-20 10:00")
        self.assertEqual(
            result["deadline_source_url"], "http://test/d/confirmed"
        )
        after_values = [change["deadline_after"] for change in result["changes"]]
        self.assertEqual(
            after_values,
            ["2026-11-02 09:30", None, "2026-11-20 10:00"],
        )


class ParseTests(unittest.TestCase):
    def test_old_and_new_dates_on_same_line(self):
        parsed = parse_notice_html(EXTENSION, "http://test/extension")
        self.assertTrue(parsed.deadline.explicit)
        self.assertEqual(
            parsed.deadline.value.strftime("%Y-%m-%d %H:%M"), "2026-11-09 09:30"
        )

    def test_extension_without_new_date_is_not_explicit(self):
        text = detail(
            "P-001", "01", "extension", "2026-10-10 09:00",
            "原投标截止时间为2026年11月02日 09:30，具体延期时间另行通知。",
        )
        parsed = parse_notice_html(text, "http://test/x")
        self.assertFalse(parsed.deadline.explicit)
        self.assertTrue(parsed.deadline.unclear)

    def test_non_time_correction_is_not_a_postponement(self):
        # The generic extension type tag and a quoted old date must not make a
        # correction that only touches non-time matters look like a postponement.
        text = detail(
            "P-001", "01", "extension", "2026-10-15 09:00",
            "原投标截止时间 2026年11月02日 09:30 仅作背景引用；本公告仅更正投标保证金账户信息。",
            "更正公告",
        )
        parsed = parse_notice_html(text, "http://test/x")
        self.assertEqual(parsed.notice_type, "extension")
        self.assertFalse(parsed.is_postponement)
        self.assertFalse(parsed.deadline.explicit)
        self.assertFalse(parsed.deadline.unclear)


if __name__ == "__main__":
    unittest.main()
