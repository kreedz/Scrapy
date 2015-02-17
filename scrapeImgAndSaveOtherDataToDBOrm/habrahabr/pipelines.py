# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from sqlalchemy.orm import sessionmaker
from models import Habrahabr, HabrahabrComment, db_connect, create_tables, delete_from_model

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem


class HabrahabrPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)
        delete_from_model(Habrahabr, engine, self.Session)

    def process_item(self, item, spider):
        session = self.Session()
        habrahabr = Habrahabr(title=item['title'])
        comments_items = getattr(item, 'comments', [])
        try:
            session.add(habrahabr)
            for comment_item in comments_items:
                comment = HabrahabrComment(comment=comment_item['comment'], habrahabr=habrahabr)
                session.add(comment)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item


class MyImagesPipeline(ImagesPipeline):

    #Name download version
    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    #Name thumbnail version
    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_guid = thumb_id + response.url.split('/')[-1]
        return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)

    def get_media_requests(self, item, info):
        #yield Request(item['images']) # Adding meta. Dunno how to put it in one line :-)
        if 'image_urls' in item and item['image_urls']:
            for image in item['image_urls']:
                yield Request(image)

    #def item_completed(self, results, item, info):
        #image_paths = [x['path'] for ok, x in results if ok]
        #if not image_paths:
            #raise DropItem("Item contains no images")
        #item['image_paths'] = image_paths
        #return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('scraped_data_utf-8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
