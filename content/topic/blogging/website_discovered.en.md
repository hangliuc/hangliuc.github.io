---
categories:
- Blog
date: 2025-12-15 11:45:07
draft: false
title: Hugo | How to make a blog searchable by search engines
---

After deploying the blog, you need to ensure that search engines can index the blog.

## Google
### Obtain Measurement ID
[Google Analytics Official Website](https://analytics.google.com/analytics/web/provision/#/provision)
Each website in Google Analytics has a unique Measurement ID, formatted as `G-XXXXXXXXXX`. This ID is used to send website visit data to Google Analytics.

Add the following configuration to hugo.yaml:

If you are using YAML format, note that it should be the top-level configuration
```yaml
googleAnalytics: G-xxxx # <--- Replace with your Measurement ID
```

### Submit sitemap
A sitemap is an XML file that tells search engines which pages your website has.

Hugo automatically generates a sitemap.xml file in the root directory of the public folder during the generation and deployment of the website.

Log in to [Google Search Console](https://search.google.com/search-console). Select "Google Analytics" under the verification of ownership options and enter your Measurement ID to verify ownership.

Here is a screenshot of a successfully submitted sitemap
![Google Search Console verification of ownership](img/blog/google_search_console.png)

### How to verify if articles have been indexed by Google
For a new site, Google may take a few days to several weeks to index all pages.

#### Google Search Console Verification
Directly search in the top search box, enter your article link to verify if it has been indexed.
![Google Search Console verification of ownership](img/blog/gcs01.png)

You can also click "Request indexing" to request Google to index your article.

#### Google Search Verification
![Google Search Console verification of ownership](img/blog/gcs02.png)


tips:
- Verification of indexing may take a few days to several weeks to complete.
- Try to increase the keyword density in article titles to make them more attractive and encourage users to click.

## Baidu
- Log in to [Baidu Search Console](https://ziyuan.baidu.com/?castk=LTE%3D)
- Add the domain according to the requirements and use normal inclusion to push resources

![Baidu Search Console add domain](img/blog/baidu_search.png)
- When submitting the sitemap.xml file, a filing number is required, so it is not added here.
- There is a daily limit on the number of API submissions.


## refs
https://hyrtee.github.io/2023/start-blog/#refs