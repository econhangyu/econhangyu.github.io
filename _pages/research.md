---
permalink: /research/
title: "Research"
author_profile: true
---

I study how behavioral constraints and program delivery shape economic outcomes in poverty, using randomized field experiments in Sub-Saharan Africa. Recent work also examines how artificial intelligence is reshaping labor markets and hiring.

<p class="research-note">Click any entry below to expand a short description and related image.</p>

## Peer-Reviewed Journal Articles

{% assign pubs = site.publications | where: "category", "published" | sort: "year" | reverse %}
{% for post in pubs %}
  {% include publication-entry.html post=post %}
{% endfor %}

### Peer-Reviewed Journal Articles in Chinese

{% assign pubs_cn = site.publications | where: "category", "published_cn" | sort: "year" | reverse %}
{% for post in pubs_cn %}
  {% include publication-entry.html post=post %}
{% endfor %}

### Edited Volumes

{% assign volumes = site.publications | where: "category", "edited" | sort: "year" | reverse %}
{% for post in volumes %}
  {% include publication-entry.html post=post %}
{% endfor %}

## Working Papers

{% assign wps = site.publications | where: "category", "working" | sort: "year" | reverse %}
{% for post in wps %}
  {% include publication-entry.html post=post %}
{% endfor %}

## Works in Progress

{% assign wips = site.publications | where: "category", "wip" | sort: "sort_order" %}
{% for post in wips %}
  {% include publication-entry.html post=post %}
{% endfor %}

## Writing for General Audiences

{% assign popular = site.publications | where: "category", "popular" | sort: "year" | reverse %}
{% for post in popular %}
  {% include publication-entry.html post=post %}
{% endfor %}
