import os
from flask import Flask, jsonify, Response
from threading import Lock

app = Flask(__name__)

# ─────────────────────────────
# VISITOR COUNTER (in-memory)
# ─────────────────────────────
visitor_count = 0
lock = Lock()

def increment_counter():
    global visitor_count
    with lock:
        visitor_count += 1
        return visitor_count

# ─────────────────────────────
# HOME PAGE
# ─────────────────────────────
@app.route("/", methods=["GET"])
def home():
    current_count = increment_counter()

    # full HTML with bubbles, glass card, playlists, etc.
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>TimmyTime</title>
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    min-height: 100vh;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", sans-serif;

    /* deep space purple base so the pink/orange pops */
    background: radial-gradient(circle at 20% 20%, #2b003b 0%, #0a001a 70%);
    color: #fff;
    overflow-x: hidden;
    overflow-y: auto;
    position: relative;
  }}

  /* BUBBLE LAYER GOES BEHIND CONTENT */
  #bubble-layer {{
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
  }}

  /* each animated bubble */
  .bubble {{
    position: absolute;
    width: var(--size);
    height: var(--size);
    left: var(--x);
    top: var(--y);
    border-radius: 50%;
    background: radial-gradient(circle at 40% 40%,
      rgba(255,0,255,0.85) 0%,
      rgba(255,0,140,0.6) 40%,
      rgba(255,140,0,0.5) 70%,
      rgba(0,0,0,0) 75%
    );
    filter: blur(20px);
    animation: floatUp var(--duration) linear infinite;
  }}

  /* rise + fade animation */
  @keyframes floatUp {{
    0% {{
      transform: translateY(0) scale(1);
      opacity: 1;
    }}
    100% {{
      transform: translateY(-200px) scale(1.1);
      opacity: 0;
    }}
  }}

  /* CONTENT WRAPPER ABOVE THE BUBBLES */
  .content {{
    position: relative;
    z-index: 2; /* KEEP ABOVE BUBBLES */
    padding: 16px;
    max-width: 100%;
    color: #fff;
    line-height: 1.25;
    font-weight: 600;
  }}

  /* glass card with neon */
  .glass-wrap {{
    width: calc(100% - 32px);
    max-width: 730px;

    /* layered glow: purple/pink/orange */
    background:
      radial-gradient(circle at 20% 20%, rgba(255,0,255,0.15) 0%, rgba(255,128,0,0.07) 60%, rgba(0,0,0,0) 100%),
      rgba(0,0,0,0.28);

    -webkit-backdrop-filter: blur(12px);
    backdrop-filter: blur(12px);

    border-radius: 20px;
    padding: 20px 24px 24px;

    box-shadow:
      0 30px 80px rgba(255,0,255,0.25),
      0 0 160px rgba(255,128,0,0.4) inset;
    border: 1px solid rgba(255,0,255,0.25);

    color: #fff;
    text-shadow:
      0 0 12px rgba(255,0,255,0.8),
      0 0 24px rgba(255,128,0,0.5);
  }}

  .top-col {{
    display: flex;
    flex-direction: column;
    row-gap: 16px;
  }}

  .app-name {{
    font-size: 2rem;
    font-weight: 800;
    color: #fff;
    line-height: 1.1;
  }}

  .visitors {{
    font-size: 1.6rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.2;
  }}

  /* playlists grid row */
  .playlist-grid {{
    display: grid;
    grid-template-columns: repeat(3,minmax(min-content,1fr));
    grid-row-gap: 12px;
    grid-column-gap: 24px;
    max-width: 100%;
    font-size: 1.4rem;
    font-weight: 700;
    line-height: 1.15;
  }}

  .playlist-grid a {{
    color: #9bb5ff;
    text-decoration: underline;
    text-shadow:
      0 0 10px rgba(155,181,255,0.8),
      0 0 30px rgba(255,0,255,0.4);
  }}

  /* track section */
  .tracks {{
    display: flex;
    flex-direction: column;
    row-gap: 16px;
    color: #fff;
  }}

  .track-title {{
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.1;
    text-shadow:
      0 0 12px rgba(255,0,255,0.8),
      0 0 24px rgba(255,128,0,0.5);
  }}

  .feature-link {{
    font-size: 1.6rem;
    font-weight: 700;
    text-decoration: underline;
    color: #9bb5ff;
    text-shadow:
      0 0 10px rgba(155,181,255,0.8),
      0 0 30px rgba(255,0,255,0.4);
  }}

  .tagline {{
    font-size: 1.6rem;
    font-weight: 700;
    color: rgba(255,255,255,0.9);
    text-shadow:
      0 0 8px rgba(255,0,255,0.6),
      0 0 16px rgba(255,128,0,0.4);
    line-height: 1.3;
  }}

  /* make sure page scrolls so bubbles can sit under */
  .spacer {{
    height: 120vh;
  }}

  a {{
    -webkit-tap-highlight-color: rgba(255,255,255,0.2);
  }}
