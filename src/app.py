from flask import Flask, Response
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

def load_and_bump_counter():
    """
    Read the current counter from counter.txt,
    add 1, write it back, return the new value.
    If counter.txt doesn't exist or is broken, start at 1.
    """
    try:
        with open(COUNTER_FILE, "r") as f:
            raw = f.read().strip()
            current = int(raw)
    except:
        current = 0  # safe fallback if file missing/bad

    current += 1  # NOW SERVING next number

    try:
        with open(COUNTER_FILE, "w") as f:
            f.write(str(current))
    except:
        # if we fail to write, we still serve current
        pass

    return current


def build_page_html(serving_number: int) -> str:
    """
    Build the full HTML page with the live counter number inserted.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>TimmyTime</title>

<style>
    :root {{
        --bg-start: rgba(10,10,20,1);
        --bg-end: rgba(0,0,0,1);
        --text-main: #ffffff;
        --text-glow: #ff8cff;
        --panel-bg: rgba(0,0,0,0.25);
        --panel-border: rgba(255,255,255,0.15);
    }}

    * {{
        box-sizing:border-box;
        margin:0;
        padding:0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", Roboto, sans-serif;
    }}

    body {{
        min-height:100vh;
        background:
            radial-gradient(circle at 20% 20%, rgba(255,0,204,0.18) 0%, rgba(0,0,0,0) 60%),
            radial-gradient(circle at 80% 30%, rgba(255,140,0,0.12) 0%, rgba(0,0,0,0) 60%),
            radial-gradient(circle at 50% 80%, rgba(140,0,255,0.18) 0%, rgba(0,0,0,0) 60%),
            linear-gradient(to bottom, var(--bg-start) 0%, var(--bg-end) 80%);
        color: var(--text-main);
        overflow:hidden;
        position:relative;
    }}

    /* ==================== BUBBLES ==================== */

    .bubble {{
        position:absolute;
        border-radius:50%;
        background: radial-gradient(circle at 30% 30%,
            rgba(255,255,255,0.9) 0%,
            rgba(255,0,204,0.2) 40%,
            rgba(0,0,0,0) 70%);
        box-shadow:
            0 0 20px rgba(255,0,204,0.6),
            0 0 50px rgba(255,140,0,0.4),
            0 0 80px rgba(140,0,255,0.4);
        opacity:0.8;
        animation: floatUp linear forwards;
        will-change: transform, opacity;
    }}

    @keyframes floatUp {{
        0%   {{ transform: translateY(0) scale(1);    opacity:0;   }}
        10%  {{ opacity:0.9; }}
        80%  {{ opacity:0.9; }}
        100% {{ transform: translateY(-110vh) scale(1.05); opacity:0.4; }}
    }}

    /* pop animation at the end */
    .pop {{
        animation: popBurst 0.18s forwards;
        box-shadow:
            0 0 30px rgba(255,255,255,0.9),
            0 0 60px rgba(255,0,204,0.8),
            0 0 90px rgba(255,140,0,0.8),
            0 0 120px rgba(140,0,255,0.8);
        background: radial-gradient(circle at 50% 50%,
            rgba(255,255,255,1) 0%,
            rgba(255,255,255,0) 70%);
    }}

    @keyframes popBurst {{
        0%   {{ transform: scale(1);   opacity:1;   }}
        50%  {{ transform: scale(1.4); opacity:1;   }}
        100% {{ transform: scale(0.2); opacity:0;   }}
    }}

    /* ==================== PANEL ==================== */

    .panel {{
        position:relative;
        width:90%;
        max-width:500px;
        margin:2rem auto;
        background: var(--panel-bg);
        border:1px solid var(--panel-border);
        border-radius:16px;
        padding:1rem 1rem 1.25rem;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow:
            0 20px 60px rgba(0,0,0,0.8),
            0 0 80px rgba(255,0,204,0.2);
        text-align:center;
    }}

    .title-row {{
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:0.4rem;
        margin-bottom:1rem;
    }}

    .brand {{
        font-size:1.25rem;
        font-weight:600;
        color: var(--text-main);
        text-shadow:
            0 0 8px rgba(255,0,204,0.7),
            0 0 20px rgba(255,140,0,0.4);
        letter-spacing:-0.03em;
    }}

    .now-serving-label {{
        font-size:0.8rem;
        font-weight:500;
        color: var(--text-glow);
        text-shadow:
            0 0 6px rgba(255,0,204,0.8),
            0 0 16px rgba(255,140,0,0.6),
            0 0 32px rgba(140,0,255,0.6);
        letter-spacing:0.08em;
        text-transform:uppercase;
    }}

    .counter-box {{
        font-size:2rem;
        font-weight:700;
        line-height:1;
        color:#fff;
        text-shadow:
            0 0 10px rgba(255,0,204,0.9),
            0 0 24px rgba(255,140,0,0.7),
            0 0 40px rgba(140,0,255,0.7);
        padding:0.6rem 1rem;
        border-radius:12px;
        border:1px solid rgba(255,255,255,0.25);
        background:rgba(0,0,0,0.35);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        min-width:220px;
        margin:0 auto 0.75rem;
    }}

    .note {{
        font-size:0.7rem;
        font-weight:400;
        line-height:1.4;
        color:rgba(255,255,255,0.8);
        text-shadow:0 0 8px rgba(0,0,0,0.8);
        max-width:90%;
        margin:0 auto 1rem;
    }}

    .note strong {{
        color:#fff;
        font-weight:600;
    }}

    .btn-list {{
        display:flex;
        flex-direction:column;
        gap:0.6rem;
        width:100%;
        max-width:400px;
        margin:0 auto;
    }}

    .music-btn {{
        display:block;
        width:100%;
        background:rgba(0,0,0,0.5);
        border:1px solid rgba(255,255,255,0.2);
        border-radius:12px;
        padding:0.8rem 1rem;
        text-align:center;
        color:#fff;
        font-size:0.9rem;
        font-weight:500;
        text-decoration:none;
        line-height:1.3;
        box-shadow:
            0 20px 40px rgba(0,0,0,0.9),
            0 0 30px rgba(255,0,204,0.4);
    }}

    .music-btn span {{
        display:block;
        font-size:0.7rem;
        font-weight:400;
        color:rgba(255,255,255,0.7);
    }}
</style>
</head>
<body>

<div class="panel">
    <div class="title-row">
        <div class="brand">TimmyTime</div>
        <div class="now-serving-label">NOW SERVING</div>
    </div>

    <div class="counter-box">{serving_number:,}</div>

    <div class="note">
        Every first punch counts toward 999,999.<br/>
        App made on iPhone 17 Pro Max.<br/>
        Reduction to Suno AI for playlist.
    </div>

    <div class="btn-list">
        <a class="music-btn" href="https://suno.com/playlist/2ec04889-1c23-4e2d-9c27-8a2b6475da4b" target="_blank" rel="noopener noreferrer">
            Timmy Bubbles • Playlist 1
            <span>Smooth / vibe / late night</span>
        </a>
        <a class="music-btn" href="https://suno.com/playlist/e95ddd12-7e37-43e2-b3e0-fe342085a19f" target="_blank" rel="noopener noreferrer">
            Timmy Bubbles • Playlist 2
            <span>Neon lounge feels</span>
        </a>
        <a class="music-btn" href="https://suno.com/playlist/01b65a04-d231-4574-bbb6-713997ca5b44" target="_blank" rel="noopener noreferrer">
            Timmy Bubbles • Playlist 3
            <span>Energy / hype / gym mirror flex</span>
        </a>
        <a class="music-btn" href="https://suno.com/playlist/457d7e00-938e-4bf0-bd59-f070729200df" target="_blank" rel="noopener noreferrer">
            Timmy Bubbles • Playlist 4
            <span>Afterparty drift</span>
        </a>
        <a class="music-btn" href="https://suno.com/playlist/08492edd-e0ba-4aea-a3f8-bb92220b28f2" target="_blank" rel="noopener noreferrer">
            Timmy Bubbles • Playlist 5
            <span>Slow kiss + trouble 🥀</span>
        </a>
    </div>
</div>

<script>
    // ==================== BUBBLE LOGIC WITH POP ====================

    const BUBBLE_COLORS = [
        'radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9) 0%, rgba(255,0,204,0.2) 40%, rgba(0,0,0,0) 70%)',
        'radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9) 0%, rgba(255,140,0,0.2) 40%, rgba(0,0,0,0) 70%)',
        'radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9) 0%, rgba(140,0,255,0.25) 40%, rgba(0,0,0,0) 70%)'
    ];

    function makeBubble() {{
        const b = document.createElement('div');
        b.className = 'bubble';

        // randomize visuals
        const size = 20 + Math.random()*80;      // 20px - 100px
        const left = Math.random()*100;          // vw
        const duration = 8 + Math.random()*10;   // 8s - 18s
        const delay = -Math.random()*duration;   // start mid-flight sometimes

        b.style.width = size + 'px';
        b.style.height = size + 'px';
        b.style.left = left + 'vw';
        b.style.bottom = '-120px';
        b.style.background = BUBBLE_COLORS[Math.floor(Math.random()*BUBBLE_COLORS.length)];
        b.style.animationDuration = duration + 's';
        b.style.animationDelay = delay + 's';

        // when floatUp finishes, do a "pop" then remove
        b.addEventListener('animationend', () => {{
            // ~50% of bubbles pop, ~50% just vanish quietly
            if (Math.random() < 0.5) {{
                b.classList.add('pop');
                b.addEventListener('animationend', () => {{
                    b.remove();
                }}, {{ once: true }});
            }} else {{
                b.remove();
            }}
        }}, {{ once: true }});

        document.body.appendChild(b);
    }}

    // fill screen with starter bubbles
    for (let i = 0; i < 30; i++) {{
        makeBubble();
    }}

    // keep generating over time
    setInterval(() => {{
        makeBubble();
    }}, 2000);
</script>

</body>
</html>"""


@app.route("/", methods=["GET"])
def home():
    # bump counter and build page using that number
    current_value = load_and_bump_counter()
    html = build_page_html(current_value)
    return Response(html, mimetype="text/html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
