# ChatGLM3 + Free Web Search (v13.0.0)

使用 [`free-web-search-ultimate`](https://github.com/wd041216-bit/free-web-search-ultimate) 为 ChatGLM3 提供零成本、无需 API Key 的实时网络搜索能力。

## 安装

```bash
pip install free-web-search-ultimate==13.0.0 transformers
```

## 使用示例

```python
from free_web_search_ultimate import UltimateSearcher

searcher = UltimateSearcher()  # 无需 API Key！

# 搜索网页
results = searcher.search("ChatGLM3 最新进展", engine="duckduckgo", max_results=5)
for r in results:
    print(f"标题: {r['title']}")
    print(f"链接: {r['url']}")
    print(f"摘要: {r['snippet'][:100]}...\n")

# 搜索新闻
news = searcher.search_news("人工智能最新动态", max_results=3)
```

## 支持的搜索引擎

- DuckDuckGo（默认）
- Bing
- Google
- Brave
- Yahoo

**PyPI:** https://pypi.org/project/free-web-search-ultimate/
**GitHub:** https://github.com/wd041216-bit/free-web-search-ultimate
