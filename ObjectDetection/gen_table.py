'''
Author: goog
Date: 2021-08-27 10:50:06
LastEditTime: 2021-08-27 10:58:10
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/ObjectDetection/gen_table.py
Time Limit Exceeded!
'''
es = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush']
cn = ['人','自行车','汽车','摩托车','飞机','公共汽车','火车','卡车','船','交通灯','消防栓','路牌', '停车标志', '停车计时器', '长凳', '鸟', '猫', '狗', '马', '羊', '牛', '大象', '熊', '斑马' , '长颈鹿', '帽子', '背包', '雨伞', '鞋子', '眼镜', '手提包', '领带', '手提箱', '飞盘', '滑雪板', '滑雪板' , '运动球', '风筝', '棒球棒', '棒球手套', '滑板', '冲浪板', '网球拍', '瓶子', '盘', '酒杯', '杯子', '叉子','刀','勺子','碗','香蕉','苹果','三明治','橙子','西兰花','胡萝卜','热狗','披萨','甜甜圈','蛋糕','椅子','沙发','盆栽','床','镜子','餐桌','窗户','书桌','厕所','门','电视','笔记本电脑','鼠标','遥控器','键盘','手机','微波炉','烤箱','烤面包机','水槽','冰箱','搅拌机','书', '时钟', '花瓶', '剪刀', '泰迪熊', '吹风机', '牙刷', '毛刷'] 
print(len(es))
print(len(cn))
str=""
for i in range(len(es)):
    str=str+"|"+es[i]+"|"+cn[i]+"|"
print(str)
