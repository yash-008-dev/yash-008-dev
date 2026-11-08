"""Builds analytics.svg (GitHub + LeetCode + Codeforces) in the neon theme.
Run by the GitHub Action once a day. Standard library only.
Local test without any network:  python scripts/stats.py --mock
"""
import os, sys, json, random, datetime as dt, urllib.request

GH_USER, LC_USER, CF_USER = "asc006-git", "asc_006", "Adhyatma_27"
START_YEAR = 2025                      # first year to count contributions from
OUT, CACHE = "analytics.svg", ".stats-cache.json"
G, G2, BG = "#CAFF3C", "#8AFF57", "#060D08"
UA = {"User-Agent": "profile-stats-bot"}


def http(url, data=None, headers=None):
    h = dict(UA); h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


# ---------------------------------------------------------------- fetchers
def fetch_github(today):
    token = os.environ["GH_TOKEN"]
    q = """query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){
    contributionsCollection(from:$f,to:$t){contributionCalendar{
    weeks{contributionDays{date contributionCount}}}}}}"""
    days = {}
    for y in range(START_YEAR, today.year + 1):
        body = json.dumps({"query": q, "variables": {
            "u": GH_USER, "f": f"{y}-01-01T00:00:00Z", "t": f"{y}-12-31T23:59:59Z"}}).encode()
        res = http("https://api.github.com/graphql", body, {"Authorization": f"bearer {token}"})
        if "errors" in res:
            raise RuntimeError(res["errors"])
        cal = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        for w in cal["weeks"]:
            for d in w["contributionDays"]:
                if d["date"] <= str(today):
                    days[d["date"]] = d["contributionCount"]
    return days


def fetch_cf():
    r = http(f"https://codeforces.com/api/user.info?handles={CF_USER}")["result"][0]
    return {"rating": r.get("rating"), "max": r.get("maxRating"), "rank": r.get("rank", "unrated")}


