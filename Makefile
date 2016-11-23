help:
	@echo "  build_env    build python env                 "
	@echo "  run          run python server                "
	@echo "  run_schema   run python schema server         "


build_env:
	@virtualenv .env -p python3
	@.env/bin/pip3 install -r requirements.txt

run:

	@FLASK_DEBUG=1
	@FLASK_APP=app/main.py
	@.env/bin/flask run

run_schema:

	@FLASK_DEBUG=1
	@FLASK_APP=app/main_schema.py
	@.env/bin/flask run --port=5001
