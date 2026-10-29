import html, json, os, shutil

DELAY = 3  # seconds before auto-redirect
ASSET_SRC = './assets/loading.gif'
ASSET_NAME = os.path.basename(ASSET_SRC)
TEMPLATE_SRC = './template.html'

config = json.load(open('./redirects.json', encoding='utf-8'))
out_dir = './dist'

for path in (TEMPLATE_SRC, ASSET_SRC):
    if not os.path.isfile(path):
        raise SystemExit(f'Missing build input: {path}')
template = open(TEMPLATE_SRC, encoding='utf-8').read()

if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.makedirs(out_dir, exist_ok=True)

for route, target in config.items():
    clean = route.strip('/')
    target_dir = os.path.join(out_dir, clean)
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy(ASSET_SRC, target_dir)
    page = (template
            .replace('{{delay}}', str(DELAY))
            .replace('{{delay_ms}}', str(DELAY * 1000))
            .replace('{{asset}}', ASSET_NAME)
            .replace('{{target_html}}', html.escape(target, quote=True))
            .replace('{{target_js}}', json.dumps(target)))
    with open(os.path.join(target_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'Generated {target_dir}/index.html -> {target}')

print('All redirects generated successfully.')
