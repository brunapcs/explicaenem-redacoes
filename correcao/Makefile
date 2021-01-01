g_project="explicaenem"

deploy: build
	gcloud config set project $(g_project) \
	&&gsutil mb gs://correcoes \
	&& gsutil cp function.zip gs://correcoes \
	&& gcloud functions deploy Correcoes-redacao \
	--region us-central1 \
	--runtime python37 \
	--entry-point main \
	--trigger-http \
	--source gs://correcoes/function.zip \
	--service-account redacao-on-demand@explicaenem.iam.gserviceaccount.com \
	--env-vars-file .env.yaml \
	&& gsutil rm -r gs://correcoes


build:
	rm function.zip
	zip -r -X function.zip . -r .

run-local: 
	python main.py -l 