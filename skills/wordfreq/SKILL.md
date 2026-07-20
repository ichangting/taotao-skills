---
name: wordfreq
description: |
  文档词频分析统计技能，支持 Word/PDF/EPUB/TXT 格式，输出表格 + 可视化图表
version: 1.0.0
author: 涛涛
license: MIT
display-name: 文本词频
category: 评价考情
homepage: https://github.com/ichangting/taotao-skills/tree/main/skills/wordfreq
---



# 词频分析统计技能 (Word Frequency Analysis)

## 技能定位

本技能用于对上传的文档进行**词频统计分析**，支持多种文档格式，输出结构化的词频数据和可视化图表，适用于：
- 文本内容分析
- 教学材料研究
- 写作风格分析
- 关键词提取
- 文档主题识别

---

## 支持的文档格式

| 格式 | 扩展名 | 处理方式 |
|------|--------|----------|
| Word 文档 | .docx, .doc | python-docx 提取 |
| PDF 文档 | .pdf | PyPDF2 / pdfplumber 提取 |
| EPUB 电子书 | .epub | ebooklib 提取 |
| 纯文本 | .txt, .md | 直接读取 |
| HTML 网页 | .html, .htm | BeautifulSoup 提取正文 |

---

## 核心功能

### 1. 文本提取

- 从各种格式文档中提取纯文本
- 保留段落结构（可选）
- 过滤页眉页脚、页码等噪音（PDF）

### 2. 中文分词

- 使用 `jieba` 进行中文分词
- 支持自定义词典
- 支持专有名词保护（人名、地名、机构名）

### 3. 词频统计

- 统计每个词的出现次数
- 计算词频占比（该词占总词数的百分比）
- 支持词性筛选（名词、动词、形容词等）
- 支持停用词过滤

### 4. 可视化输出

| 图表类型 | 说明 | 适用场景 |
|----------|------|----------|
| 词云图 | 词频越高字体越大 | 快速概览高频词 |
| 柱状图 | Top N 高频词 | 精确对比前 N 个词 |
| 饼图 | 词性分布 | 了解词汇构成 |
| 折线图 | 词频分布趋势 | 观察词频衰减规律 |
| 表格 | 完整词频列表 | 详细数据查阅 |

### 5. 高级分析

- **关键词提取**：基于 TF-IDF 算法
- **共现分析**：哪些词经常一起出现
- **情感分析**：文档整体情感倾向（可选）
- **主题识别**：推测文档主题类别

---

## 使用方法

### 基本用法

用户上传文档后，直接进行分析：

```
请分析这份文档的词频
```

### 指定参数

```
请分析这份文档的词频，Top 50，排除停用词
```

```
生成词云图和柱状图，只要名词
```

### 配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| top_n | 显示前 N 个高频词 | 50 |
| min_freq | 最小词频阈值 | 2 |
| exclude_stopwords | 是否排除停用词 | 是 |
| wordcloud | 是否生成词云图 | 是 |
| barchart | 是否生成柱状图 | 是 |
| pos_filter | 词性筛选（n 名词/v 动词/a 形容词） | 全部 |
| min_word_length | 最小词长（过滤单字词） | 2 |

---

## 处理流程

### Step 1: 接收文档

- 接收用户上传的文档
- 自动识别文档格式
- 确认分析参数（可使用默认值）

### Step 2: 文本提取

根据文档格式调用相应提取器：

```python
# Word 文档
from docx import Document
doc = Document(file_path)
text = "\n".join([p.text for p in doc.paragraphs])

# PDF 文档
import pdfplumber
with pdfplumber.open(file_path) as pdf:
    text = "\n".join([page.extract_text() for page in pdf.pages])

# EPUB 电子书
from ebooklib import epub
book = epub.read_epub(file_path)
text = "".join([item.get_content().decode() for item in book.get_items_of_kind(kind='item.kind.document')])
```

### Step 3: 文本预处理

- 去除特殊字符、多余空白
- 统一繁简体（可选）
- 数字/英文处理（保留或移除）
- 分段/分句（可选）

