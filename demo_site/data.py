"""In-memory fixture for the offline demonstration notice board.

The pages deliberately put the original notice and its follow-up notices on
different result pages.  A second lot of the same project is included so that
the checker's lot isolation can be demonstrated.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Notice:
    slug: str
    project_no: str
    section_no: str
    notice_type: str  # original | extension | terminated | result | other
    title: str
    published_at: str
    deadline: str | None
    deadline_label: str | None
    body: tuple[str, ...]
    project_name: str


NOTICES: tuple[Notice, ...] = (
    Notice(
        slug="DEMO-2026-001-01-original",
        project_no="DEMO-2026-001",
        section_no="01",
        notice_type="original",
        title="滨河智慧园区设备采购项目（01标段）招标公告",
        published_at="2026-10-08 09:00",
        deadline="2026-11-02 09:30",
        deadline_label="投标截止时间",
        body=(
            "受采购人委托，现对滨河智慧园区设备采购项目（01标段）进行公开招标。",
            "项目编号：DEMO-2026-001；标段编号：01。",
            "投标截止时间：2026年11月02日 09:30（北京时间）。",
            "投标文件应在上述截止时间前递交至滨河公共资源交易中心。",
        ),
        project_name="滨河智慧园区设备采购项目",
    ),
    Notice(
        slug="DEMO-2026-001-02-original",
        project_no="DEMO-2026-001",
        section_no="02",
        notice_type="original",
        title="滨河智慧园区设备采购项目（02标段）招标公告",
        published_at="2026-10-09 10:00",
        deadline="2026-11-03 09:30",
        deadline_label="投标截止时间",
        body=(
            "受采购人委托，现对滨河智慧园区设备采购项目（02标段）进行公开招标。",
            "项目编号：DEMO-2026-001；标段编号：02。",
            "投标截止时间：2026年11月03日 09:30（北京时间）。",
            "本标段与 01 标段分别评审，投标人应按标段分别递交文件。",
        ),
        project_name="滨河智慧园区设备采购项目",
    ),
    Notice(
        slug="DEMO-2026-002-A-original",
        project_no="DEMO-2026-002",
        section_no="A",
        notice_type="original",
        title="北岸道路照明提升项目（A包）采购公告",
        published_at="2026-10-10 14:20",
        deadline="2026-11-20 14:00",
        deadline_label="响应文件提交截止时间",
        body=(
            "北岸道路照明提升项目（A包）采用竞争性磋商方式采购。",
            "项目编号：DEMO-2026-002；包号：A。",
            "响应文件提交截止时间：2026年11月20日 14:00。",
            "响应文件提交地点：北岸区公共资源交易中心三楼。",
        ),
        project_name="北岸道路照明提升项目",
    ),
    Notice(
        slug="DEMO-2026-001-01-extension",
        project_no="DEMO-2026-001",
        section_no="01",
        notice_type="extension",
        title="滨河智慧园区设备采购项目（01标段）延期公告",
        published_at="2026-10-18 16:00",
        deadline="2026-11-09 09:30",
        deadline_label="投标截止时间（延期后）",
        body=(
            "因答疑澄清，现对本项目 01 标段投标截止时间作如下延期。",
            "项目编号：DEMO-2026-001；标段编号：01。",
            "原投标截止时间为 2026年11月02日 09:30，现延期至：2026年11月09日 09:30。",
            "开标时间同步顺延至 2026年11月09日 09:30，开标地点不变。",
        ),
        project_name="滨河智慧园区设备采购项目",
    ),
    Notice(
        slug="DEMO-2026-001-02-extension",
        project_no="DEMO-2026-001",
        section_no="02",
        notice_type="extension",
        title="滨河智慧园区设备采购项目（02标段）延期公告",
        published_at="2026-10-20 11:00",
        deadline="2026-11-12 09:30",
        deadline_label="投标截止时间（延期后）",
        body=(
            "因投标人不足三家，现对 02 标段投标截止时间进行延期。",
            "项目编号：DEMO-2026-001；标段编号：02。",
            "原投标截止时间为 2026年11月03日 09:30，现变更为 2026年11月12日 09:30。",
            "其他内容不变。",
        ),
        project_name="滨河智慧园区设备采购项目",
    ),
    Notice(
        slug="DEMO-2026-003-B-original",
        project_no="DEMO-2026-003",
        section_no="B",
        notice_type="original",
        title="西岭绿化养护服务项目（B包）询价公告",
        published_at="2026-10-22 09:30",
        deadline="2026-12-02 10:00",
        deadline_label="报价截止时间",
        body=(
            "西岭绿化养护服务项目（B包）进行询价采购。",
            "项目编号：DEMO-2026-003；包号：B。",
            "报价截止时间：2026年12月02日 10:00。",
        ),
        project_name="西岭绿化养护服务项目",
    ),
    Notice(
        slug="DEMO-2026-002-A-extension",
        project_no="DEMO-2026-002",
        section_no="A",
        notice_type="extension",
        title="北岸道路照明提升项目（A包）延期公告",
        published_at="2026-10-26 15:30",
        deadline="2026-11-25 14:00",
        deadline_label="响应文件提交截止时间（变更后）",
        body=(
            "根据采购人通知，北岸道路照明提升项目 A 包响应文件提交截止时间调整如下。",
            "项目编号：DEMO-2026-002；包号：A。",
            "原响应文件提交截止时间为 2026年11月20日 14:00，现调整为 2026年11月25日 14:00。",
            "磋商时间相应调整为 2026年11月26日 09:30。",
        ),
        project_name="北岸道路照明提升项目",
    ),
    Notice(
        slug="DEMO-2026-001-01-terminated",
        project_no="DEMO-2026-001",
        section_no="01",
        notice_type="terminated",
        title="滨河智慧园区设备采购项目（01标段）终止公告",
        published_at="2026-10-28 10:00",
        deadline=None,
        deadline_label=None,
        body=(
            "因采购需求发生重大调整，经采购人研究决定，终止滨河智慧园区设备采购项目 01 标段本次采购活动。",
            "项目编号：DEMO-2026-001；标段编号：01。",
            "已递交的投标文件将按原渠道退还。后续采购安排另行公告。",
        ),
        project_name="滨河智慧园区设备采购项目",
    ),
    Notice(
        slug="DEMO-2026-002-A-result",
        project_no="DEMO-2026-002",
        section_no="A",
        notice_type="result",
        title="北岸道路照明提升项目（A包）成交结果公告",
        published_at="2026-10-29 09:00",
        deadline=None,
        deadline_label=None,
        body=(
            "北岸道路照明提升项目（A包）成交结果公告。",
            "项目编号：DEMO-2026-002；包号：A。",
            "本公告为结果公告，不改变响应文件提交截止时间。",
        ),
        project_name="北岸道路照明提升项目",
    ),
    # ------------------------------------------------------------------
    # 终止后又出现载明截止时间的公告：来源必须保留，但不得恢复有效时间。
    # 四份公告分处第 4–7 页，用于跨页核对。
    # ------------------------------------------------------------------
    Notice(
        slug="DEMO-2026-004-C-original",
        project_no="DEMO-2026-004",
        section_no="C",
        notice_type="original",
        title="东河水利设施维护项目（C包）采购公告",
        published_at="2026-11-02 09:00",
        deadline="2026-11-23 09:30",
        deadline_label="响应文件提交截止时间",
        body=(
            "东河水利设施维护项目（C包）采用竞争性磋商方式采购。",
            "项目编号：DEMO-2026-004；包号：C。",
            "响应文件提交截止时间：2026年11月23日 09:30（北京时间）。",
            "响应文件递交地点：东河区公共资源交易中心二楼。",
        ),
        project_name="东河水利设施维护项目",
    ),
    Notice(
        slug="DEMO-2026-004-C-extension",
        project_no="DEMO-2026-004",
        section_no="C",
        notice_type="extension",
        title="东河水利设施维护项目（C包）延期公告",
        published_at="2026-11-05 15:00",
        deadline="2026-11-30 09:30",
        deadline_label="响应文件提交截止时间（延期后）",
        body=(
            "因采购文件需要澄清，现对 C 包响应文件提交截止时间作如下延期。",
            "项目编号：DEMO-2026-004；包号：C。",
            "原响应文件提交截止时间为 2026年11月23日 09:30，现延期至：2026年11月30日 09:30。",
            "磋商开始时间同步顺延，磋商地点不变。",
        ),
        project_name="东河水利设施维护项目",
    ),
    Notice(
        slug="DEMO-2026-004-C-terminated",
        project_no="DEMO-2026-004",
        section_no="C",
        notice_type="terminated",
        title="东河水利设施维护项目（C包）终止公告",
        published_at="2026-11-09 10:30",
        deadline=None,
        deadline_label=None,
        body=(
            "因采购人采购计划调整，经研究决定，终止东河水利设施维护项目 C 包本次采购活动。",
            "项目编号：DEMO-2026-004；包号：C。",
            "自本公告发布之日起不再接受响应文件，已递交文件将按原渠道退还。后续安排另行公告。",
        ),
        project_name="东河水利设施维护项目",
    ),
    Notice(
        slug="DEMO-2026-004-C-extension-after-termination",
        project_no="DEMO-2026-004",
        section_no="C",
        notice_type="extension",
        title="东河水利设施维护项目（C包）延期公告（终止后发布）",
        published_at="2026-11-12 14:00",
        deadline="2026-12-07 09:30",
        deadline_label="响应文件提交截止时间（延期后）",
        body=(
            "项目编号：DEMO-2026-004；包号：C。",
            "原响应文件提交截止时间为 2026年11月30日 09:30，现延期至：2026年12月07日 09:30。",
            "说明：本公告系经办环节留痕补发；本项目 C 包终止公告已生效，本公告载明的时间不恢复投标安排。",
        ),
        project_name="东河水利设施维护项目",
    ),
    # ------------------------------------------------------------------
    # 延期时间待定后，只更正非时间事项：旧期限不得重新显示为有效。
    # 三份公告跨第 5–7 页。
    # ------------------------------------------------------------------
    Notice(
        slug="DEMO-2026-005-D-original",
        project_no="DEMO-2026-005",
        section_no="D",
        notice_type="original",
        title="南塬智慧农业设备采购项目（D包）招标公告",
        published_at="2026-11-03 09:30",
        deadline="2026-11-24 09:30",
        deadline_label="投标截止时间",
        body=(
            "南塬智慧农业设备采购项目（D包）进行公开招标。",
            "项目编号：DEMO-2026-005；标段编号：D。",
            "投标截止时间：2026年11月24日 09:30（北京时间）。",
            "投标文件递交至南塬市公共资源交易中心四楼开标室。",
        ),
        project_name="南塬智慧农业设备采购项目",
    ),
    Notice(
        slug="DEMO-2026-005-D-extension-pending",
        project_no="DEMO-2026-005",
        section_no="D",
        notice_type="extension",
        title="南塬智慧农业设备采购项目（D包）延期公告（时间待定）",
        published_at="2026-11-06 16:30",
        deadline=None,
        deadline_label=None,
        body=(
            "因招标方案需进一步论证，现暂缓 D 包投标截止安排。",
            "项目编号：DEMO-2026-005；标段编号：D。",
            "原投标截止时间为 2026年11月24日 09:30，因故延期，新的投标截止时间待定，具体时间另行通知。",
            "请各投标人留意后续公告，合理安排投标准备。",
        ),
        project_name="南塬智慧农业设备采购项目",
    ),
    Notice(
        slug="DEMO-2026-005-D-correction",
        project_no="DEMO-2026-005",
        section_no="D",
        notice_type="extension",
        title="南塬智慧农业设备采购项目（D包）更正公告",
        published_at="2026-11-13 11:00",
        deadline=None,
        deadline_label=None,
        body=(
            "现就南塬智慧农业设备采购项目 D 包招标文件作如下更正。",
            "项目编号：DEMO-2026-005；标段编号：D。",
            "更正事项：投标保证金收款账户由原账户变更为公告附件所列新账户，联系人及咨询电话同步更正。",
            "原投标截止时间 2026年11月24日 09:30 仅作背景引用；本公告仅更正上述账户与联系信息，不涉及投标截止时间安排。",
        ),
        project_name="南塬智慧农业设备采购项目",
    ),
    # ------------------------------------------------------------------
    # 延期时间待定后，后续公告明确给出新时间：期限恢复为可判定。
    # 三份公告跨第 5–7 页。
    # ------------------------------------------------------------------
    Notice(
        slug="DEMO-2026-006-E-original",
        project_no="DEMO-2026-006",
        section_no="E",
        notice_type="original",
        title="北港冷链仓储建设项目（E包）采购公告",
        published_at="2026-11-04 10:00",
        deadline="2026-11-25 14:00",
        deadline_label="响应文件提交截止时间",
        body=(
            "北港冷链仓储建设项目（E包）采用竞争性谈判方式采购。",
            "项目编号：DEMO-2026-006；包号：E。",
            "响应文件提交截止时间：2026年11月25日 14:00（北京时间）。",
            "响应文件递交地点：北港新区政务服务中心三楼。",
        ),
        project_name="北港冷链仓储建设项目",
    ),
    Notice(
        slug="DEMO-2026-006-E-extension-pending",
        project_no="DEMO-2026-006",
        section_no="E",
        notice_type="extension",
        title="北港冷链仓储建设项目（E包）延期公告（时间待定）",
        published_at="2026-11-07 17:00",
        deadline=None,
        deadline_label=None,
        body=(
            "因谈判文件需补充技术参数，现暂缓 E 包响应文件提交安排。",
            "项目编号：DEMO-2026-006；包号：E。",
            "原响应文件提交截止时间为 2026年11月25日 14:00，因故延期，新的响应文件提交截止时间待定，具体时间另行通知。",
        ),
        project_name="北港冷链仓储建设项目",
    ),
    Notice(
        slug="DEMO-2026-006-E-extension-confirmed",
        project_no="DEMO-2026-006",
        section_no="E",
        notice_type="extension",
        title="北港冷链仓储建设项目（E包）延期公告（明确新时间）",
        published_at="2026-11-16 09:30",
        deadline="2026-12-09 14:00",
        deadline_label="响应文件提交截止时间（延期后）",
        body=(
            "北港冷链仓储建设项目 E 包新的响应文件提交安排已确定。",
            "项目编号：DEMO-2026-006；包号：E。",
            "响应文件提交截止时间现变更为 2026年12月09日 14:00（北京时间），请据此安排响应文件递交。",
            "谈判开始时间调整为 2026年12月10日 09:30，谈判地点不变。",
        ),
        project_name="北港冷链仓储建设项目",
    ),
)


NOTICE_BY_SLUG = {notice.slug: notice for notice in NOTICES}
PAGE_SIZE = 3
NOTICES_ASC = tuple(sorted(NOTICES, key=lambda n: n.published_at))

TYPE_LABELS = {
    "original": "原公告",
    "extension": "延期公告",
    "terminated": "终止公告",
    "result": "结果公告",
    "other": "其他公告",
}


def page_count() -> int:
    return (len(NOTICES_ASC) + PAGE_SIZE - 1) // PAGE_SIZE


def notices_on_page(page: int) -> list[Notice]:
    start = (page - 1) * PAGE_SIZE
    return list(NOTICES_ASC[start : start + PAGE_SIZE])
