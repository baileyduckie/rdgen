from pathlib import Path

from django.test import TestCase, RequestFactory

from rdgenerator import views


class GeneratorFileHandlingTests(TestCase):
    def test_project_storage_path_uses_project_root(self):
        path = views.project_storage_path('exe', 'demo-uuid', 'build.exe')
        expected = (Path(__file__).resolve().parent.parent / 'exe' / 'demo-uuid' / 'build.exe').resolve()
        self.assertEqual(Path(path), expected)

    def test_save_png_ignores_blank_data_uri(self):
        result = views.save_png('data:image/png;base64,', 'demo-uuid', 'https://example.com', 'icon.png')
        self.assertIsNone(result)

    def test_settings_do_not_hardcode_sensitive_defaults(self):
        from rdgen import settings as app_settings

        self.assertEqual(app_settings.GHBEARER, '')
        self.assertEqual(app_settings.GENURL, '')
        self.assertEqual(app_settings.ZIP_PASSWORD, '')
        self.assertNotIn('github_pat_', app_settings.GHBEARER)
        self.assertNotIn('ngrok', app_settings.GENURL.lower())

    def test_build_public_base_url_prefers_configured_genurl(self):
        request = RequestFactory().get('/generator')
        with self.settings(GENURL='https://example.com', PROTOCOL='https'):
            self.assertEqual(views.build_public_base_url(request), 'https://example.com')

    def test_build_public_base_url_falls_back_to_request_host(self):
        request = RequestFactory().get('/generator', HTTP_HOST='localhost:8000')
        with self.settings(GENURL='', PROTOCOL='https'):
            self.assertEqual(views.build_public_base_url(request), 'https://localhost:8000')
