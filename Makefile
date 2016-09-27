help:
	@echo "  build_env    build python env                 "
	@echo "  run          run python server                "
	@echo "  clean        clean cache                      "
	@echo "  migrate      migrate all models               "
	@echo "  watch        compile from scss to css static  "
	@echo "  shell        shell work                       "

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.env' -exec rm -rf {} +
	rm -rf ./env

build_env:
	@virtualenv .env -p python3
	@.env/bin/pip3 install -r requirements.txt

run:
	@.env/bin/python3 ./manage.py runserver 127.0.0.1:8080
