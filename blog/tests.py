from django.test import TestCase
from django.shortcuts import reverse
from .models import Post
from django.contrib.auth.models import User

class BlogTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user1')  #make an instance for User
        cls.post_obj = Post.objects.create(
            status=Post.STATUS_CHOICES[0][0],
            title='title1',
            text='sample text',
            author= cls.user,
        )
        cls.post_obj2 = Post.objects.create(
            status=Post().STATUS_CHOICES[1][0],
            title='title2',
            text='some lorem ipsum',
            author=cls.user,
        )


    #testing post model str
    def test_post_model_str(self):
        self.assertEqual(str(self.post_obj), self.post_obj.title)

    #testing post detail
    def test_post_detail(self):
        self.assertEqual(self.post_obj.title, 'title1')
        self.assertEqual(self.post_obj.text, 'sample text')

    # testing post list URL
    def test_post_list_url(self):
        response1 = self.client.get('/blog/')
        self.assertEqual(response1.status_code, 200)


    # testing post list URL By name
    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    
    # testing post detail URL
    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.post_obj.id}/')
        self.assertEqual(response.status_code, 200)


    # testing post list URL By name
    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post_obj.id]))
        self.assertEqual(response.status_code, 200)


    # testing post detail cotains obj
    def test_post_detail_page(self):
        response = self.client.get('/blog/1/')
        self.assertContains(response, self.post_obj.text)


    # testing post list cotains objs
    def test_blog_list(self):
        response1 = self.client.get(reverse('post_list'))
        self.assertContains(response1, self.post_obj)
        self.assertContains(response1, self.post_obj.text)


    # testing 404 status code for id does not exist
    def test_status_404_post_id_does_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[99]))
        self.assertEqual(response.status_code, 404)


    # testing draft posts for not shown
    def test_draft_not_shown(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post_obj.title)
        self.assertNotContains(response, self.post_obj2.title)


    # testing post list templates
    def test_post_list_correct_template(self):
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'blog/posts_list.html')

    #testing CRUD: create for post
    def test_post_create(self):
        response = self.client.post(reverse('post_create'), 
        {
            'title' : 'sample title', 
            'text' : 'sample text',
            'status' : 'published',
            'author' : self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'sample title')
        self.assertEqual(Post.objects.last().text, 'sample text')


    #testing CRUD: update for post
    def test_post_update(self):
        response = self.client.post(reverse('post_update', args=[self.post_obj2.id]), {
            'title' : 'title:updated',
            'text' : 'text:updated',
            'status' : 'published',
            'author' : self.post_obj2.author.id, 
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'title:updated')
        self.assertEqual(Post.objects.last().text, 'text:updated')

    def test_post_delete(self):
        response = self.client.post(reverse('post_delete', args=[self.post_obj.id]))
        self.assertEqual(response.status_code, 302)









        



