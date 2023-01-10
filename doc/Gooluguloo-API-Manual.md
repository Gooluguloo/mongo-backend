# Gooluguloo API Manual

**GET search()**

The search endpoint.

```js
http://localhost:5000/search/<query>
```

The `query` parameter may contain 3 parts, `query string`, `start index`, and `count`.

`query string` is what the user types in. Replace all spaces in the string with `%WANG`.

`start index` is the index of the first item of the results list.

`count` indicates how many items to get.

The three parameters should be parsed into a single string called `query` upon request. Use `%SPL` to separate them.

For example, say the user enters `family guy`, the `start index` is 30, and `count` is 10. The final query should look like this:

```js
family%WANGguy%SPL30%SPL10
```

<br>

**GET crawl()**

Crawls a single url.

```js
http://localhost:5000/crawl/<url>
```

This method takes a single parameter `url`, which represents to URL of a webpage. The system will then automatically crawls and index this webpage into the database.


<br>

**GET crawl_next()**

Crawls the first item in the pending list.

```js
http://localhost:5000/crawl-next
```

This method does not take any parameters. It will automatically retrieve and crawl the first item in the pending list.

If the pending list is empty, the system will crawl one of the top 500 websites instead.


<br>

**GET list_webpages()**

List all the crawled and indexed webpages.

```js
http://localhost:5000/webpages
```


<br>

**GET list_keywords()**

List all the indexed keywords.

```js
http://localhost:5000/keywords
```


<br>

**GET list_pending_crawls()**

List all the items in the pending list.

```js
http://localhost:5000/pending
```