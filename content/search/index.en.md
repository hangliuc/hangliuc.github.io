---
layout: search
slug: search
title: Search
---

<link href="/pagefind/pagefind-ui.css" rel="stylesheet">
<script src="/pagefind/pagefind-ui.js"></script>

<div id="search"></div>

<script>
    window.addEventListener('DOMContentLoaded', (event) => {
        const search = new PagefindUI({
            element: "#search", 
            showSubResults: true,
            translations: {
                placeholder: "Search documents...",
                zero_results: "No results found for [SEARCH_TERM]",
                count_one: "Found 1 document",
                count_many: "Found [COUNT] documents",
            }
        });

        const keyword = new URLSearchParams(window.location.search).get("keyword");
        if (keyword) search.triggerSearch(keyword);
    });
</script>

<style>
    #search {
        margin-top: 20px;
        min-height: 200px;
    }
    .pagefind-ui__result-title {
        font-weight: bold;
        color: var(--primary);
    }
</style>
