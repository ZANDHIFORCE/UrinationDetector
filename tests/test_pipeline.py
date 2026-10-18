import contextlib
from datetime import datetime, timedelta
from io import BytesIO
import os
from pathlib import Path
import runpy
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from PIL import Image
import requests


root = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def change_module(self, cv2=None):
        with patch.dict(sys.modules, {'cv2': cv2 or SimpleNamespace()}):
            return runpy.run_path(str(root/'vision/yolov5/change_detection.py'))

    def test_ten_second_trigger_and_reset(self):
        namespace = self.change_module()
        detector = namespace['ChangeDetection'](['person', 'car'])
        detector.send = Mock()
        start = datetime(2026, 10, 19)
        clock = Mock()
        clock.now.side_effect = [start + timedelta(seconds=n) for n in (0, 9, 10, 19, 20, 100, 109, 110)]
        with patch.dict(namespace['ChangeDetection'].add.__globals__, {'datetime': clock}):
            for state in ([1, 0], [1, 0], [1, 1]):
                detector.add(['person', 'car'], state, 'unused', 'frame')
            self.assertEqual(detector.send.call_count, 1)
            self.assertEqual(detector.text, 'person, car, ')
            detector.add(['person', 'car'], [1, 0], 'unused', 'frame')
            self.assertEqual(detector.send.call_count, 1)
            detector.add(['person', 'car'], [1, 0], 'unused', 'frame')
            self.assertEqual(detector.send.call_count, 2)
            detector.add(['person', 'car'], [0, 0], 'unused', 'frame')
            self.assertIsNone(detector.timestamp1)
            self.assertIsNone(detector.timestamp2)
            for state in ([1, 0], [1, 0], [1, 0]):
                detector.add(['person', 'car'], state, 'unused', 'frame')
            self.assertEqual(detector.send.call_count, 3)

    def test_upload_fields_auth_and_file_closure(self):
        cv2 = SimpleNamespace(INTER_AREA=3, resize=Mock(return_value='small'))
        cv2.imwrite = Mock(side_effect=lambda path, image: Path(path).write_bytes(b'mock image'))
        namespace = self.change_module(cv2)
        for token in ('local-test-token', ''):
            with patch.dict(os.environ, {'URINATION_API_URL': 'http://127.0.0.1:8000/', 'URINATION_API_TOKEN': token}):
                detector = namespace['ChangeDetection'](['person'])
            detector.title, detector.text, detector.label = 'Person', 'person, ', 'UCF'
            for failure in (False, True):
                with self.subTest(token=bool(token), failure=failure), tempfile.TemporaryDirectory() as directory:
                    response = Mock()
                    if failure:
                        response.raise_for_status.side_effect = requests.HTTPError('mock failure')
                    captured = {}
                    def upload(url, **kwargs):
                        captured.update(url=url, **kwargs)
                        self.assertFalse(kwargs['files']['image'].closed)
                        return response
                    with patch('requests.post', side_effect=upload):
                        if failure:
                            with self.assertRaises(requests.HTTPError):
                                detector.send(directory, 'frame')
                        else:
                            detector.send(directory, 'frame')
                    self.assertEqual(captured['url'], 'http://127.0.0.1:8000/api_root/Posts/')
                    self.assertEqual(captured['timeout'], 30)
                    self.assertEqual(set(captured['data']), {'title', 'text', 'created_date', 'published_date', 'label'})
                    self.assertEqual(captured['data']['label'], 'UCF')
                    self.assertEqual(captured['headers'].get('Authorization'), 'Token '+token if token else None)
                    image_file = captured['files']['image']
                    self.assertTrue(image_file.closed)
                    self.assertTrue(Path(image_file.name).is_relative_to(Path(directory)/'detected'))
                    self.assertIsInstance(cv2.imwrite.call_args.args[0], str)
                    cv2.resize.assert_called_with('frame', dsize=(320, 240), interpolation=3)

    def test_export_no_import_network_and_alternate_cwd(self):
        script = root/'tools/dataset_export/export_images.py'
        with patch('requests.get') as get, patch('requests.post') as post:
            namespace = runpy.run_path(str(script))
        get.assert_not_called()
        post.assert_not_called()
        image = BytesIO()
        Image.new('RGB', (2, 2)).save(image, format='JPEG')
        for login in (False, True):
            with tempfile.TemporaryDirectory() as directory, contextlib.chdir(root.parent):
                record = {'published_date': '2026-10-19T10:11:12+09:00', 'label': 'URN', 'image': '/media/test.jpg'}
                listing = Mock()
                listing.json.return_value = [record]
                picture = Mock(content=image.getvalue())
                auth = Mock()
                auth.json.return_value = {'token': 'login-token'}
                env = {'URINATION_API_URL': 'http://127.0.0.1:8000/', 'URINATION_API_TOKEN': '' if login else 'test-token',
                       'URINATION_API_USERNAME': 'local' if login else '', 'URINATION_API_PASSWORD': 'test-only'}
                with patch.dict(namespace['main'].__globals__, {'__file__': str(Path(directory)/'export_images.py')}), \
                     patch.dict(os.environ, env), patch('requests.get', side_effect=[listing, picture]) as get, \
                     patch('requests.post', return_value=auth) as post:
                    namespace['main']()
                expected = Path(directory)/'image_output/URN/2026-10-19T10_11_12+09_00.jpg'
                self.assertTrue(expected.is_file())
                self.assertEqual(get.call_args_list[1].args[0], 'http://127.0.0.1:8000/media/test.jpg')
                self.assertEqual(get.call_args_list[0].kwargs['headers']['Authorization'], 'Token '+('login-token' if login else 'test-token'))
                if login:
                    post.assert_called_once_with('http://127.0.0.1:8000/api-token-auth/', data={'username': 'local', 'password': 'test-only'}, timeout=30)
                else:
                    post.assert_not_called()

    def test_inference_paths_without_hardware(self):
        script = root/'inference/run_classifier.py'
        with patch.dict(sys.modules, {'cv2': Mock(), 'keras.models': Mock()}) as modules:
            namespace = runpy.run_path(str(script))
            modules['keras.models'].load_model.assert_not_called()
            modules['cv2'].VideoCapture.assert_not_called()
        for cwd in (root, root.parent):
            load_model = Mock()
            camera = Mock()
            camera.read.side_effect = StopIteration('stop before hardware')
            cv2 = SimpleNamespace(VideoCapture=Mock(return_value=camera))
            with contextlib.chdir(cwd), patch.dict(sys.modules, {
                'keras': SimpleNamespace(), 'keras.models': SimpleNamespace(load_model=load_model),
                'cv2': cv2, 'numpy': SimpleNamespace(set_printoptions=Mock()),
            }):
                with self.assertRaisesRegex(StopIteration, 'stop before hardware'):
                    namespace['main']()
            load_model.assert_called_once_with(str(script.parent/'keras_Model.h5'), compile=False)
            self.assertTrue((script.parent/'labels.txt').is_file())


if __name__ == '__main__':
    unittest.main()
