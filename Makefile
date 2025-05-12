init: download_l100_3_data set_pythonpath

download_l100_3_data:
	@echo "Downloading latest 'Recensement de la DINUM des administrations au sens L100-3' dataset"
	@mkdir -p data
	@rm -rf data/*.csv
	@wget -O data/liste-administrations.csv https://www.data.gouv.fr/fr/datasets/r/c0f355f1-66bd-4f57-8a3c-2c6f3527b364
	@echo "Data downloaded."

set_pythonpath:
	@echo "Setting PYTHONPATH to include the current directory"
	@export PYTHONPATH=$(shell pwd):$$PYTHONPATH
	@echo "PYTHONPATH set to: $$PYTHONPATH"

test:
	@echo "Running tests"
	@pytest --maxfail=1 --disable-warnings
	@echo "Tests completed."

.PHONY: init download_l100_3_data set_pythonpath test