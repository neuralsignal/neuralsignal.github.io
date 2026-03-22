.PHONY: serve build clean local local-build

serve:
	docker-compose up

build:
	docker-compose run --rm jekyll bundle exec jekyll build

local:
	bundle exec jekyll serve --port 8080 --livereload

local-build:
	bundle exec jekyll build

clean:
	rm -rf _site .jekyll-cache .sass-cache