### Step 4: 中文分词

```python
import jieba

# 基础分词
words = jieba.lcut(text)

# 精确模式（默认）
words = jieba.lcut(text, cut_all=False)

# 全模式
words = jieba.lcut(text, cut_all=True)

# 搜索引擎模式
words = jieba.lcut_for_search(text)
```

### Step 5: 过滤处理

```python
# 加载停用词表
stopwords = set([line.strip() for line in open('stopwords.txt', encoding='utf-8')])

# 过滤
filtered_words = [
    w for w in words 
    if w not in stopwords 
    and len(w) >= min_word_length
    and not w.isdigit()
    and not re.match(r'^[a-zA-Z]+$', w)  # 可选：排除纯英文
]
```

### Step 6: 词频统计

```python
from collections import Counter

word_counts = Counter(filtered_words)
top_words = word_counts.most_common(top_n)
```

### Step 7: 可视化生成

#### 词云图

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wc = WordCloud(
    font_path='simhei.ttf',  # 中文字体
    width=1600,
    height=900,
    background_color='white',
    max_words=200,
    colormap='viridis'
).generate(text)

plt.figure(figsize=(16, 9))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.savefig('wordcloud.png', dpi=300, bbox_inches='tight')
```

#### 柱状图

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(top_words, columns=['词语', '词频'])

plt.figure(figsize=(12, 8))
plt.barh(range(len(df)), df['词频'], color='steelblue')
plt.yticks(range(len(df)), df['词语'], fontproperties='SimHei')
plt.xlabel('词频', fontproperties='SimHei')
plt.title(f'Top {top_n} 高频词', fontproperties='SimHei')
plt.gca().invert_yaxis()
plt.savefig('barchart.png', dpi=300, bbox_inches='tight')
```

### Step 8: 输出结果

输出结构化报告 + 可视化图表文件

---

## 输出报告模板

```markdown
# 词频分析报告

**文档名称**：xxx.docx
**文档格式**：Word 文档
**文本长度**：12,345 字
**总词数**：8,765 词
**去重词数**：2,345 词
**分析时间**：2026-04-01 17:30

---

## 📊 统计概览

| 指标 | 数值 |
|------|------|
| 总字数 | 12,345 |
| 总词数 | 8,765 |
| 去重词数 | 2,345 |
| 平均词长 | 2.3 字 |
| 停用词排除 | 1,234 个 |

---

## 🔝 Top 50 高频词

| 排名 | 词语 | 词频 | 占比 | 词性 |
|------|------|------|------|------|
| 1 | 学生 | 234 | 2.67% | 名词 |
| 2 | 学习 | 189 | 2.16% | 动词 |
| 3 | 教师 | 156 | 1.78% | 名词 |
| 4 | 教学 | 145 | 1.65% | 名词 |
| 5 | 课程 | 132 | 1.51% | 名词 |
| ... | ... | ... | ... | ... |

---

## 📈 词性分布

| 词性 | 数量 | 占比 |
|------|------|------|
| 名词 (n) | 3,456 | 39.4% |
| 动词 (v) | 2,123 | 24.2% |
| 形容词 (a) | 1,234 | 14.1% |
| 副词 (d) | 876 | 10.0% |
| 其他 | 1,076 | 12.3% |

---

## 🎨 可视化图表

### 词云图
![词云图](wordcloud.png)

### Top 20 柱状图
![柱状图](barchart.png)

### 词性分布饼图
![饼图](piechart.png)

---

## 🔑 关键词提取 (TF-IDF)

| 关键词 | TF-IDF 得分 |
|--------|------------|
| 核心素养 | 0.089 |
| 深度学习 | 0.076 |
| 单元教学 | 0.065 |

---

## 📝 分析建议

1. **主题识别**：文档主要讨论「教育教学」相关话题
2. **高频词特征**：名词占比最高（39.4%），符合说明文特征
3. **用词多样性**：去重词数/总词数 = 26.8%，词汇丰富度中等
```

---

## 停用词表

内置中文停用词表，包括：

