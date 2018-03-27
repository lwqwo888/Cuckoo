# coding=utf-8
import os
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Sync(object):
    def __init__(self):
        pass
    def start(self):
        print 666666666666666


def main():
    sync = Sync()
    cfg_name = "/sync_config.cfg"
    folder = os.getcwd() + cfg_name
    with open(folder) as f:  # 默认模式为‘r’，只读模式
        contents = f.read()  # 读取文件全部内容
    run_mode = "normal"
    json_obj = json.loads(contents)
    print json_obj["path"]
    lock_file = '.lock_bajisitan_huangjia_' + run_mode
    if os.path.exists(lock_file):
        print('%s 模式已在运行中...' % lock_file)
        os.remove(lock_file)
        sys.exit(1)
    if os.path.exists('.stop_bajisitan_huangjia_end'):
        print('模式运行已完成...')
        sys.exit(0)
    file_hide = file(lock_file, 'w')
    file_hide.write(lock_file)
    file_hide.close()

    try:
        sync.start()
        end_file = '.stop_bajisitan_huangjia_end'
        file_hide = file(end_file, 'w')
        file_hide.write(end_file)
        file_hide.close()
    except Exception as e:
        print e
    finally:
        if os.path.exists(lock_file):
            os.remove(lock_file)



if __name__ == '__main__':
    main()