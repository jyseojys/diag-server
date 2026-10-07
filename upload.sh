#!/bin/bash
git add .
git commit -m "Auto update: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main
echo "✅ 깃 서버 업로드 완료!"