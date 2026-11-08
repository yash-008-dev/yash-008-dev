"""Builds analytics.svg ("mission control" card): GitHub + LeetCode + Codeforces.
Run daily by the GitHub Action. Standard library only.
Local test without network:  python scripts/stats.py --mock
"""
import os, sys, json, random, html, datetime as dt, urllib.request

GH_USER = os.environ.get("GH_USER", "asc006-git")   # the workflow passes the repo owner
LC_USER, CF_USER = "asc_006", "Adhyatma_27"
START_YEAR = 2025
OUT, CACHE = "analytics.svg", ".stats-cache.json"
G, G2, BG = "#CAFF3C", "#8AFF57", "#060D08"
UA = {"User-Agent": "profile-stats-bot"}


def http(url, data=None, headers=None):
    h = dict(UA); h.update(headers or {})
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=25) as r:
        return json.load(r)


def gql(query, variables):
    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is empty: add a repo secret named STATS_TOKEN (Settings > Secrets and variables > Actions)")
    res = http("https://api.github.com/graphql", json.dumps({"query": query, "variables": variables}).encode(),
               {"Authorization": f"bearer {token}"})
    if "errors" in res:
        raise RuntimeError(res["errors"])
    return res["data"]


# ---------------------------------------------------------------- fetchers
def fetch_github(today):
    q = """query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){contributionsCollection(from:$f,to:$t){
    totalCommitContributions totalIssueContributions totalPullRequestContributions totalPullRequestReviewContributions
    contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
    days, tot = {}, dict(commits=0, prs=0, issues=0, reviews=0)
    for y in range(START_YEAR, today.year + 1):
        c = gql(q, {"u": GH_USER, "f": f"{y}-01-01T00:00:00Z", "t": f"{y}-12-31T23:59:59Z"})["user"]["contributionsCollection"]
        tot["commits"] += c["totalCommitContributions"]; tot["prs"] += c["totalPullRequestContributions"]
        tot["issues"] += c["totalIssueContributions"]; tot["reviews"] += c["totalPullRequestReviewContributions"]
        for w in c["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                if d["date"] <= str(today):
                    days[d["date"]] = d["contributionCount"]
    return days, tot


def fetch_extra():
    q = """query($u:String!,$m:String!,$o:String!,$a:String!){
    user(login:$u){followers{totalCount}
      repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){totalCount nodes{stargazerCount
        languages(first:6,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}}
    merged:search(query:$m,type:ISSUE,first:3){issueCount nodes{... on PullRequest{title mergedAt repository{nameWithOwner}}}}
    oss:search(query:$o,type:ISSUE,first:1){issueCount}
    opened:search(query:$a,type:ISSUE,first:1){issueCount}}"""
    d = gql(q, {"u": GH_USER,
                "m": f"is:pr is:merged author:{GH_USER} sort:updated-desc",
                "o": f"is:pr is:merged author:{GH_USER} -user:{GH_USER}",
                "a": f"is:pr author:{GH_USER}"})
    repos = d["user"]["repositories"]; langs = {}
    for n in repos["nodes"]:
        for e in n["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    return {"followers": d["user"]["followers"]["totalCount"], "repos": repos["totalCount"],
            "stars": sum(n["stargazerCount"] for n in repos["nodes"]),
            "langs": sorted(langs.items(), key=lambda kv: -kv[1])[:5],
            "merged": d["merged"]["issueCount"], "oss": d["oss"]["issueCount"], "opened": d["opened"]["issueCount"],
            "recent": [{"t": n["title"], "r": n["repository"]["nameWithOwner"], "d": n["mergedAt"][:10]}
                       for n in d["merged"]["nodes"] if n]}


def fetch_cf():
    r = http(f"https://codeforces.com/api/user.info?handles={CF_USER}")["result"][0]
    hist = http(f"https://codeforces.com/api/user.rating?handle={CF_USER}")["result"]
    return {"rating": r.get("rating"), "max": r.get("maxRating"), "rank": r.get("rank", "unrated"),
            "hist": [h["newRating"] for h in hist][-14:]}


def fetch_lc():
    q = """query($u:String!){matchedUser(username:$u){submitStatsGlobal{acSubmissionNum{difficulty count}}}
    userContestRanking(username:$u){rating}}"""
    d = http("https://leetcode.com/graphql", json.dumps({"query": q, "variables": {"u": LC_USER}}).encode(),
             {"Content-Type": "application/json", "Referer": "https://leetcode.com"})["data"]
    c = {x["difficulty"]: x["count"] for x in d["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]}
    rk = d.get("userContestRanking") or {}
    return {"solved": c["All"], "easy": c["Easy"], "medium": c["Medium"], "hard": c["Hard"],
            "rating": round(rk["rating"]) if rk.get("rating") else None}


def soft(name, fn, cache):
    """Fetch; on failure keep the last good value instead of showing zeros."""
    try:
        cache[name] = fn()
    except Exception as e:
        print(f"[warn] {name} failed ({e}); using cached value", file=sys.stderr)
    return cache.get(name)


# ---------------------------------------------------------------- helpers
def streaks(days, today):
    run = longest = 0
    d = min(map(dt.date.fromisoformat, days))
    while d <= today:
        run = run + 1 if days.get(str(d), 0) else 0
        longest = max(longest, run); d += dt.timedelta(days=1)
    cur, d = 0, today
    if not days.get(str(d), 0):
        d -= dt.timedelta(days=1)
    while days.get(str(d), 0):
        cur += 1; d -= dt.timedelta(days=1)
    return cur, longest


def fmt(v):
    return "—" if v is None else str(v)


def esc(s, n=None):
    s = str(s)
    if n and len(s) > n:
        s = s[:n - 1] + "…"
    return html.escape(s)


# ---------------------------------------------------------------- render
def render(days, tot, ex, lc, cf, today):
    W, H, left, total_w = 1000, 610, 27, 946
    tot = tot or {}; ex = ex or {}; lc = lc or {}; cf = cf or {}
    cur, longest = streaks(days, today)
    last7 = [today - dt.timedelta(days=i) for i in range(6, -1, -1)]
    wk = [days.get(str(d), 0) for d in last7]
    o = []; a = o.append
    a(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Developer Analytics">
<defs>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset=".5" stop-color="{G}" stop-opacity=".12"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{G}" stroke-opacity=".05"/></pattern>
<clipPath id="clip"><rect width="{W}" height="{H}" rx="10"/></clipPath>
</defs>
<style>
text{{font-family:"Courier New",Courier,monospace}}
.pan{{animation:pan 4s ease-in-out infinite}}
.dot,.cur{{animation:blink 1.2s steps(2,end) infinite}}
.flow{{stroke-dasharray:6 10;animation:flow 1.4s linear infinite}}
.title{{animation:flick 6s linear infinite}}
.spin{{transform-box:fill-box;transform-origin:center;animation:spin 5s linear infinite}}
.rot{{transform-box:fill-box;transform-origin:center;animation:spin 40s linear infinite}}
.grow{{transform-box:fill-box;transform-origin:50% 100%;animation:grow 3s ease-in-out infinite}}
.tw{{animation:tw 3s ease-in-out infinite}}
.kpi{{animation:pan 3.2s ease-in-out infinite}}
@keyframes pan{{0%,100%{{stroke-opacity:.45}}50%{{stroke-opacity:1}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes flow{{to{{stroke-dashoffset:-32}}}}
@keyframes flick{{0%,92%,100%{{opacity:1}}93%{{opacity:.55}}94%{{opacity:1}}96%{{opacity:.7}}97%{{opacity:1}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes grow{{0%,100%{{transform:scaleY(.85)}}50%{{transform:scaleY(1)}}}}
@keyframes tw{{0%,100%{{opacity:1}}50%{{opacity:.5}}}}
</style>
<g clip-path="url(#clip)">
<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="9" fill="none" stroke="{G}" stroke-opacity=".6" stroke-width="2" class="pan"/>
<path d="M40 52H300M700 52H960" stroke="{G}" stroke-opacity=".5" fill="none" class="flow"/>
<text x="{W/2}" y="62" text-anchor="middle" font-size="34" font-weight="bold" letter-spacing="4" fill="{G}" class="title" filter="url(#glow)">DEVELOPER ANALYTICS</text>
<text x="{W/2}" y="86" text-anchor="middle" font-size="12" fill="{G2}" fill-opacity=".8">LIVE FEED // GITHUB · OPEN SOURCE · CP<tspan class="cur">_</tspan></text>''')

    def T(x, y, s, size=10, fill=G2, anchor="start", bold=False, glow=False):
        a(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
          f'{" font-weight=\"bold\"" if bold else ""}{" filter=\"url(#glow)\"" if glow else ""}>{s}</text>')

    def box(x, y, w, h, title, i):
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{G}" fill-opacity=".03" stroke="{G}" stroke-width="1.5" class="pan" style="animation-delay:{i*.4}s"/>')
        T(x + 14, y + 24, title, 12, G)
        a(f'<circle cx="{x+w-16}" cy="{y+20}" r="3" fill="{G2}" class="dot" style="animation-delay:{i*.2}s"/>')

    # ---- KPI strip
    kpis = [("CONTRIBUTIONS", sum(days.values())), ("COMMITS", tot.get("commits")), ("PRS OPENED", ex.get("opened")),
            ("PRS MERGED", ex.get("merged")), ("OPEN-SOURCE PRS", ex.get("oss")), ("CODE REVIEWS", tot.get("reviews"))]
    kw = (total_w - 5 * 10) / 6
    for i, (lab, v) in enumerate(kpis):
        kx = left + i * (kw + 10)
        a(f'<rect x="{kx:.1f}" y="104" width="{kw:.1f}" height="62" rx="8" fill="{G}" fill-opacity=".05" stroke="{G}" stroke-width="1.5" class="kpi" style="animation-delay:{i*.3}s"/>')
        T(kx + kw / 2, 138, fmt(v), 26, G, "middle", True, True)
        T(kx + kw / 2, 156, lab, 9, G2, "middle")

    # ---- row 2
    y2, h2 = 176, 190
    x1, x2, x3 = left, left + 260, left + 260 + 430 + 10
    # streak
    box(x1, y2, 250, h2, "01 // STREAK", 0)
    cx, cy = x1 + 66, y2 + 82
    a(f'<circle cx="{cx}" cy="{cy}" r="36" fill="none" stroke="{G2}" stroke-opacity=".25" stroke-width="5"/>')
    a(f'<circle cx="{cx}" cy="{cy}" r="36" fill="none" stroke="{G2}" stroke-width="5" stroke-linecap="round" stroke-dasharray="55 171" class="spin" filter="url(#glow)"/>')
    T(cx, cy + 10, cur, 28, G, "middle", True)
    T(cx, cy + 56, "CURRENT STREAK", 9, G2, "middle")
    T(x1 + 128, y2 + 62, "LONGEST", 10); T(x1 + 128, y2 + 86, longest, 24, G, bold=True, glow=True)
    T(x1 + 128, y2 + 108, "THIS WEEK", 10); T(x1 + 128, y2 + 132, sum(wk), 24, G, bold=True, glow=True)
    mx = max(max(wk), 1); bx = x1 + (250 - 7 * 18 - 6 * 12) / 2
    for k, (d, c) in enumerate(zip(last7, wk)):
        hh = max(3, 20 * c / mx); bxx = bx + k * 30
        a(f'<rect x="{bxx:.1f}" y="{y2+170-hh:.1f}" width="18" height="{hh:.1f}" rx="2" fill="{G}" fill-opacity="{1 if c else .3}" class="grow" style="animation-delay:-{k*.3:.1f}s"/>')
        T(bxx + 9, y2 + 182, "MTWTFSS"[d.weekday()], 8, G2, "middle")

    # heatmap (26 weeks)
    box(x2, y2, 430, h2, "02 // ACTIVITY", 1)
    T(x2 + 400, y2 + 24, "26 WEEKS", 10, G2, "end")
    wd = (today.weekday() + 1) % 7
    first = today - dt.timedelta(days=wd + 25 * 7)
    vals = [days.get(str(first + dt.timedelta(days=i)), 0) for i in range((today - first).days + 1)]
    mxv = max(max(vals), 1)
    for i, v in enumerate(vals):
        col, row = divmod(i, 7)
        lvl = 0 if v == 0 else min(4, -(-4 * v // mxv))
        extra = f' class="tw" style="animation-delay:-{(col*7+row)%9*.35:.2f}s"' if lvl else ""
        a(f'<rect x="{x2+20+col*15}" y="{y2+40+row*15}" width="12" height="12" rx="2" fill="{G}" fill-opacity="{[.1,.3,.5,.75,1][lvl]}"{extra}/>')
    a(f'<path d="M{x2+14} {y2+154}H{x2+416}" stroke="{G}" stroke-opacity=".25"/>')
    stats = [("BEST DAY", max(vals)), ("AVG / DAY", f"{sum(vals)/len(vals):.1f}"), ("ACTIVE DAYS", sum(1 for v in vals if v))]
    for k, (lab, v) in enumerate(stats):
        sx = x2 + 14 + k * 138
        T(sx, y2 + 172, lab, 9); T(sx + 90, y2 + 172, v, 13, G, bold=True)

    # contribution mix donut
    box(x3, y2, 246, h2, "03 // MIX", 2)
    mix = [("COMMITS", tot.get("commits") or 0), ("PULL REQ", tot.get("prs") or 0),
           ("ISSUES", tot.get("issues") or 0), ("REVIEWS", tot.get("reviews") or 0)]
    msum = sum(v for _, v in mix); r = 40; C = 2 * 3.14159265 * r; dcx, dcy = x3 + 62, y2 + 96
    a(f'<circle cx="{dcx}" cy="{dcy}" r="{r}" fill="none" stroke="{G}" stroke-opacity=".12" stroke-width="14"/>')
    a(f'<g class="rot"><g transform="rotate(-90 {dcx} {dcy})" filter="url(#glow)">')
    start = 0
    for k, (_, v) in enumerate(mix):
        seg = C * v / msum if msum else 0
        if seg > 0:
            a(f'<circle cx="{dcx}" cy="{dcy}" r="{r}" fill="none" stroke="{G}" stroke-opacity="{[1,.7,.45,.25][k]}" stroke-width="14" stroke-dasharray="{max(seg-2,0.5):.1f} {C:.1f}" stroke-dashoffset="{-start:.1f}"/>')
        start += seg
    a('</g></g>')
    T(dcx, dcy + 4, msum, 14, G, "middle", True); T(dcx, dcy + 16, "ACTIONS", 7, G2, "middle")
    for k, (lab, v) in enumerate(mix):
        ry = y2 + 70 + k * 26
        a(f'<rect x="{x3+122}" y="{ry-8}" width="9" height="9" rx="2" fill="{G}" fill-opacity="{[1,.7,.45,.25][k]}"/>')
        T(x3 + 138, ry, lab, 9); T(x3 + 232, ry + 1, v, 13, G, "end", True)

    # ---- row 3
    y3, h3 = 376, 172
    y1x, y2x, y3x = left, left + 310, left + 310 + 350
    # languages
    box(y1x, y3, 300, h3, "04 // LANGUAGES", 3)
    langs = ex.get("langs") or []
    if langs:
        ltot = sum(s for _, s in langs)
        for k, (n, s) in enumerate(langs):
            ry = y3 + 52 + k * 24; pct = 100 * s / ltot
            T(y1x + 14, ry, esc(n, 11), 10, G)
            a(f'<rect x="{y1x+104}" y="{ry-8}" width="140" height="8" rx="2" fill="{G}" fill-opacity=".1"/>')
            a(f'<rect x="{y1x+104}" y="{ry-8}" width="{max(2,140*pct/100):.0f}" height="8" rx="2" fill="{G}" fill-opacity=".85"/>')
            T(y1x + 286, ry, f"{pct:.0f}%", 9, G2, "end")
    else:
        T(y1x + 150, y3 + 90, "NO PUBLIC REPO DATA", 10, G2, "middle")
    # merged PRs
    box(y2x, y3, 340, h3, "05 // MERGED PRS", 4)
    T(y2x + 310, y3 + 24, f"OSS: {fmt(ex.get('oss'))}", 10, G2, "end")
    rec = ex.get("recent") or []
    if rec:
        for k, p in enumerate(rec[:3]):
            ry = y3 + 48 + k * 40
            a(f'<circle cx="{y2x+20}" cy="{ry+2}" r="3" fill="{G}" class="dot" style="animation-delay:{k*.3}s"/>')
            T(y2x + 32, ry, esc(p["r"], 38), 9, G2)
            T(y2x + 32, ry + 15, esc(p["t"], 36), 11, G)
            try:
                dd = dt.date.fromisoformat(p["d"]).strftime("%b %d").upper()
            except Exception:
                dd = ""
            T(y2x + 326, ry, dd, 9, G2, "end")
    else:
        T(y2x + 170, y3 + 95, "NO MERGED PRS YET", 10, G2, "middle")
    # competitive
    box(y3x, y3, 286, h3, "06 // COMPETITIVE", 5)
    rx_ = y3x + 272
    T(y3x + 14, y3 + 58, fmt(lc.get("solved")), 24, G, bold=True, glow=True); T(y3x + 14, y3 + 70, "LEETCODE SOLVED", 8)
    T(rx_, y3 + 58, fmt(lc.get("rating")), 24, G, "end", True, True); T(rx_, y3 + 70, "LEETCODE RATING", 8, G2, "end")
    e, m, h_ = (lc.get("easy") or 0), (lc.get("medium") or 0), (lc.get("hard") or 0)
    seg_total = max(e + m + h_, 1); bw = 258; sx = y3x + 14
    for op, v in ((.35, e), (.65, m), (1, h_)):
        sw = bw * v / seg_total
        if sw > 0:
            a(f'<rect x="{sx:.1f}" y="{y3+80}" width="{max(sw-1,1):.1f}" height="8" fill="{G}" fill-opacity="{op}"/>')
        sx += sw
    T(y3x + 14, y3 + 102, f"EASY {fmt(lc.get('easy'))}  MED {fmt(lc.get('medium'))}  HARD {fmt(lc.get('hard'))}", 9)
    a(f'<path d="M{y3x+14} {y3+112}H{rx_}" stroke="{G}" stroke-opacity=".3"/>')
    T(y3x + 14, y3 + 130, f"CODEFORCES // {esc(str(cf.get('rank','')).upper())}", 9)
    T(rx_, y3 + 130, f"MAX {fmt(cf.get('max'))}", 9, G2, "end")
    T(y3x + 14, y3 + 160, fmt(cf.get("rating")), 24, G, bold=True, glow=True)
    hist = cf.get("hist") or []
    if len(hist) >= 2:
        lo, hi = min(hist), max(hist); span = max(hi - lo, 1)
        px = [y3x + 110 + i * (162 / (len(hist) - 1)) for i in range(len(hist))]
        py = [y3 + 164 - 24 * (v - lo) / span for v in hist]
        a(f'<polyline points="{" ".join(f"{p:.1f},{q:.1f}" for p, q in zip(px, py))}" fill="none" stroke="{G}" stroke-width="2" stroke-linejoin="round" filter="url(#glow)"/>')
        a(f'<circle cx="{px[-1]:.1f}" cy="{py[-1]:.1f}" r="3" fill="{G}" class="dot"/>')

    # ---- footer
    a(f'<rect x="{left}" y="558" width="{total_w}" height="34" rx="6" fill="{G}" fill-opacity=".04" stroke="{G}" stroke-opacity=".5"/>')
    a(f'<circle cx="{left+18}" cy="575" r="4" fill="{G}" class="dot"/>')
    for fx, s in ((30, "STATUS: SYNCED"), (190, f"LAST SYNC: {today} UTC"),
                  (380, f"REPOS {fmt(ex.get('repos'))} · STARS {fmt(ex.get('stars'))} · FOLLOWERS {fmt(ex.get('followers'))}"),
                  (700, "AUTO-UPDATE: DAILY 23:00 IST")):
        T(left + fx, 579, s, 11, G2)
    a(f'<rect x="0" y="-80" width="{W}" height="80" fill="url(#scan)"><animateTransform attributeName="transform" type="translate" values="0 0;0 {H+80}" dur="5s" repeatCount="indefinite"/></rect></g></svg>')
    return "\n".join(o)


# ---------------------------------------------------------------- main
def main():
    today = dt.datetime.now(dt.timezone.utc).date()
    if "--mock" in sys.argv:
        random.seed(3)
        days = {str(today - dt.timedelta(days=i)): random.choice([0, 0, 1, 2, 3, 5, 8]) for i in range(450)}
        tot = dict(commits=412, prs=38, issues=9, reviews=14)
        ex = {"followers": 12, "repos": 21, "stars": 17, "opened": 41, "merged": 33, "oss": 6,
              "langs": [("Java", 52000), ("Python", 41000), ("TypeScript", 22000), ("JavaScript", 9000), ("HTML", 4000)],
              "recent": [{"t": "Fix tokenizer edge case <for> unicode & emoji input", "r": "huggingface/transformers", "d": "2026-11-02"},
                         {"t": "Add retry to client", "r": "someorg/some-long-repository-name", "d": "2026-10-21"},
                         {"t": "Docs: clarify install steps", "r": "asc006-git/halluciguard", "d": "2026-10-09"}]}
        lc = {"solved": 770, "easy": 300, "medium": 400, "hard": 70, "rating": 1816}
        cf = {"rating": 1201, "max": 1250, "rank": "newbie", "hist": [800, 900, 850, 1000, 1100, 1050, 1201]}
    else:
        cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
        days, tot = fetch_github(today)                 # if this fails the job fails; the old SVG stays
        ex, lc, cf = soft("ex", fetch_extra, cache), soft("lc", fetch_lc, cache), soft("cf", fetch_cf, cache)
        json.dump(cache, open(CACHE, "w"))
    open(OUT, "w").write(render(days, tot, ex, lc, cf, today))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