### 常见停用词

```
的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有 看 好 自己 这
```

### 标点符号

```
， 。 、 ； ： ？ ！ " " ' ' （ ） 《 》 【 】 … — ～
```

### 数量词（可选过滤）

```
一些 几个 很多 所有 每个 这个 那个 这些 那些
```

---

## 自定义词典

支持添加自定义词典，确保专有名词正确分词：

```python
# 添加人名
jieba.add_word("张三")
jieba.add_word("李四")

# 添加专业术语
jieba.add_word("核心素养")
jieba.add_word("深度学习")
jieba.add_word("大单元教学")

# 添加机构名
jieba.add_word("教育部")
jieba.add_word("人民教育出版社")
```

---

## 使用示例

### 示例 1：分析语文教材

**用户**：请分析这份八年级语文教材的词频

**输出**：
- Top 50 高频词表格
- 词云图
- 词性分布图
- 关键词提取

### 示例 2：对比两篇文章

**用户**：请对比这两篇文章的词频差异

**输出**：
- 两篇文章的独立词频统计
- 共有高频词对比
- 差异词对比
- 风格分析

### 示例 3：提取关键词

**用户**：从这份文档中提取 10 个关键词

**输出**：
- 基于 TF-IDF 的关键词列表
- 每个词的得分和解释

---

## 依赖库与安装自检

> ⚠️ 本技能依赖本地 Python 环境，未安装对应库会**静默失败**。请先安装。

```bash
pip install jieba wordcloud matplotlib pandas python-docx pdfplumber ebooklib beautifulsoup4
# 可选：情感分析 / TF-IDF 高级分析
pip install textblob scikit-learn
```

```python
# 核心库
jieba >= 0.42.1          # 中文分词
wordcloud >= 1.9.2       # 词云生成
matplotlib >= 3.7.0      # 图表绘制
pandas >= 2.0.0          # 数据处理
collections              # 词频统计（内置）

# 文档提取
python-docx >= 0.8.11    # Word 文档
pdfplumber >= 0.9.0      # PDF 提取
ebooklib >= 0.18         # EPUB 提取
beautifulsoup4 >= 4.12.0 # HTML 提取

# 可选
textblob >= 0.17.1       # 情感分析
scikit-learn >= 1.2.0    # TF-IDF 计算
```

**安装自检**：`python -c "import jieba, wordcloud, matplotlib, pandas, docx, pdfplumber; print('依赖就绪')"`
**额外注意**：
- 停用词表：脚本依赖 `stopwords.txt`，若环境没有请自备一份中文停用词表，否则跳过停用词过滤。
- 中文字体：词云 / 图表需中文字体（如 `simhei.ttf`），否则中文会显示为方框。

---

## 注意事项

1. **中文字体**：生成词云图需要中文字体文件（如 simhei.ttf）
2. **PDF 质量**：扫描版 PDF 需要 OCR 处理，可能影响准确率
3. **专业术语**：建议提供自定义词典以提高分词准确率
4. **大文件处理**：超过 10MB 的文档可能需要较长处理时间
5. **隐私保护**：敏感文档建议本地处理，不上传云端

---

## 扩展功能（可选）

### 1. 批量分析

支持同时分析多个文档，进行对比：

```
请分析这 5 份文档的词频，并对比差异
```

### 2. 时间序列分析

分析文档中词频的时间分布（适用于日记、日志等）：

```
分析这份日记中每月的情感变化
```

### 3. 情感分析

分析文档的情感倾向：

```
分析这份文档的情感倾向是积极还是消极
```

### 4. 主题建模

使用 LDA 等算法识别文档主题：

```
识别这份文档的主要主题
```

---

## 限制说明

1. 扫描版 PDF 需要 OCR 支持，准确率可能受影响
2. 古籍文言文分词准确率低于现代文
3. 高度专业化文档需要自定义词典支持
4. 词云图不支持太长的词语（建议不超过 10 字）

---

*技能版本：1.0*
*适用场景：文本分析、教学研究、内容审核、写作辅助、文献研究*
