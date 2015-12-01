# bruce_sopel_modules
    一些sopel中文模块   A lot of sopel module for chinese users

## Install 安装:
    [if does not exists] mkdir ~/.sopel/modules/
    cd ~/.sopel/modules/
    git clone https://github.com/BruceZhang1993/bruce_sopel_modules.git
    Restart your sopel, and it should work.
    重启sopel即可使用
    
## Configure 配置
    For aqi.py:
      Edit this file and change the API Key, you may get it here -> http://pm25.in/api_doc
      修改aqi.py，在文件中设置你的API Key，API Key 申请地址：http://pm25.in/api_doc
      (默认使用公开API Key，仅测试使用。)
    For express:
      No configuration needed, API Key not required.
      无需配置即可使用，无需API Key.
    
## Uninstall 卸载
    rm -rf ~/.sopel/modules/bruce_sopel_modules/ (be care)
