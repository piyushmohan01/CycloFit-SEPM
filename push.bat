git add .
git status
set /p Input=---ENTER COMMIT MESSAGE---:
git commit -m "%Input%"
git pull origin main
git push origin main