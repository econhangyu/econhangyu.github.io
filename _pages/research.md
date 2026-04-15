---
permalink: /research/
title: "Research"
author_profile: true
---

I study how behavioral constraints and program delivery shape economic outcomes in poverty, using randomized field experiments in Sub-Saharan Africa. Recent work also examines how artificial intelligence is reshaping labor markets and hiring.

## Peer-Reviewed Journal Articles

<ol class="pub-list">
{% assign pubs = site.publications | where: "category", "published" | sort: "year" | reverse %}
{% for post in pubs %}{% include publication-entry.html post=post %}{% endfor %}
</ol>

### In Chinese

<ol class="pub-list pub-list-secondary">
{% assign pubs_cn = site.publications | where: "category", "published_cn" | sort: "year" | reverse %}
{% for post in pubs_cn %}{% include publication-entry.html post=post %}{% endfor %}
</ol>

### Edited Volumes

<ul class="pub-list pub-list-unnumbered">
{% assign volumes = site.publications | where: "category", "edited" | sort: "year" | reverse %}
{% for post in volumes %}{% include publication-entry.html post=post %}{% endfor %}
</ul>

## Working Papers

<ol class="pub-list">
{% assign wps = site.publications | where: "category", "working" | sort: "year" | reverse %}
{% for post in wps %}{% include publication-entry.html post=post %}{% endfor %}
</ol>

## Selected Works in Progress

<ol class="pub-list">
{% assign wips = site.publications | where: "category", "wip" | sort: "sort_order" %}
{% for post in wips %}{% include publication-entry.html post=post %}{% endfor %}
</ol>
