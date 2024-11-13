# 数据集设置
dataset_type = 'CityscapesDataset'  # 数据集类型，这将被用来定义数据集
data_root = 'data/cityscapes/'  # 数据的根路径
crop_size = (512, 1024)  # 训练时的裁剪大小
train_pipeline = [  # 训练流程
    dict(type='LoadImageFromFile'),  # 第1个流程，从文件路径里加载图像
    dict(type='LoadAnnotations'),  # 第2个流程，对于当前图像，加载它的标注图像
    dict(type='RandomResize',  # 调整输入图像大小(resize)和其标注图像的数据增广流程
         scale=(2048, 1024),  # 图像裁剪的大小
         ratio_range=(0.5, 2.0),  # 数据增广的比例范围
         keep_ratio=True),  # 调整图像大小时是否保持纵横比
    dict(type='RandomCrop',  # 随机裁剪当前图像和其标注图像的数据增广流程
         crop_size=crop_size,  # 随机裁剪的大小
         cat_max_ratio=0.75),  # 单个类别可以填充的最大区域的比
    dict(type='RandomFlip',  # 翻转图像和其标注图像的数据增广流程
         prob=0.5),  # 翻转图像的概率
    dict(type='PhotoMetricDistortion'),  # 光学上使用一些方法扭曲当前图像和其标注图像的数据增广流程
    dict(type='PackSegInputs')  # 打包用于语义分割的输入数据
]
test_pipeline = [
    dict(type='LoadImageFromFile'),  # 第1个流程，从文件路径里加载图像
    dict(type='Resize',  # 使用调整图像大小(resize)增强
         scale=(2048, 1024),  # 图像缩放的大小
         keep_ratio=True),  # 在调整图像大小时是否保留长宽比
    # 在' Resize '之后添加标注图像
    # 不需要做调整图像大小(resize)的数据变换
    dict(type='LoadAnnotations'),  # 加载数据集提供的语义分割标注
    dict(type='PackSegInputs')  # 打包用于语义分割的输入数据
]
train_dataloader = dict(  # 训练数据加载器(dataloader)的配置
    batch_size=2,  # 每一个GPU的batch size大小
    num_workers=2,  # 为每一个GPU预读取数据的进程个数
    persistent_workers=True,  # 在一个epoch结束后关闭worker进程，可以加快训练速度
    sampler=dict(type='InfiniteSampler', shuffle=True),  # 训练时进行随机洗牌(shuffle)
    dataset=dict(  # 训练数据集配置
        type=dataset_type,  # 数据集类型，详见mmseg/datassets/
        data_root=data_root,  # 数据集的根目录
        data_prefix=dict(
            img_path='leftImg8bit/train', seg_map_path='gtFine/train'),  # 训练数据的前缀
        pipeline=train_pipeline))  # 数据处理流程，它通过之前创建的train_pipeline传递。
val_dataloader = dict(
    batch_size=1,  # 每一个GPU的batch size大小
    num_workers=4,  # 为每一个GPU预读取数据的进程个数
    persistent_workers=True,  # 在一个epoch结束后关闭worker进程，可以加快训练速度
    sampler=dict(type='DefaultSampler', shuffle=False),  # 训练时不进行随机洗牌(shuffle)
    dataset=dict(  # 测试数据集配置
        type=dataset_type,  # 数据集类型，详见mmseg/datassets/
        data_root=data_root,  # 数据集的根目录
        data_prefix=dict(
            img_path='leftImg8bit/val', seg_map_path='gtFine/val'),  # 测试数据的前缀
        pipeline=test_pipeline))  # 数据处理流程，它通过之前创建的test_pipeline传递。
test_dataloader = val_dataloader
# 精度评估方法，我们在这里使用 IoUMetric 进行评估
val_evaluator = dict(type='IoUMetric', iou_metrics=['mIoU'])
test_evaluator = val_evaluator
