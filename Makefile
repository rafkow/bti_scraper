run:
	python BTI_Scraper.pyw

install: requirements.txt
	pip install -r requirements.txt

build: setup.py
	python setup.py build

clean:
	if [ -d "./build" ]; then rm -rf build; fi


