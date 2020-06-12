from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from .views import hello, http_requests
from .models import Contact, HttpRequestLog
import datetime
from django.test import Client


class InitialDataTest(TestCase):
    def test_adminuser(self):
        """
        check if initial superuser exists and has default credentials
        """
        default_creds = 'admin:admin'
        username, password = default_creds.split(':')
        u = User.objects.get(pk=1)
        self.assertEqual(u.is_superuser, True)
        self.assertEqual(u.username == username, True)
        self.assertEqual(u.check_password(password), True)

    def test_model(self):
        '''
        check if initial contact data exist
        '''
        c = Contact.objects.get(pk=1)
        self.assertEqual(c.pk, 1)


class HomeTests(TestCase):
    fixtures = ['fixtures/initial_data.json']

    def test_hello_view_status_code(self):
        """
        check status code
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_hello_url_resolves_home_view(self):
        """
        check url resolving
        """
        view = resolve('/')
        self.assertEquals(view.func, hello)


class ContactModelTest(TestCase):

    def setUpTestData(cls):
        Contact.objects.create(
            id=1,
            first_name='Ruslan',
            last_name='Zhovniriv',
            date_of_birth='1987-07-15',
            bio='Developer, Full Stack developper',
            email='ruszhov@gmail.com',
            skype='ruszhov',
            jabber='ruszhov@42.cc.co'
        )

    def test_first_name_label(self):
        """
        check if the first name has label
        """
        contact = Contact.objects.get(pk=1)
        field_label = contact._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'First Name')

    def test_last_name_label(self):
        """
        check if the last name has label
        """
        contact = Contact.objects.get(pk=1)
        field_label = contact._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'Last Name')

    def test_date_of_birth_label(self):
        """
        check if the date of birth has label
        """
        contact = Contact.objects.get(pk=1)
        field_label = contact._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'Date of birth')

    def test_first_name_max_length(self):
        """
        check max length of first name
        """
        contact = Contact.objects.get(pk=1)
        max_length = contact._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        """
        check max length of last name
        """
        contact = Contact.objects.get(pk=1)
        max_length = contact._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)

    def test_bio_max_length(self):
        """
        check max length of bio
        """
        contact = Contact.objects.get(pk=1)
        max_length = contact._meta.get_field('bio').max_length
        self.assertEquals(max_length, 200)

    def test_skype_max_length(self):
        """
        check max length of skype
        """
        contact = Contact.objects.get(pk=1)
        max_length = contact._meta.get_field('skype').max_length
        self.assertEquals(max_length, 50)


class TestPage(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        """
        checking index page, template, context
        """
        contact = Contact.objects.get(pk=1)
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/index.html')
        self.assertEqual(response.context['contact'], contact)
        self.assertContains(response, 'ruszhov@42.cc.co')


class HomeRequestsTests(TestCase):

    def test_requests_status_code(self):
        """
        check status code
        """
        url = reverse('http_requests')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_requests_url_resolve(self):
        """
        check url equals
        """
        url = reverse('http_requests')
        self.assertEqual(url, '/http_requests/')

    def test_requests_url_resolves_view(self):
        """
        check url resolving
        """
        view = resolve('/http_requests/')
        self.assertEquals(view.func, http_requests)


class HttpLoggingRequestMiddlewareTest(TestCase):

    def setUp(cls):
        HttpRequestLog.objects.create(
            id=1,
            date=datetime.datetime.now(),
            request_method='GET',
            url='/http_requests/',
            server_protocol='HTTP/1.1'
        )

    def test_url_request_method(self):
        """
        checking request method
        :return:
        """

        url = reverse('http_requests')
        entry = HttpRequestLog.objects.get(id=1)
        self.assertEquals(url, '/http_requests/')
        self.assertEquals(entry.request_method, 'GET')

    def test_create_entries(self):
        '''
        create 10 entries, check if items are created (getting latest id),
        check if returns 10 items
        create 5 more, check if items are created (getting latest id),
        check if returns 10 newest
        :return:
        '''

        def create_record(id):
            HttpRequestLog.objects.create(
                id=id,
                date=datetime.datetime.now(),
                request_method='GET',
                url='/http_requests/',
                server_protocol='HTTP/1.1'
            )
        for i in range(2, 12):
            create_record(i)

        url = reverse('http_requests')
        # makes one more item itself
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/requests.html')

        items = HttpRequestLog.objects.all().order_by('-date')[:10]
        count_items = items.count()
        latest_pk_after_create_records = HttpRequestLog.objects.latest('id')

        self.assertEquals(count_items, 10)
        self.assertEquals(latest_pk_after_create_records.id, 12)
        self.assertEqual((response.context['requests']).count(), items.count())

        # create 5 new items
        for i in range(13, 18):
            create_record(i)

        more_items = HttpRequestLog.objects.all().order_by('-date')[:10]
        latest_pk_after_adding_five_more_records = \
            HttpRequestLog.objects.latest('id')
        self.assertEquals(latest_pk_after_adding_five_more_records.id,
                          latest_pk_after_create_records.id + 5)
        self.assertEqual((response.context['requests']).count(),
                         more_items.count())
