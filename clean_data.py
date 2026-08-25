#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据清洗脚本：从 CSV 文件中提取 IP 端口号和地区，生成 txt 文件
格式：IP:端口#地区
"""

import csv
import os
from collections import defaultdict

def clean_data(input_file='result.csv', output_dir='cleaned'):
    """
    清洗数据，按地区分类保存
    
    Args:
        input_file: 输入的 CSV 文件路径
        output_dir: 输出目录
    """
    # 清空输出目录（确保删除上轮有但本轮没有的地区文件）
    if os.path.exists(output_dir):
        import shutil
        print(f"正在清空输出目录：{output_dir}")
        shutil.rmtree(output_dir)
    
    # 重新创建输出目录
    os.makedirs(output_dir)
    
    # 按地区分组存储数据
    data_by_region = defaultdict(list)
    
    print(f"正在读取文件：{input_file}")
    
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            ip = row.get('IP', '').strip()
            port = row.get('端口', '').strip()
            country = row.get('CF归属国', '').strip()
            
            # 跳过无效数据
            if not ip or not port:
                continue
            
            # 格式化：IP:端口#地区
            entry = f"{ip}:{port}#{country}"
            data_by_region[country].append(entry)
    
    # 按地区保存文件
    print(f"正在保存数据到 {output_dir} 目录...")
    
    for region, entries in data_by_region.items():
        # 使用地区代码作为文件名
        filename = f"{region}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(entry + '\n')
        
        print(f"已保存 {len(entries)} 条数据到 {filename}")
    
    # 也可以保存一个合并的总文件
    all_entries = []
    for entries in data_by_region.values():
        all_entries.extend(entries)
    
    if all_entries:
        total_file = os.path.join(output_dir, 'all.txt')
        with open(total_file, 'w', encoding='utf-8') as f:
            for entry in all_entries:
                f.write(entry + '\n')
        print(f"已保存总计 {len(all_entries)} 条数据到 all.txt")
    
    print("数据清洗完成！")

if __name__ == '__main__':
    clean_data()
