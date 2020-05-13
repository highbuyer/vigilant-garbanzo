{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "import scrapy\n",
    "\n",
    "class MofanSpider(scrapy.Spider):\n",
    "    name = \"mofan\"\n",
    "    start_urls = [\n",
    "        'https://morvanzhou.github.io/',\n",
    "    ]\n",
    "    # unseen = set()\n",
    "    # seen = set()      # 我们不在需要 set 了, 它自动去重\n",
    "    def parse(self, response):\n",
    "        yield {     # return some results\n",
    "            'title': response.css('h1::text').extract_first(default='Missing').strip().replace('\"', \"\"),\n",
    "            'url': response.url,\n",
    "        }\n",
    "\n",
    "        urls = response.css('a::attr(href)').re(r'^/.+?/$')     # find all sub urls\n",
    "        for url in urls:\n",
    "            yield response.follow(url, callback=self.parse)     # it will filter duplication automatically"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
