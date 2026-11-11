import importlib.util
from pathlib import Path
import unittest


class IsolationTest(unittest.TestCase):
    def audit(self, text):
        path = Path(__file__).resolve().parents[1] / 'scripts/check_isolation.py'
        self.assertTrue(path.exists(), 'Falta el verificador de aislamiento')
        spec = importlib.util.spec_from_file_location('check_isolation', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.audit(text)

    def safe(self):
        return '\n'.join([f'nic{i}="none"' for i in range(1, 9)] + [
            'clipboard="disabled"', 'draganddrop="disabled"',
            'vrde="off"', 'usb="off"', 'ehci="off"', 'xhci="off"'])

    def test_accepts_disconnected_vm(self):
        self.assertEqual(self.audit(self.safe()), [])

    def test_rejects_each_network_escape(self):
        for mode in ['nat', 'bridged', 'hostonly', 'intnet', 'natnetwork']:
            with self.subTest(mode=mode):
                self.assertTrue(self.audit(self.safe().replace('nic1="none"', f'nic1="{mode}"')))

    def test_missing_config_is_not_success(self):
        self.assertTrue(self.audit(''))

    def test_rejects_host_integrations(self):
        for key, value in [('clipboard', 'bidirectional'), ('draganddrop', 'hosttoguest'),
                           ('vrde', 'on'), ('usb', 'on'), ('ehci', 'on'), ('xhci', 'on')]:
            with self.subTest(key=key):
                lines=[line for line in self.safe().splitlines() if not line.startswith(key+'=')]
                self.assertTrue(self.audit('\n'.join(lines+[f'{key}="{value}"'])))

    def test_rejects_shared_folder(self):
        self.assertTrue(self.audit(self.safe()+'\nSharedFolderNameMachineMapping1="vagrant"'))


if __name__ == '__main__':
    unittest.main()
