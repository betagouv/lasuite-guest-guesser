init: download_l100_3_data

download_l100_3_data:
	@echo "Downloading latest 'Recensement de la DINUM des administrations au sens L100-3' dataset"
	@mkdir -p data
	@rm -rf data/*.csv
	@wget -O data/liste-administrations.csv https://www.data.gouv.fr/fr/datasets/r/c0f355f1-66bd-4f57-8a3c-2c6f3527b364
	@echo "Data downloaded."

test:
	@echo "Running tests"
	@pytest --maxfail=1 --disable-warnings
	@echo "Tests completed."

.PHONY: init download_l100_3_data test
export PYTHONPATH=.