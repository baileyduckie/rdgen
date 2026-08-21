from pathlib import Path

from django.test import TestCase

from rdgenerator import views


class GeneratorFileHandlingTests(TestCase):
    def test_project_storage_path_uses_project_root(self):
        path = views.project_storage_path('exe', 'demo-uuid', 'build.exe')
        expected = (Path(__file__).resolve().parent.parent / 'exe' / 'demo-uuid' / 'build.exe').resolve()
        self.assertEqual(Path(path), expected)

    def test_save_png_ignores_blank_data_uri(self):
        result = views.save_png('data:image/png;base64,', 'demo-uuid', 'https://example.com', 'icon.png')
        self.assertIsNone(result)
