# 五子棋GUI设计文档

> 作者： Adrian

因为设计gui需要和各个模块连接，所以我整个上传了一份具有“完整功能的”五子棋项目

clone/download这个文件夹后运行**Gobang.py**查看效果。

其中，AI模块和多人对战模块均直接来自网络，主要由我完成的是人机对战界面`gobangGUI.py`和主菜单`Gobang.py`。

对接时有任何问题请**直接询问我**，注释上遗留的小问题 *理论上* 会在近期解决。

# 双人部分对战说明

运行gobang.py文件进入双人对战之后 客户端1上线 等待客户端2连接
客户端2运行Player2GUI文件 与服务器连接 开启对战PS：客户端2打完一局之后自动结束 不会返回主界面


