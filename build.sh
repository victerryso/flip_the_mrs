USER="victerryso"
REPO="reauth_test"

rm -rf _build/
make html

# Development
# open _build/html/index.html

# Production
cd _build/html
touch .nojekyll
git init
git add .
git commit -m 'asdf'
git remote add origin https://github.com/${USER}/${REPO}.git
git checkout -b gh-pages
git push --force origin gh-pages
open http://${USER}.github.io/${REPO}
