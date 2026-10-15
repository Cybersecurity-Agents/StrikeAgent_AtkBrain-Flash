"""CTF 题型提示。只服务 objective=flag 的题目，写进猎面简报。"""
from __future__ import annotations

CTF_CATEGORIES = ("web", "pwn", "reverse", "misc", "crypto")

CTF_CATEGORY_LABELS = {
    "web": "Web",
    "pwn": "PWN",
    "reverse": "逆向",
    "misc": "杂项",
    "crypto": "密码学",
}

_PROMPTS = {
    "web": """题型：Web。
先读附加信息和 workspace/challenge/ 里的源码、配置、注释、备份、robots。有远程入口时，先打开入口和题面点名的路径、参数、账号；响应里像 flag 就立刻 report_flag。
不要用目录爆破或全端口扫描开局。只打题面已经露出的参数和接口（登录、上传、模板、包含、查询、反序列化）。附件里的源码优先于扫描。没有旗再对题目入口做有限侦察，禁止扫题面没给的主机，禁止超 10 万行的词表。""",
    "pwn": """题型：PWN。
附件在 workspace/challenge/。先在本机看文件类型和保护（file、checksec、strings、libc），把漏洞点从二进制里读出来，再决定要不要连远程。
没有远程地址就只在本地把 flag 从程序或附件里拿出来，不要把二进制当成网站去扫。有题目给的主机和端口时，只连接这个入口（nc / pwntools），禁止扫别的主机、禁止全端口、禁止 rockyou 和 hashcat 全库。拿到 flag 立刻 report_flag。""",
    "reverse": """题型：逆向。
只分析 workspace/challenge/ 里的程序、脚本和数据。用 strings、ltrace、反汇编把校验、密钥或硬编码 flag 还原出来。
不要对附件文件名做端口扫描，不要把程序当成 Web 目标。题面没有给出远程地址时，禁止对外连。题面给了调试或验证地址时，只连那一个。还原出的 flag 立刻 report_flag。""",
    "misc": """题型：杂项。
先看附件类型再动手：图片和音频看隐写，pcap/cap 只在包里找 flag 或凭据，压缩包看伪加密和注释，文本先识别编码（base 家族、进制、二维码）。
流量包里出现的公网地址默认不是攻击目标，除非附加信息写明那是题目入口。不要对杂项附件做目录爆破或口令字典。解出来的 flag 立刻 report_flag。""",
    "crypto": """题型：密码学。
先读 workspace/challenge/ 里的脚本和参数（n、e、c、密文、密钥、协议）。按这份脚本实际用的算法做题：小指数、共模、广播、Padding Oracle 只在题面提供了对应预言机时才用。
不要 hashcat 全库，不要 rockyou。有远程交互时，只按脚本里的协议和题目给的地址说话，不要扫旁站。算出的 flag 立刻 report_flag。""",
}


def normalize_ctf_category(raw: object) -> str:
    key = str(raw or "").strip().lower()
    aliases = {
        "web": "web",
        "pwn": "pwn",
        "rev": "reverse",
        "reverse": "reverse",
        "re": "reverse",
        "misc": "misc",
        "crypto": "crypto",
        "密码": "crypto",
        "密码学": "crypto",
        "逆向": "reverse",
        "杂项": "misc",
    }
    key = aliases.get(key, key)
    if key not in _PROMPTS:
        return ""
    return key


def ctf_category_prompt(category: object) -> str:
    return _PROMPTS.get(normalize_ctf_category(category), "")


def brief_for_category(
    category: object,
    *,
    attachments: object = None,
    offline: bool = False,
) -> str:
    """拼进猎面简报的题型说明。没有合法题型时返回空。"""
    prompt = ctf_category_prompt(category)
    if not prompt:
        return ""
    lines = [prompt]
    names: list[str] = []
    if isinstance(attachments, (list, tuple)):
        for item in attachments:
            name = str(item or "").strip()
            if name:
                names.append(name)
    if names:
        shown = "、".join(names[:12])
        lines.append(
            f"题目附件在 workspace/challenge/：{shown}。"
            "先在本机读这些文件，不要把文件名当成远程路径去扫。"
        )
    if offline:
        lines.append("本题没有远程入口。只分析附件和附加信息，拿到 flag 后 report_flag。不要扫描。")
    return "\n".join(lines)
