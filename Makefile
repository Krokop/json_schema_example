help:
	@echo "  build_env    build python env                 "
	@echo "  run          run python server                "


build_env:
	@virtualenv .env -p python3
	@.env/bin/pip3 install -r requirements.txt

run:

	@export FLASK_DEBUG=1
	export FLASK_APP=app/main.py
	@.env/bin/flask run
