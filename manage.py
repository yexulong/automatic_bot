# -*- coding: utf-8 -*-
import os

device_type = {
    1: 'Device',
    2: 'MuMuSimulator'
}


def create_project(project_name: str, hwnd_name: str , device: int = 1):
    img_dir = os.path.join(project_name, 'img')
    img_template_dir = os.path.join(img_dir, 'template')
    img_screenshots_dir = os.path.join(img_dir, 'screenshots')
    log_dir = os.path.join(project_name, 'log')
    os.mkdir(project_name)
    os.mkdir(img_dir)
    os.mkdir(img_template_dir)
    os.mkdir(img_screenshots_dir)
    os.mkdir(log_dir)

    enter_file_name = os.path.join(project_name, '{}.py'.format(project_name))
    template = get_template('project.template/py.template')
    project_class_name = project_name[:1].upper() + project_name[1:]
    template = template.format(project_name=project_name, project_class_name=project_class_name, hwnd_name=hwnd_name, device=device_type[int(device)])
    with open(enter_file_name, 'w', encoding='utf8') as f:
        f.write(template)


def get_template(template_path):
    with open(template_path, 'r', encoding='utf8') as f:
        template = f.read()
    return template


if __name__ == '__main__':
    project = input('请输入项目名称:')
    handler = input('请输入句柄名称:')
    device = int(input('请输入设备类型（1: 桌面端APP; 2: MuMu模拟器; 3: 夜神模拟器(未实现); 默认为1):'))
    create_project(project, handler, device)
