git add .
git status
set commit=%~1
git commit -m "%commit%"
git pull origin main
git push origin main