</style>
</head>
<body>

<!-- FLOATING NEON BACKGROUND -->
<div id="bubble-layer"></div>

<!-- FOREGROUND CARD -->
<div class="content">
  <div class="glass-wrap">
    <div class="top-col">

      <div class="app-name">TimmyTime</div>

      <!-- live visitor count from Flask -->
      <div class="visitors">Visitors: <span id="visitorCount">{current_count}</span></div>

      <!-- playlists + feature links -->
      <div class="playlist-grid">
        <a href="https://suno.com/playlist/2ec04889-1c23-4e2d-9c27-8a2b6475da4b" target="_blank" rel="noopener noreferrer">
          Playlist 1
        </a>
        <a href="https://suno.com/playlist/e95ddd12-7e37-43e2-b3e0-fe342085a19f" target="_blank" rel="noopener noreferrer">
          Playlist 2
        </a>
        <a href="https://suno.com/playlist/01b65a04-d231-4574-bbb6-713997ca5b44" target="_blank" rel="noopener noreferrer">
          Playlist 3
        </a>
        <a href="https://suno.com/playlist/457d7e00-938e-4bf0-bd59-f070729200df" target="_blank" rel="noopener noreferrer">
          Playlist 4
        </a>
        <a href="https://suno.com/playlist/08492edd-e0ba-4aea-a3f8-bb92220b28f2" target="_blank" rel="noopener noreferrer">
          Playlist 5
        </a>
        <a href="https://suno.com/song/c0943681-4a5f-48f0-9e18-5c8bf5b24e8d" target="_blank" rel="noopener noreferrer">
          Feature Track
        </a>
      </div>

      <div class="tracks">
        <div class="track-title">Single Track</div>
        <a class="feature-link"
           href="https://suno.com/song/c0943681-4a5f-48f0-9e18-5c8bf5b24e8d"
           target="_blank"
           rel="noopener noreferrer">
          Feature Track
        </a>
      </div>

      <div class="tagline">
        App made by iPhone 17 Pro Max • Timmy Bubbles
      </div>

    </div>
  </div>
</div>

<div class="spacer"></div>

<script>
/*
  Bubble generator:
  builds ~40 glowing pink/purple/orange orbs,
  positions them around the viewport,
  and animates them floating upward + fading.
*/
(function makeBubbles() {{
  const layer = document.getElementById('bubble-layer');
  const BUBBLE_COUNT = 40;

  function randPct() {{
    return (Math.random() * 100) + '%';
  }}

  function rand(min, max) {{
    return min + Math.random() * (max - min);
  }}

  for (let i = 0; i < BUBBLE_COUNT; i++) {{
    const b = document.createElement('div');
    b.className = 'bubble';

    const size = rand(70, 220);      // tuned smaller so it's orbs not full fog
    const duration = rand(6, 14);    // rise speed

    b.style.setProperty('--size', size + 'px');
    b.style.setProperty('--x', randPct());
    b.style.setProperty('--y', randPct());
    b.style.setProperty('--duration', duration + 's');

    layer.appendChild(b);
  }}
}})();

/*
  OPTIONAL live refresh from /count.
  This lets the counter update without reload.
  Safe if /count 200s JSON like {{ "count": 7 }}.
*/
(function syncCount() {{
  fetch('/count')
    .then(r => r.json())
    .then(data => {{
      const el = document.getElementById('visitorCount');
      if (el && data && typeof data.count !== 'undefined') {{
        el.textContent = data.count;
      }}
    }})
    .catch(() => {{
      // silent fail, keeps page clean
    }});
}})();
</script>

</body>
</html>"""
    return Response(html, mimetype="text/html")


# ─────────────────────────────
# PUBLIC COUNT ENDPOINT
# ─────────────────────────────
@app.route("/count", methods=["GET"])
def get_count():
    # don't increment here, just report
    with lock:
        return jsonify({"count": visitor_count})


# ─────────────────────────────
# MAIN ENTRY
# ─────────────────────────────
if __name__ == "__main__":
    # Render injects PORT. Local fallback 10000 for testing.
    port = int(os.environ.get("PORT", 10000))

    # CRITICAL FOR RENDER:
    # listen on 0.0.0.0 and that port.
    # NO GUNICORN. NO PROCFILE. JUST PYTHON.
    app.run(host="0.0.0.0", port=port)
