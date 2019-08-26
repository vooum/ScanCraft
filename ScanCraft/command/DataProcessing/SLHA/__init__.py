#!/usr/bin/env python3

# 说明：
# 该SLHA读取包大量采用了懒加载属性
# 读取SLHA数据文件：
#     从文件读取：
#     spectr=SLHA_document({path},blockformat=ReadBlock)
#         path 文件路径
#         blockformat 该对象包含了各种block对应的读取方法
#     从字符串列表读取：
#     spectr=SLHA_text({text_list},blockformat=ReadBlock)
#         text_list 字符串列表，每个元素是一行，通常用file_object.readlines()获取
# 访问数据：
#     spectr({block_name},code)
#     block_name:
#         大写，三种选择：
#         1.获取数据所在的block的名，如'MASS','NMNMIX'
#         2.获取粒子的衰变 'DECAY'
#         3.获取粒子的宽度 'WIDTH'
#     code:
#         1.获取某block中的数据，code写数据的编号，单个编号填整数(int)，矩阵元素填元组(tuple)
#         2.获取衰变的宽度，先填入粒子的PDG编号，再填末态粒子PDG编号的元组
#         3.获取宽度，填粒子PDG编号