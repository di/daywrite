if [ ! -d "venv" ]; then
  virtualenv venv --distribute -p `which python2.7`
fi
source venv/bin/activate
pip install -q -r requirements.txt
foreman start
