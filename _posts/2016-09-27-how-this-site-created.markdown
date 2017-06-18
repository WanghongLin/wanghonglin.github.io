---
layout: post
title:  "How this site created?"
date:   2016-09-27 08:35:17 +0800
categories: site
---

# How this sited created?

###### Note: Don't forget to replace all the following 'username' with your username

#### Create a github project name 'username.github.io'

#### Prepare jekyll and bundler
```shell
$ gem install jekyll bundler
```

#### Checkout the project 'username.github.io' you just created from github
```shell
$ git checkout https://github/username/username.github.io
```

#### Create boilerplate from jekyll
```shell
$ cd username.github.io
$ jekyll new . --force
# modify 'Gemfile' to use github pages
$ bundle install
```

#### Copy the remanning resources from minimal theme
```shell
$ bundle show minima
# you will see an absolute path of your minima theme's location
$ cp -rf /var/lib/gems/2.3.0/gems/minima-2.0.0/{assets,_includes,_layout,_sass} .
```

Then add following code to the top of your markdown file.

```
---
layout: post
title:  "How this site created?"
date:   2016-09-27 08:35:17 +0800
categories: jekyll update
---
```

If you are working in bash, you can use `$ date "+%F %T %z"` to generate date description.


#### Do testing in your local machine
```shell
$ bundle exec jekyll serve
```

#### Commit and push all your site content to origin
```shell
$ git add .
$ git commit -m 'just created github pages blog'
$ git push
```

#### Congratulations!

#### References
1. [Jekyll quick start guide](https://jekyllrb.com/docs/quickstart/)
2. [Github pages](https://pages.github.com/)
