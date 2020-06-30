from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.template import Template, Context
from .views import hello, http_requests, edit_form
from .models import Contact, HttpRequestLog, ModelActionLog
from .forms import ContactForm
import datetime
from freezegun import freeze_time


class InitialDataTest(TestCase):
    def test_adminuser(self):
        '''
        check if initial superuser exists and has default credentials
        '''
        default_creds = 'admin:admin'
        username, password = default_creds.split(':')
        u = User.objects.all().first()
        self.assertEqual(u.is_superuser, True)
        self.assertEqual(u.username == username, True)
        self.assertEqual(u.check_password(password), True)

    def test_model(self):
        '''
        check if initial contact data exist
        '''
        expected = ['Ruslan', 'ruszhov@42.cc.co', 'ruszhov@gmail.com']
        c = Contact.objects.all().first()
        self.assertEqual([c.first_name, c.jabber, c.email], expected)


class HomeTests(TestCase):
    fixtures = ['fixtures/initial_data.json']

    def test_hello_view_status_code(self):
        '''
        check status code
        '''
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_hello_url_resolves_home_view(self):
        '''
        check url resolving
        '''
        view = resolve('/')
        self.assertEquals(view.func, hello)


class ContactModelTest(TestCase):

    @classmethod
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
        '''
        check if the first name has label
        '''
        contact = Contact.objects.all().first()
        field_label = contact._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'First Name')

    def test_last_name_label(self):
        '''
        check if the last name has label
        '''
        contact = Contact.objects.all().first()
        field_label = contact._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'Last Name')

    def test_date_of_birth_label(self):
        '''
        check if the date of birth has label
        '''
        contact = Contact.objects.all().first()
        field_label = contact._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'Date of birth')

    def test_first_name_max_length(self):
        '''
        check max length of first name
        '''
        contact = Contact.objects.all().first()
        max_length = contact._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        '''
        check max length of last name
        '''
        contact = Contact.objects.all().first()
        max_length = contact._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)

    def test_bio_max_length(self):
        '''
        check max length of bio
        '''
        contact = Contact.objects.all().first()
        max_length = contact._meta.get_field('bio').max_length
        self.assertEquals(max_length, 200)

    def test_skype_max_length(self):
        '''
        check max length of skype
        '''
        contact = Contact.objects.all().first()
        max_length = contact._meta.get_field('skype').max_length
        self.assertEquals(max_length, 50)


class TestPage(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        '''
        checking index page, template, context
        '''
        contact = Contact.objects.all().first()
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/index.html')
        self.assertEqual(response.context['contact'], contact)
        self.assertContains(response, 'ruszhov@42.cc.co')


class HomeRequestsTests(TestCase):

    def test_requests_status_code(self):
        '''
        check status code
        '''
        url = reverse('http_requests')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_requests_url_resolve(self):
        '''
        check url equals
        '''
        url = reverse('http_requests')
        self.assertEqual(url, '/http_requests/')

    def test_requests_url_resolves_view(self):
        '''
        check url resolving
        '''
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
        '''
        checking request method
        :return:
        '''

        url = reverse('http_requests')
        entry = HttpRequestLog.objects.all().first()
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


class ContactFormTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = Client()
        self.admin.login(username='admin', password='admin')

        self._contact = {
            'first_name': 'Ruslan',
            'last_name': 'Zhovniriv',
            'date_of_birth': '1987-07-15',
            'bio': 'Developer, Full Stack',
            'email': 'ruszhov@gmail.com',
            'skype': 'ruszhov',
            'jabber': 'ruszhov@42.cc.co',
            'other_contacts': 'https://www.linkedin.com/in/ruszhov/',
        }

    def test_form_url_view(self):
        '''
        check url status code, test view
        '''
        url = reverse('edit_form')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

        view = resolve('/edit_form/')
        self.assertEquals(view.func, edit_form)

    # @freeze_time("1901-01-14")
    def test_validation_data(self):
        '''
        check custom and required validations
        :return:
        '''
        with freeze_time('1901-01-14'):
            assert datetime.datetime.now() == datetime.datetime(1901, 1, 14)
            data = {
                'first_name': '',
                'last_name': '',
                'email': '',
                'date_of_birth': datetime.datetime.now().date(),
                'jabber': 'sdhsjdhjdh---.@kk'
            }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'first_name': [u'This field is required.'],
            'last_name': [u'This field is required.'],
            'email': [u'This field is required.'],
            'date_of_birth': [u'Age can\'t be longer than 100 years!!!!'],
            'jabber': [u'This value can\'t be used as Jabber account']
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
        instance = Contact.objects.all().first()
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


class TemplateTagsTestCase(TestCase):

    def setUp(self):
        self.contact = Contact.objects.all().first()
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
            'model_name': 'User',
            'instance': 'admin',
            'action': 'update',
            'created': datetime.datetime.now()
        }

        self._contact = {
            'first_name': 'Ruslan',
            'last_name': 'Zhovniriv',
            'date_of_birth': '1987-07-15',
            'bio': 'Developer, Full Stack',
            'email': 'ruszhov@gmail.com',
            'skype': 'ruszhov',
            'jabber': 'ruszhov@42.cc.co',
            'other_contacts': 'https://www.linkedin.com/in/ruszhov/',
        }

    def test_max_length(self):
        '''
        check max length of ModelActionLog's fields
        '''
        logentry = ModelActionLog.objects.all().first()
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
        url = reverse('edit_form')
        self.client.get(url)
        url = reverse('http_requests')
        self.client.get(url)
        httplog = HttpRequestLog.objects.all()[1]
        httplog.priority = 33
        httplog.save()
        self.assertEqual(
            HttpRequestLog.objects.all().first().priority, httplog.priority)
