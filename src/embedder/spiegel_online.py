import spiegel_scraper as spon


class spiegel_api:

    def get_articles_of_date(self, date):
        archive_entries = spon.archive.by_date(date)
        all_archives = []
        for entry in archive_entries:
            article_url = entry['url']
            try:
                article = spon.article.by_url(article_url)
                all_archives.append(article)
            except Exception as ex:
                print("Skipped one article since an error occured")
                print(ex)
        return all_archives
