---
title: "搜索"
slug: "search"
layout: "search"
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
                placeholder: "搜索文档...",
                zero_results: "没有找到 [SEARCH_TERM]",
                count_one: "找到 1 篇",
                count_many: "找到 [COUNT] 篇",
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
