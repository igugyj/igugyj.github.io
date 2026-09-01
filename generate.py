import json, os, shutil

config = json.load(open('./redirects.json', encoding='utf-8'))
out_dir = './dist'

if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.makedirs(out_dir, exist_ok=True)

html_template = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={target}">
  <title>Redirecting...</title>
</head>
<body>
  <p>Redirecting to <a href="{target}">{target}</a></p>
</body>
</html>'''

for route, target in config.items():
    clean = route.strip('/')
    target_dir = os.path.join(out_dir, clean)
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_template.format(target=target))
    print(f'Generated {target_dir}/index.html -> {target}')

print('All redirects generated successfully.')