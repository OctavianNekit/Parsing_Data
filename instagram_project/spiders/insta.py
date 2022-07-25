import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instagram_project.items import InstagramProjectItem


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['http://www.instagram.com/']
    instagram_in = "https://www.instagram.com/accounts/login/ajax/"
    instagram_login = "***"
    instagram_password = "***"
    parse_user = "_chkhlv"
    followers_hash = '5aefa9893005572d237da5068082d8d5'
    follow_hash = '3dec7e2c57367ef3da3d987d89f9dbc8'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    def parse(self, response):
        token = self.get_token(response.text)
        yield scrapy.FormRequest(
            self.instagram_in,
            method="POST",
            callback=self.login,
            formdata={'username': self.instagram_login, 'enc_password': self.instagram_password},
            headers={"X-CSRFToken": token}
        )

    def login(self, response: HtmlResponse):
        body = response.json()
        if body.get("authenticated"):
            yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.get_user_id(response.text, username)
        variables = {'id': user_id, 'include_reel': True, 'fetch_mutual': False, 'first': 24}

        follow_url = f'{self.graphql_url}query_hash={self.follow_hash}&{urlencode(variables)}'
        yield response.follow(
            follow_url,
            callback=self.follow_parse,
            cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)})

        followers_url = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
        yield response.follow(
            followers_url,
            callback=self.followers_parse,
            cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)})

    def followers_parse(self, response: HtmlResponse, username, user_id, variables):
        json_data = response.json()
        page_info = json_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.followers_parse,
                cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)})
        followers = json_data.get('data').get('user').get('edge_followed_by').get('edges')
        for follower in followers:
            item = InstagramProjectItem(
                id_user=user_id,
                follow_id=follower.get('node').get('id'),
                group="follower",
                name=follower.get('node').get('username'),
                photo_url=follower.get('node').get('profile_pic_url')
            )
            yield item

    def follow_parse(self, response: HtmlResponse, username, user_id, variables):
        json_data = response.json()
        page_info = json_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info.get('end_cursor')
            url_following = f'{self.graphql_url}query_hash={self.follow_hash}&{urlencode(variables)}'
            yield response.follow(
                url_following,
                callback=self.follow_parse,
                cb_kwargs={'username': username, 'user_id': user_id, 'variables': deepcopy(variables)})
        following = json_data.get('data').get('user').get('edge_follow').get('edges')
        for follow in following:
            item = InstagramProjectItem(
                id_user=user_id,
                follow_id=follow.get('node').get('id'),
                group="following",
                name=follow.get('node').get('username'),
                photo_url=follow.get('node').get('profile_pic_url')
            )
            yield item

    def get_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        print()
        return json.loads(matched).get('id')

    def get_token(self, text):
        find = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return find.split(":").pop().replace(r'"', '')
