try:
    from django.urls import reverse
except ImportError:
    # django<=1.10
    from django.core.urlresolvers import reverse


def test_state_log_inline_django2(article, admin_client, admin_user):
    article.submit(by=admin_user)
    article.publish(by=admin_user)
    url = reverse('admin:tests_article_change', args=(article.pk,))
    response = admin_client.get(url)
    assert response.status_code == 200
    assert '{} - submit'.format(article).encode() in response.content
    assert '{} - publish'.format(article).encode() in response.content
