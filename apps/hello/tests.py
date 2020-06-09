from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.template import Template, Context
from .views import hello, http_requests
from .models import Contact, HttpRequestLog, ModelActionLog
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
        # self.assertEquals(entry, None)
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

    def test_auth_redirect(self):
        """
        check status code
        """
        response = self.client.get(reverse('edit-form'))
        self.failUnlessEqual(response.status_code, 302)

    def test_form(self):
        """
        check form validation
        :return:
        """
        form_data = self._contact.copy()
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        """
        check if field are required
        :return:
        """
        entry = Contact.objects.get(pk=1)
        form = ContactForm({}, instance=entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'first_name': [u'This field is required.'],
            'last_name': [u'This field is required.'],
            'email': [u'This field is required.']
        })


class TemplateTagsTestCase(TestCase):

    def setUp(self):
        self.contact = Contact.objects.get(pk=1)
        self.template = Template(
            '{% load edit_object %}{% edit_link contact %}')

    def test_edit_link_templatetag(self):
        '''
        checking admin edit url
        :return:
        '''
        edit_link = self.template.render(Context(dict(contact=self.contact)))
        self.assertEqual('/admin/hello/contact/1/', edit_link)


class AuditLoggerTest(TestCase):
    def setUp(self):
        self._log_entry = {
            "model_name": "User",
            "instance": "admin",
            "action": "update",
            "created": datetime.datetime.now()
        }

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

    def test_max_length(self):
        """
        check max length of ModelActionLog's fields
        """
        logentry = ModelActionLog.objects.first()
        max_length_model_name = logentry._meta.get_field('model_name')\
            .max_length
        max_length_instance = logentry._meta.get_field('instance').max_length
        max_length_action = logentry._meta.get_field('action').max_length
        self.assertEquals(max_length_model_name, 64)
        self.assertEquals(max_length_instance, 64)
        self.assertEquals(max_length_action, 16)

    def test_object_create(self):
        '''
        Checking post_save signal, 'create' action
        :return:
        '''
        count = ModelActionLog.objects.count()
        contact = Contact.objects.create(**self._contact)
        new_count = ModelActionLog.objects.count()
        self.assertEqual(count + 1, new_count)

        log_entry = ModelActionLog.objects.latest('created')
        self.assertNotEquals(log_entry, None)
        self.assertEquals(log_entry.model_name, contact._meta.object_name)
        self.assertEquals(log_entry.instance, unicode(contact))
        self.assertEquals(log_entry.action, unicode('create'))

    def test_object_update(self):
        '''
        Checking post_save signal, 'update' action
        :return:
        '''
        count = ModelActionLog.objects.count()

        contact = Contact.objects.get()
        contact.jabber = 'ruszhov@42.cc.co'
        contact.save()

        new_count = ModelActionLog.objects.count()
        self.assertEqual(count + 1, new_count)

        log_entry = ModelActionLog.objects.latest('created')
        self.assertNotEquals(log_entry, None)
        self.assertEquals(log_entry.model_name, contact._meta.object_name)
        self.assertEquals(log_entry.instance, unicode(contact))
        self.assertEquals(log_entry.action, unicode('update'))

    def test_object_delete(self):
        '''
        Checking post_delete signal
        :return:
        '''
        count = ModelActionLog.objects.count()

        contact = Contact.objects.get()
        contact.delete()

        new_count = ModelActionLog.objects.count()
        self.assertEqual(count + 1, new_count)

        log_entry = ModelActionLog.objects.latest('created')
        self.assertNotEquals(log_entry, None)
        self.assertEquals(log_entry.model_name, contact._meta.object_name)
        self.assertEquals(log_entry.instance, unicode(contact))
        self.assertEquals(log_entry.action, unicode('delete'))


class HttpRequestLogPriorityTest(TestCase):

    def test_logging_with_priority(self):
        '''
        Checking logging with priority field
        '''

        client = Client()
        client.get('/')

        entry = HttpRequestLog.objects.get(url='/')

        self.assertNotEquals(entry, None)
        self.assertEquals(entry.request_method, 'GET')
        self.assertEquals(entry.priority, 0)

    def test_sort_by_priority(self):
        '''
        Checking sorting by priority
        '''
        url = reverse('home')
        self.client.get(url)
        url = reverse('edit-form')
        self.client.get(url)
        url = reverse('http_requests')
        self.client.get(url)
        httplog = HttpRequestLog.objects.all()[1]
        httplog.priority = 33
        httplog.save()
        self.assertEqual(
            HttpRequestLog.objects.first().priority, httplog.priority)
