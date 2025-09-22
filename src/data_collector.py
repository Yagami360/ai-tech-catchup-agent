"""
データ収集モジュール - RSSフィード、Webサイトからの情報収集
"""
import logging
from datetime import datetime
from typing import Any, Dict, List

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Article:
    """記事データクラス"""

    def __init__(
        self,
        title: str,
        url: str,
        content: str = "",
        published_date: datetime = None,
        source: str = "",
    ):
        self.title = title
        self.url = url
        self.content = content
        self.published_date = published_date or datetime.now()
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "published_date": self.published_date.isoformat(),
            "source": self.source,
        }


class DataCollector:
    """データ収集クラス"""

    def __init__(self, rss_feeds: List[str]):
        self.rss_feeds = rss_feeds
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "AI-Tech-Catchup-Agent/1.0"})

    def collect_rss_articles(self) -> List[Article]:
        """RSSフィードから記事を収集"""
        articles = []

        for feed_url in self.rss_feeds:
            try:
                logger.info(f"RSSフィードを取得中: {feed_url}")
                feed = feedparser.parse(feed_url)

                for entry in feed.entries[:5]:  # 最新5件
                    article = Article(
                        title=entry.get("title", ""),
                        url=entry.get("link", ""),
                        published_date=self._parse_date(entry.get("published", "")),
                        source=feed.feed.get("title", feed_url),
                    )

                    # 記事の詳細内容を取得
                    article.content = self._extract_article_content(article.url)
                    articles.append(article)

            except Exception as e:
                logger.error(f"RSSフィードの取得に失敗: {feed_url}, エラー: {e}")

        return articles

    def _parse_date(self, date_str: str) -> datetime:
        """日付文字列をパース"""
        try:
            from dateutil import parser

            return parser.parse(date_str)
        except:
            return datetime.now()

    def _extract_article_content(self, url: str) -> str:
        """記事の詳細内容を抽出"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # 不要な要素を削除
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()

            # メインコンテンツを抽出
            content_selectors = [
                "article",
                ".post-content",
                ".entry-content",
                ".content",
                "main",
                'div[class*="content"]',
            ]

            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = " ".join([elem.get_text(strip=True) for elem in elements])
                    break

            if not content:
                # フォールバック: body全体からテキストを抽出
                content = soup.get_text(strip=True)

            # 長すぎる場合は切り詰め
            if len(content) > 5000:
                content = content[:5000] + "..."

            return content

        except Exception as e:
            logger.error(f"記事内容の抽出に失敗: {url}, エラー: {e}")
            return ""

    def search_articles_by_keywords(self, keywords: List[str]) -> List[Article]:
        """キーワード検索による記事収集（将来的にAPI実装）"""
        # 現在はRSSフィードからの収集のみ実装
        # 将来的にはGoogle News APIやその他の検索APIを統合
        articles = self.collect_rss_articles()

        # キーワードでフィルタリング
        filtered_articles = []
        for article in articles:
            content_lower = (article.title + " " + article.content).lower()
            if any(keyword.lower() in content_lower for keyword in keywords):
                filtered_articles.append(article)

        return filtered_articles
