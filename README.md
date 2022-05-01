# microblog
Learning to build web applications with Flask!

Reference Book: *The New Flask Mega-Tutorial* by Miguel Grinberg



**For translation features**

- To add a new display language for users : `(venv) $ flask translate init <language-code>`
- To update all the languages after making changes to the `_()` and `_l()` language markers: `(venv) $ flask translate update`
- And to compile all languages after updating the translation files: `(venv) $ flask translate compile`

**For searching features**
- To initialize the index from database: run `>>> Post.reindex()` in flask shell



