---
layout: default
---

<div id="home">
  <h1>Project logs</h1>
  <ul class="posts">
    {% for post in site.categories.wiki %}
		<h2>{{ post.title }}</h2>
		<p class="meta">{{ post.date | date_to_string }}</p>
		<div class="post">
			{{ post.excerpt }}
			<a href="{{ site.baseurl }}{{ post.url }}">Read more...</a>
		</div>
    {% endfor %}
  </ul>
</div>