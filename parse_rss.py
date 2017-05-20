#!/usr/bin/python

import feedparser
from argparse import ArgumentParser
from sqlalchemy import create_engine, func, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
session = None

class RssFeedItem(Base):
    __tablename__ = "rss_feed_items"
    
    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    title = Column(String(480))
    
    def update(self, session):
        session.commit()
                
    def __init__(self, title):
        self.title = title
                
    def __repr__(self):
        return "<RssFeedItem title=%s" % self.title
        
def _check_if_item_in_database(title):
    found_rss_feed_item = session.query(RssFeedItem).filter_by(title=title).first()
    
    if found_rss_feed_item is not None:
        return found_rss_feed_item
    else:
        return None
            
def parse_rss_feed(url):
    feed = feedparser.parse(url)
    
    for post in feed.entries:
        title = post.title
        
        if _check_if_item_in_database(title) is None:
            print "Title: {}".format(title)
            
            # Add to database
            new_rss_feed_item = RssFeedItem(title=title)
            session.add(new_rss_feed_item)
            session.commit()
        else:
            print "Title already in database: {}".format(title)
            
if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument("--url", help="RSS feed URL to parse", required=True)
    args = args.parse_args()
    
    database_name = "py_rss_feeds"
    
    # NOTE - creation will only happen if database file and tables don't exist
    engine = create_engine('sqlite:///%s.sqlite' % database_name, echo=False)    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    parse_rss_feed(args.url)