.PHONY: install serve build clean

install:
	mise exec -- bundle install

serve:
	mise exec -- bundle exec jekyll serve --port 8080 --livereload

build:
	mise exec -- bundle exec jekyll build

clean:
	rm -rf _site .jekyll-cache .sass-cache
