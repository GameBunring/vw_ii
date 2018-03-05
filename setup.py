from distutils.core import setup
import py2exe
import os


images = ["images/" + i for i in os.listdir('images') if i[-4:]==".jpg"]
setup(
    windows=[
    	{"script": 'main.py',
    	"icon_resources": [(1, "main.ico")]
    }],
    data_files=[("", ['2018车辆管理系统导入模板.xls', 'config.ini']),
    	('icon', ['icon/main.ico', 'icon/vw.ico']),
    	("images", images)],
    options={
        'py2exe': {
            'packages': ['xlrd', 'qrcode']
        }
    }
)
