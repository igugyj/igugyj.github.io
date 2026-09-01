const fs = require('fs');
const path = require('path');

const config = JSON.parse(fs.readFileSync('./redirects.json', 'utf8'));
const outDir = './dist';

if (fs.existsSync(outDir)) {
  fs.rmSync(outDir, { recursive: true, force: true });
}
fs.mkdirSync(outDir, { recursive: true });

for (const [route, target] of Object.entries(config)) {
  let cleanRoute = route.replace(/^\/+/, '').replace(/\/+$/, '');
  const targetDir = path.join(outDir, cleanRoute);
  const targetFile = path.join(targetDir, 'index.html');

  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=${target}">
  <title>Redirecting...</title>
</head>
<body>
  <p>Redirecting to <a href="${target}">${target}</a></p>
</body>
</html>`;

  fs.mkdirSync(targetDir, { recursive: true });
  fs.writeFileSync(targetFile, html, 'utf8');
  console.log('Generated ' + targetFile + ' -> ' + target);
}

console.log('All redirects generated successfully.');