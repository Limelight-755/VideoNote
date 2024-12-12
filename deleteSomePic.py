import os
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN

# 加载预训练的 ResNet50 模型并去掉最后的分类层
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')


# 步骤 1: 特征提取函数
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # 调整图像大小
    img_array = image.img_to_array(img)  # 将图像转换为数组
    img_array = np.expand_dims(img_array, axis=0)  # 增加批次维度
    img_array = preprocess_input(img_array)  # 预处理图像
    features = model.predict(img_array)  # 提取特征
    return features.flatten()  # 展平为1D向量


# 步骤 2: 特征向量降维
def reduce_dimensions(features, n_components=25):
    pca = PCA(n_components=n_components)
    reduced_features = pca.fit_transform(features)
    return reduced_features


# 步骤 3: 图像聚类
def cluster_images(features, eps=30, min_samples=1):
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean').fit(features)
    return clustering.labels_


# 步骤 4: 去除相似图像并删除多余图像
def remove_similar_images(image_paths, labels):
    unique_images = []
    seen_clusters = set()
    images_to_delete = []  # 存储需要删除的图像

    for i, label in enumerate(labels):
        if label not in seen_clusters and label != -1:  # 忽略噪声点
            unique_images.append(image_paths[i])  # 保留此簇的第一个图像
            seen_clusters.add(label)  # 记录已经处理的簇
        else:
            images_to_delete.append(image_paths[i])  # 将重复的图像加入待删除列表

    # 删除多余的图像
    for img in images_to_delete:
        if os.path.exists(img):
            os.remove(img)  # 删除文件
            print(f"已删除图像: {img}")

    return unique_images


# 主函数
def process_images(image_folder):
    # 获取文件夹中的所有图像路径
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if
                   f.endswith(('.png', '.jpg', '.jpeg'))]

    # 提取所有图像的特征
    print("提取特征中...")
    features = np.array([extract_features(path) for path in image_paths])

    # 降维
    print("降维中...")
    reduced_features = reduce_dimensions(features)

    # 聚类
    print("聚类中...")
    labels = cluster_images(reduced_features)

    # 去除相似图像并删除不需要的图像
    print("去除相似图像中...")
    unique_images = remove_similar_images(image_paths, labels)

    print(f"原始图像数量: {len(image_paths)}")
    print(f"去重后剩余图像数量: {len(unique_images)}")

    return unique_images


if __name__ == "__main__":
    # 实例调用
    image_folder = "extractimg"
    unique_images = process_images(image_folder)




