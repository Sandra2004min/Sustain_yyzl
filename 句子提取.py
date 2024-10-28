import fitz  # PyMuPDF
import re
import pandas as pd
import os

def extract_sentences_from_pdf(pdf_path):
    try:
        # 打开PDF文件
        document = fitz.open(pdf_path)

        # 初始化结果列表
        all_sentences = []

        for page_num in range(len(document)):
            page = document.load_page(page_num)  # 加载每一页
            text = page.get_text("text")  # 获取页面文本

            # 使用正则表达式分割句子，包括中文和英文标点
            sentences = re.split(r'(?<=[。！？\.!?])', text)

            # 去除空句子，并确保每个句子在一行内显示
            sentences = [re.sub(r'\s+', ' ', s.strip()) for s in sentences if s.strip()]

            all_sentences.extend(sentences)

    except Exception as e:
        return []

    return all_sentences


def extract_sentences_with_keywords(pdf_path, keywords):
    sentences = extract_sentences_from_pdf(pdf_path)

    # 匹配关键词的句子
    matching_sentences = []
    for sentence in sentences:
        for keyword in keywords:
            if re.escape(keyword).lower() in sentence.lower():
                matching_sentences.append(sentence)

    return matching_sentences


def process_pdfs_in_folder(folder_path, keywords, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            matching_sentences = extract_sentences_with_keywords(pdf_path, keywords)

            # 创建 DataFrame 并保存到 Excel 文件
            df = pd.DataFrame(matching_sentences, columns=['Sentence'])
            excel_filename = os.path.splitext(filename)[0] + '.xlsx'
            excel_path = os.path.join(output_folder, excel_filename)
            df.to_excel(excel_path, index=False)

            print(f"Matching sentences from {filename} saved to {excel_path}")


if __name__ == "__main__":
    folder_path = r"C:\Users\HP\Desktop\易旻小组\供应商\黑色金属矿采选业\黑色金属矿采选业"  # 文件夹路径
    output_folder = r"C:\Users\HP\Desktop\易旻小组\供应商\output"  # 输出文件夹路径
    keywords = [
        '二氧化碳', '甲烷', '氧化亚氮', '六氟化硫', '氢氟碳化物', '全氟碳化物', '氟氯碳化物', '氯一氟甲烷',
        '氯二氟甲烷', '一氯三氟甲烷', '五氯一氟乙烷', '四氯二氟乙烷', '三氯三氟乙烷', '1.2-二氯四氣乙烷',
        '氯五氟乙烷', '七氯一氟丙烷', '六氯二氟丙烷', '五氯三氟丙烷', '四氯四氟丙烷', '氯五氟丙烷',
        '氯六氟丙烷', '氯七氟丙烷', '氢氯氟碳化物', '臭气', '氨', '氮氧化物', '一氧化氮', '二氧化氮',
        '一氧化碳', '氟化氢', '磷化氢', '肼', '过氧化氢', '叠氮酸', '叠氮化钠', '元素磷', '黄磷', '五硫化二磷',
        '五氧化二磷', '三氯化磷', '氰化物', '氟化物', '碘化物', '硫酰氟', '氰化氢', '氯', '氧化氯', '氯化氢',
        '氯化亚砜', '氧化硫', '三氧化硫', '硫化氢', '降水量', '降水类型', '降水 pH 值', '电导率', '硫酸根离子',
        '硝酸根离子', '氟离子', '氯离子', '铵离子', '钙离子', '镁离子', '钠离子', '钾离子', '碳酸氢根离子',
        '溴离子', '甲酸根离子', '醋酸根离子', '磷酸根离子', '亚硝酸根离子', '亚硫酸根离子', '铝及其化合物',
        '铝', '锑及其化合物', '氧化锑', '砷及其化合物', '砷', '五氧化二砷', '三氧化二砷', '砷化氢',
        '钡及其化合物', '钡', '氯化钡', '氢氧化钡', '氧化钡', '铍及其化合物', '铍', '氧化铍', '铋及其化合物',
         '碲化铋', '硼及其化合物', '硼', '氧化硼', '镉及其化合物', '镉', '氧化镉', '钙及其化合物', '钙',
        '氰氨化钙', '氧化钙', '铬及其化合物', '铬', '铬酸盐', '重铬酸盐', '三氧化铬', '钴及其化合物', '钴',
        '氧化钴', '铜及其化合物', '饷', '氧化铜', '铅及其化合物', '氧化铅', '硫化铅', '四乙基铅',
        '锂及其化合物', '锂', '氢化锂', '镁及其化合物', '氧化镁', '锰及其化合物', '锰', '二氧化锰',
        '汞及其化合物', '汞', '氯化汞', '钼及其化合物', '钼', '氧化钼镍及其化合物', '镍', '硝酸镍', '氧化镍',
        '钾及其化合物', '钾', '氯化钾氢氧化钾', '硒及其化合物', '硒', '二氧化硒', '钠及其化合物', '钠',
        '碳酸钠', '氢氧化钠', '锶濟及其化合物', '锶', '饈鉤嬤ㄇ様友化锶', '氧化锶', '钽及其化合物', '檗',
        '枬进↘彩氧化二钽', '碲及其化合物', '碲', '氧化碲', '铊及其化合物', '铊', '氧化铊', '锡及其化合物', '锡',
        '二氧化锡', '钛及其化合物', '钛', '四氯化钛', '钨及其化合物', '鸽', '碳化钨', '钒及其化合物', '钒',
        '钒铁合金', '锌及其化合物', '氧化锌', '锆及其化合物', '锆', '氧化锆',
        '尾矿渣 ', '烧结烟尘', '高炉渣', '高炉瓦斯泥', '高炉瓦斯灰', '钢渣', '转炉尘土',
        '轧钢尘泥', '脱硫渣', '铜冶炼渣选尾矿', '铜冶炼贫化渣', '铜冶炼熔炼渣', '铜冶炼吹炼渣', '铜冶炼阳极炉精炼渣',
        '铜冶炼不合格阳极板', '铜冶炼不合格阳残极', '铜冶炼阳极泥冶炼炉渣', '黑铜粉', '铜电积铅泥', '湿法炼铜浸渣',
        '中和渣', '水淬渣', '铅锌冶炼渣', '镍钴冶炼渣', '锡冶炼渣', '锑冶炼渣', '镁冶炼渣', '硅冶炼渣', '粉煤灰',
        '煤矸石', '铁尾矿', '锰铬尾矿', '铜尾矿', '铅锌尾矿', '镍钴尾矿', '锡尾矿', '锑尾矿', '铝尾矿', '铝矿泥',
        '镁尾矿', '金尾矿', '银尾矿', '钨钼尾矿', '稀土金属尾矿', '化学尾矿', '其他非金属尾矿', '其他尾矿', '赤泥',
        '水基钻井岩屑和泥浆（石油）', '废弃石油钻井液', '酸化残渣', '焦渣', '气化炉渣', '气化炉灰', '三废焚烧炉灰渣',
        '废盐', '工程渣土', '工程泥浆', '工程垃圾']

    # 处理文件夹中的所有PDF文件
    process_pdfs_in_folder(folder_path, keywords, output_folder)