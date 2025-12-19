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
        new PagefindUI({ 
            element: "#search", 
            showSubResults: true,
            translations: {
                placeholder: "Search documents...",
                zero_results: "No results found for [SEARCH_TERM]",
                count_one: "Found 1 document",
                count_many: "Found [COUNT] documents",
            }
        });
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