def fetch_lc():
    q = """query($u:String!){matchedUser(username:$u){submitStatsGlobal{acSubmissionNum{difficulty count}}}
    userContestRanking(username:$u){rating}}"""
    body = json.dumps({"query": q, "variables": {"u": LC_USER}}).encode()
    d = http("https://leetcode.com/graphql", body,
             {"Content-Type": "application/json", "Referer": "https://leetcode.com"})["data"]
    c = {x["difficulty"]: x["count"] for x in d["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]}
    rk = d.get("userContestRanking") or {}
    return {"solved": c["All"], "easy": c["Easy"], "medium": c["Medium"], "hard": c["Hard"],
            "rating": round(rk["rating"]) if rk.get("rating") else None}


def soft(name, fn, cache):
    """Try to fetch; on any failure keep yesterday's value instead of showing zeros."""
    try:
        cache[name] = fn()
    except Exception as e:
        print(f"[warn] {name} failed ({e}); using cached value", file=sys.stderr)
    return cache.get(name)


# ---------------------------------------------------------------- calculations
def streaks(days, today):
    run = longest = 0
    d = min(map(dt.date.fromisoformat, days)); 
    while d <= today:
        run = run + 1 if days.get(str(d), 0) else 0
        longest = max(longest, run); d += dt.timedelta(days=1)
    cur, d = 0, today
    if not days.get(str(d), 0):          # today not finished yet: don't break the streak
        d -= dt.timedelta(days=1)
    while days.get(str(d), 0):
        cur += 1; d -= dt.timedelta(days=1)
    return cur, longest


# ---------------------------------------------------------------- rendering
def fmt(v):
    return "—" if v is None else str(v)


def render(days, lc, cf, today):
    W, H = 1000, 400
    left, gap, py, ph = 27, 14, 104, 222
    widths = [300, 318, 300]
    xs = [left, left + 300 + gap, left + 300 + 318 + 2 * gap]
    total = sum(days.values())
    cur, longest = streaks(days, today)
    last7 = [(today - dt.timedelta(days=i)) for i in range(6, -1, -1)]
    wk = [days.get(str(d), 0) for d in last7]
    o = []; a = o.append
    a(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Developer Analytics">
<defs>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G}" stop-opacity="0"/><stop offset=".5" stop-color="{G}" stop-opacity=".14"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></linearGradient>
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
.grow{{transform-box:fill-box;transform-origin:50% 100%;animation:grow 3s ease-in-out infinite}}
.tw{{animation:tw 3s ease-in-out infinite}}
@keyframes pan{{0%,100%{{stroke-opacity:.5}}50%{{stroke-opacity:1}}}}
@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes flow{{to{{stroke-dashoffset:-32}}}}
@keyframes flick{{0%,92%,100%{{opacity:1}}93%{{opacity:.55}}94%{{opacity:1}}96%{{opacity:.7}}97%{{opacity:1}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes grow{{0%,100%{{transform:scaleY(.85)}}50%{{transform:scaleY(1)}}}}
@keyframes tw{{0%,100%{{opacity:1}}50%{{opacity:.55}}}}
</style>
<g clip-path="url(#clip)">
<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="9" fill="none" stroke="{G}" stroke-opacity=".6" stroke-width="2" class="pan"/>
<path d="M40 52H300M700 52H960" stroke="{G}" stroke-opacity=".5" fill="none" class="flow"/>
<text x="{W/2}" y="62" text-anchor="middle" font-size="34" font-weight="bold" letter-spacing="4" fill="{G}" class="title" filter="url(#glow)">DEVELOPER ANALYTICS</text>
<text x="{W/2}" y="86" text-anchor="middle" font-size="12" fill="{G2}" fill-opacity=".8">LIVE FEED // GITHUB · LEETCODE · CODEFORCES<tspan class="cur">_</tspan></text>''')

    def panel(i, title):
        x = xs[i]
        a(f'<rect x="{x}" y="{py}" width="{widths[i]}" height="{ph}" rx="8" fill="{G}" fill-opacity=".03" stroke="{G}" stroke-width="1.5" class="pan" style="animation-delay:{i*.4}s"/>')
        a(f'<text x="{x+14}" y="{py+24}" font-size="12" fill="{G}">{title}</text>')
        a(f'<circle cx="{x+widths[i]-16}" cy="{py+20}" r="3" fill="{G2}" class="dot" style="animation-delay:{i*.2}s"/>')
        return x

    # ---- panel 1: GitHub
    x = panel(0, "01 // GITHUB")
    rcx, rcy = x + 62, py + 92
    a(f'<circle cx="{rcx}" cy="{rcy}" r="38" fill="none" stroke="{G2}" stroke-opacity=".25" stroke-width="5"/>')
    a(f'<circle cx="{rcx}" cy="{rcy}" r="38" fill="none" stroke="{G2}" stroke-width="5" stroke-linecap="round" stroke-dasharray="60 179" class="spin" filter="url(#glow)"/>')
    a(f'<text x="{rcx}" y="{rcy+10}" text-anchor="middle" font-size="28" font-weight="bold" fill="{G}">{cur}</text>')
    a(f'<text x="{rcx}" y="{rcy+58}" text-anchor="middle" font-size="9" fill="{G2}">CURRENT STREAK</text>')
    for k, (lab, val) in enumerate([("TOTAL", total), ("LONGEST STREAK", longest)]):
        yy = py + 62 + k * 46
        a(f'<text x="{x+130}" y="{yy}" font-size="10" fill="{G2}">{lab}</text>')
        a(f'<text x="{x+130}" y="{yy+26}" font-size="26" font-weight="bold" fill="{G}" filter="url(#glow)">{val}</text>')
    a(f'<text x="{x+14}" y="{py+170}" font-size="10" fill="{G2}">LAST 7 DAYS: {sum(wk)}</text>')
    mx = max(max(wk), 1); bx = x + (300 - 210) / 2
    for k, (d, c) in enumerate(zip(last7, wk)):
        h = max(3, 28 * c / mx); bxx = bx + k * 32
        a(f'<rect x="{bxx:.1f}" y="{py+202-h:.1f}" width="18" height="{h:.1f}" rx="2" fill="{G}" fill-opacity="{1 if c else .3}" class="grow" style="animation-delay:-{k*.3:.1f}s"/>')
        a(f'<text x="{bxx+9:.1f}" y="{py+215}" text-anchor="middle" font-size="8" fill="{G2}">{"MTWTFSS"[d.weekday()]}</text>')

    # ---- panel 2: heatmap (13 weeks)
    x = panel(1, "02 // ACTIVITY")
    a(f'<text x="{x+widths[1]-30}" y="{py+24}" text-anchor="end" font-size="10" fill="{G2}">13 WEEKS</text>')
    wd = (today.weekday() + 1) % 7                     # Sunday = 0
    first = today - dt.timedelta(days=wd + 12 * 7)
    vals = [days.get(str(first + dt.timedelta(days=i)), 0) for i in range((today - first).days + 1)]
    mxv = max(max(vals), 1); gx = x + (318 - 260) / 2
    for i, v in enumerate(vals):
        col, row = divmod(i, 7)
        lvl = 0 if v == 0 else min(4, -(-4 * v // mxv))
        fo = [.1, .3, .5, .75, 1][lvl]
        cls = ' class="tw"' if lvl else ""
        dl = f' style="animation-delay:-{(col*7+row)%9*.35:.2f}s"' if lvl else ""
        a(f'<rect x="{gx+col*20:.0f}" y="{py+44+row*20}" width="16" height="16" rx="3" fill="{G}" fill-opacity="{fo}"{cls}{dl}/>')
    a(f'<text x="{x+159}" y="{py+206}" text-anchor="middle" font-size="10" fill="{G2}">{sum(vals)} CONTRIBUTIONS · BEST DAY {max(vals)}</text>')

    # ---- panel 3: competitive programming
    x = panel(2, "03 // COMPETITIVE"); r = x + 286
    lc = lc or {}; cf = cf or {}
    a(f'<text x="{x+14}" y="{py+46}" font-size="10" fill="{G2}">LEETCODE</text>')
    a(f'<text x="{x+14}" y="{py+76}" font-size="28" font-weight="bold" fill="{G}" filter="url(#glow)">{fmt(lc.get("rating"))}</text>')
    a(f'<text x="{x+14}" y="{py+89}" font-size="8" fill="{G2}">CONTEST RATING</text>')
    a(f'<text x="{r}" y="{py+76}" text-anchor="end" font-size="28" font-weight="bold" fill="{G}" filter="url(#glow)">{fmt(lc.get("solved"))}</text>')
    a(f'<text x="{r}" y="{py+89}" text-anchor="end" font-size="8" fill="{G2}">SOLVED</text>')
    cnt = [lc.get("easy"), lc.get("medium"), lc.get("hard")]
    mxc = max([c for c in cnt if c] or [1])
    for k, (lab, c) in enumerate(zip("EMH", cnt)):
        yy = py + 101 + k * 14
        w = 0 if c is None else max(2, 190 * c / mxc)
        a(f'<text x="{x+14}" y="{yy+8}" font-size="9" fill="{G2}">{lab}</text>')
        a(f'<rect x="{x+28}" y="{yy}" width="190" height="8" rx="2" fill="{G}" fill-opacity=".1"/>')
        a(f'<rect x="{x+28}" y="{yy}" width="{w:.0f}" height="8" rx="2" fill="{G}" fill-opacity=".85"/>')
        a(f'<text x="{r}" y="{yy+8}" text-anchor="end" font-size="9" fill="{G2}">{fmt(c)}</text>')
    a(f'<path d="M{x+14} {py+148}H{r}" stroke="{G}" stroke-opacity=".3"/>')
    rank = str(cf.get("rank", "")).upper()
    a(f'<text x="{x+14}" y="{py+168}" font-size="10" fill="{G2}">CODEFORCES // {rank}</text>')
    a(f'<text x="{x+14}" y="{py+198}" font-size="28" font-weight="bold" fill="{G}" filter="url(#glow)">{fmt(cf.get("rating"))}</text>')
    a(f'<text x="{x+14}" y="{py+211}" font-size="8" fill="{G2}">RATING</text>')
    a(f'<text x="{r}" y="{py+198}" text-anchor="end" font-size="28" font-weight="bold" fill="{G}" filter="url(#glow)">{fmt(cf.get("max"))}</text>')
    a(f'<text x="{r}" y="{py+211}" text-anchor="end" font-size="8" fill="{G2}">MAX RATING</text>')

    # ---- footer
    a(f'''<g font-size="11" fill="{G2}">
<rect x="{left}" y="346" width="946" height="34" rx="6" fill="{G}" fill-opacity=".04" stroke="{G}" stroke-opacity=".5"/>
<circle cx="{left+18}" cy="363" r="4" fill="{G}" class="dot"/>
<text x="{left+30}" y="367">STATUS: SYNCED</text>
<text x="{left+230}" y="367">LAST SYNC: {today} UTC</text>
<text x="{left+520}" y="367">AUTO-UPDATE: DAILY 23:00 IST</text>
</g>
<rect x="0" y="-80" width="{W}" height="80" fill="url(#scan)"><animateTransform attributeName="transform" type="translate" values="0 0;0 {H+80}" dur="5s" repeatCount="indefinite"/></rect>
</g></svg>''')
    return "\n".join(o)


# ---------------------------------------------------------------- main
def main():
    today = dt.datetime.now(dt.timezone.utc).date()
    if "--mock" in sys.argv:
        random.seed(3)
        days = {str(today - dt.timedelta(days=i)): random.choice([0, 0, 1, 2, 3, 5, 8]) for i in range(400)}
        lc = {"solved": 770, "easy": 300, "medium": 400, "hard": 70, "rating": 1816}
        cf = {"rating": 1201, "max": 1250, "rank": "newbie"}
    else:
        cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
        days = fetch_github(today)                  # if this fails the job fails and the old SVG stays
        lc, cf = soft("lc", fetch_lc, cache), soft("cf", fetch_cf, cache)
        json.dump(cache, open(CACHE, "w"))
    open(OUT, "w").write(render(days, lc, cf, today))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
