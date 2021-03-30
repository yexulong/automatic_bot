# -*- coding: utf-8 -*-
import os

device_type = {
    1: 'Device',
    2: 'MuMuSimulator'
}


class CreateProject(object):
    def __init__(self, project_name, hwnd_name, device):
        self.project_name = project_name
        self.project_class_name = str(self.project_name).capitalize()
        self.hwnd_name = hwnd_name
        self.device = device
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self._format_value = {
            'project_name': self.project_name,
            'project_class_name': self.project_class_name,
            'hwnd_name': self.hwnd_name,
            'device': device_type[int(self.device)]
        }

    @property
    def format_value(self):
        return self._format_value

    @format_value.setter
    def format_value(self, kwargs):
        for k, v in kwargs.items():
            self._format_value[k] = v

    def create(self, template_dir_path='./{project_name}.template', **format_value):
        self.format_value = format_value
        for root, dirs, files in os.walk(template_dir_path):
            root_path = root.replace('.template', '').format(**self.format_value)
            if not os.path.exists(root_path):
                os.mkdir(root_path)
            for file in files:
                print('{}:{}:{}'.format(root, dirs, files))
                temp_full_path = os.path.join(root, file)
                template, file_name = self.get_template(temp_full_path)
                project_full_path = os.path.join(self.base_path, file_name)
                template = template.format(**self.format_value)
                with open(project_full_path, 'w', encoding='utf8') as f:
                    f.write(template)

    def get_template(self, template_path):
        with open(template_path, 'r', encoding='utf8') as f:
            template = f.read()
        project_file_name = str(template_path).replace('.template', '').format(**self.format_value)
        return template, project_file_name


if __name__ == '__main__':
    project = input('请输入项目名称:')
    handler = input('请输入句柄名称:')
    device = int(input('请输入设备类型（1: 桌面端APP; 2: MuMu模拟器; 3: 夜神模拟器(未实现); 默认为1):'))
    # create_project(project, handler, device)
    CreateProject(project, handler, device).create()
