import os, time
from django.test import override_settings
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from posti.models import Post

def create_post():
    """
    Creates anonymous post
    :rtype : Post
    """
    data = {'title': 'Esto es un titulo', 'text': 'Esto es un texto de prueba'}
    post = Post.create_post(data['title'], data['text'])
    post.save()
    return post

class DetailViewTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        """ Quit selenium driver instance """
        cls.selenium.quit()
        super().tearDownClass()

    def test_page_welcome(self):
        url = reverse('posti:index')
        self.selenium.get(self.live_server_url + url)
        text = self.selenium.find_element_by_tag_name('legend').text
        self.assertEqual(text, 'Añade una nueva nota')

    def test_make_a_post(self):
        url = reverse('posti:index')
        data = {'title': 'Esto es un titulo', 'text': 'Esto es un texto de prueba'}
        self.selenium.get(self.live_server_url + url)
        title = self.selenium.find_element_by_name('title')
        title.send_keys(data['title'])
        self.selenium.switch_to.frame('id_text_iframe')
        text = self.selenium.find_element_by_class_name('note-editable.panel-body')
        text.send_keys(data['text'])
        self.selenium.switch_to.default_content()
        submit = 'button[type="submit"]'
        submit = self.selenium.find_element_by_css_selector(submit)
        submit.click()
        self.selenium.implicitly_wait(5)
        warning = '×\nPlease fill out all the fields'
        alert = self.selenium.find_element_by_css_selector('.alert').text
        self.assertEqual(warning, alert)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_reporting(self):
        p = create_post()
        url = reverse('posti:detail', args=(p.uuid,))
        self.selenium.get(self.live_server_url + url)
        self.selenium.find_element_by_class_name('report-link').click()
        self.selenium.implicitly_wait(15)
        alert = self.selenium.switch_to.alert
        alert.accept()
        self.selenium.implicitly_wait(5)
        response = self.selenium.find_element_by_class_name('report').find_element_by_tag_name('p').text
        self.assertEqual(response, 'El reporte se ha realizado exitosamente.')