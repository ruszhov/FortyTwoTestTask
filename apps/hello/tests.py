from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .views import hello, http_requests, edit_form
from .models import Contact, HttpRequestLog
from .forms import ContactForm
import datetime


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


class ContactFormTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = Client()
        self.admin.login(username='admin', password='admin')

        self._contact = {
            "first_name": "Ruslan",
            "last_name": "Zhovniriv",
            "date_of_birth": "1987-07-15",
            "bio": "Developer, Full Stack",
            "email": "ruszhov@gmail.com",
            "skype": "ruszhov",
            "jabber": "ruszhov@42.cc.co",
            "other_contacts": "https://www.linkedin.com/in/ruszhov/",
        }

    def test_form_url_view(self):
        """
        check url status code, test view
        """
        url = reverse('edit_form')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

        view = resolve('/edit_form/')
        self.assertEquals(view.func, edit_form)

    def test_validation_data(self):
        """
        check custom and required validations
        :return:
        """
        data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'date_of_birth': '1901-01-06',
            'jabber': 'sdhsjdhjdh---.@kk'
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'first_name': [u'This field is required.'],
            'last_name': [u'This field is required.'],
            'email': [u'This field is required.'],
            'date_of_birth': [u"Age can't be longer than 100 years!!!!"],
            'jabber': [u"This value can't be used as Jabber account"]
        })

    def test_form_saving(self):
        '''
        Checking save data with form
        '''
        form_url = reverse('edit_form')
        # log in to acscess page
        c = Client()
        c.login(username='admin', password='admin')
        r = c.get(form_url)
        data = r.context['form'].initial
        # generate new data
        new_data = self._contact.copy()
        # update some data
        data['first_name'] = new_data['first_name']
        data['last_name'] = new_data['last_name']
        data['date_of_birth'] = new_data['date_of_birth']
        data['bio'] = new_data['bio']
        data['email'] = new_data['email']
        data['skype'] = new_data['skype']
        data['jabber'] = new_data['jabber']
        data['other_contacts'] = new_data['other_contacts']
        data['photo'] = ''
        # post to the form
        r = c.post(form_url, data)
        self.assertEqual(r.status_code, 200)
        # retrieve from DB abd check if data was saved
        instance = Contact.objects.all()[0]
        self.assertEqual(instance.first_name, new_data['first_name'])
        self.assertEqual(instance.last_name, new_data['last_name'])
        self.assertEqual(instance.date_of_birth,
                         datetime.datetime.strptime(new_data['date_of_birth'],
                                                    '%Y-%m-%d').date())
        self.assertEqual(instance.bio, new_data['bio'])
        self.assertEqual(instance.email, new_data['email'])
        self.assertEqual(instance.jabber, new_data['jabber'])
        self.assertEqual(instance.skype, new_data['skype'])
        self.assertEqual(instance.other_contacts, new_data['other_contacts'])
