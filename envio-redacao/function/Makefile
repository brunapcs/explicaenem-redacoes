g_project="explicaenem"

deploy: build
	gcloud config set project $(g_project) \
	&& gsutil cp function.zip gs://redacao-function \
	&& gcloud functions deploy Consumer-redacao \
	--region us-central1 \
	--runtime python37 \
	--entry-point main \
	--trigger-http \
	--source gs://redacao-function/function.zip \
	--service-account redacao-on-demand@explicaenem.iam.gserviceaccount.com \
	--env-vars-file .env.yaml \
	&& gsutil rm -r gs://redacao-function



build:
	rm function.zip
	zip -r -X function.zip . -r .