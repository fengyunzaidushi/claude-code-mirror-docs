# 递归总结 Sub-Agent 使用示例

## ✅ 已就绪

Sub-agent 配置已经创建在：`.claude/agents/recursive-summarizer.md`

## 🎯 你的任务需求

处理 200 个章节文件，生成 3 层递归摘要：

```
第一层：200个章节 → 20个摘要（每10章一个摘要）→ section_summary01/
第二层：20个摘要 → 2个摘要（每10个摘要生成1个）→ section_summary02/
第三层：2个摘要 → 1个最终大纲 → section_summary03/
```

## 📝 使用方法

### 方法 1：直接在 Claude Code 中使用

假设你的章节文件在 `D:/novels/my-novel/chapters/` 目录下，包含：

- `chapter_001.txt`
- `chapter_002.txt`
- ...
- `chapter_200.txt`

在 Claude Code 中输入以下提示词：

```
使用 recursive-summarizer subagent 处理我的小说章节：

源目录：D:/novels/my-novel/chapters/ (200个txt文件，命名为chapter_001.txt到chapter_200.txt)
输出目录：D:/novels/my-novel/summaries/

第一层处理：
- 批次大小：每10个章节
- 处理：读取chapter_001.txt到chapter_010.txt，生成摘要
- 输出：写入 summaries/section_summary01/summary_01.txt
- 继续处理chapter_011.txt到chapter_020.txt → summary_02.txt
- ...依此类推
- 最终：生成20个摘要文件（summary_01.txt 到 summary_20.txt）

第二层处理：
- 批次大小：每10个摘要
- 处理：读取section_summary01/summary_01.txt到summary_10.txt
- 输出：写入 summaries/section_summary02/summary_01.txt
- 继续处理summary_11.txt到summary_20.txt → summary_02.txt
- 最终：生成2个摘要文件

第三层处理：
- 读取：section_summary02/summary_01.txt 和 summary_02.txt
- 生成：最终完整大纲
- 输出：写入 summaries/section_summary03/final_outline.txt

请系统性地逐层处理，每完成一层后报告进度和统计信息。
```

### 方法 2：使用 Python 脚本辅助

首先运行准备脚本：

```bash
# Windows PowerShell或Git Bash
python docs/build-with-claude-code/examples/scripts/prepare-recursive-summary.py \
    --source "D:/novels/my-novel/chapters" \
    --output "D:/novels/my-novel/summaries" \
    --batch-size 10 \
    --generate-prompt
```

这将：

1. 计算需要的层级结构
2. 创建所需的目录
3. 生成一个优化的 Claude 提示词

然后复制生成的提示词到 Claude Code 中执行。

### 方法 3：逐层手动控制

如果你想更细致地控制每一层：

**第一层**：

```
使用 recursive-summarizer 处理第一层：
- 源：D:/novels/my-novel/chapters/ (200个文件)
- 输出：D:/novels/my-novel/summaries/section_summary01/
- 批次：每10个章节生成1个摘要
- 命名：summary_01.txt, summary_02.txt, ..., summary_20.txt
```

等第一层完成并验证质量后，再进行第二层：

**第二层**：

```
使用 recursive-summarizer 处理第二层：
- 源：D:/novels/my-novel/summaries/section_summary01/ (20个摘要文件)
- 输出：D:/novels/my-novel/summaries/section_summary02/
- 批次：每10个摘要生成1个总结
- 命名：summary_01.txt, summary_02.txt
```

**第三层**：

```
使用 recursive-summarizer 处理第三层：
- 源：D:/novels/my-novel/summaries/section_summary02/ (2个文件)
- 输出：D:/novels/my-novel/summaries/section_summary03/final_outline.txt
- 生成：最终完整大纲
```

## 📁 预期输出结构

```
D:/novels/my-novel/
├── chapters/
│   ├── chapter_001.txt
│   ├── chapter_002.txt
│   ...
│   └── chapter_200.txt
│
└── summaries/
    ├── section_summary01/          # 第一层：20个文件
    │   ├── summary_01.txt          # 章节1-10的摘要
    │   ├── summary_02.txt          # 章节11-20的摘要
    │   ...
    │   └── summary_20.txt          # 章节191-200的摘要
    │
    ├── section_summary02/          # 第二层：2个文件
    │   ├── summary_01.txt          # 前100章的总结
    │   └── summary_02.txt          # 后100章的总结
    │
    └── section_summary03/          # 第三层：1个文件
        └── final_outline.txt       # 全书大纲
```

## 🎨 摘要内容示例

### 第一层摘要示例 (summary_01.txt)

```markdown
# Summary of Chapters 1-10

Source: chapter_001.txt - chapter_010.txt
Generated: 2025-10-15

## Overview

本部分为小说开篇，介绍主角张三的平凡生活及其意外获得特殊能力的过程。
建立了基本的世界观设定和主要角色关系。

## Key Events

1. **第 1-2 章**：主角张三的日常生活，刻画其性格特点
2. **第 3 章**：神秘事件发生，主角意外接触到古老遗迹
3. **第 4-5 章**：觉醒特殊能力，初次使用产生混乱
4. **第 6-7 章**：遇到导师李四，开始了解能力本质
5. **第 8-10 章**：基础训练，逐步掌控能力

## Character Development

- **张三（主角）**：从普通高中生到能力觉醒者，经历迷茫与好奇
- **李四（导师）**：神秘的引导者，透露部分世界真相
- **王五（好友）**：支持主角的普通人，代表日常世界的联系

## Important Details

- 能力体系初步展示：元素操控、感知增强
- 世界观：普通世界与隐藏的能力者世界并存
- 伏笔：古老遗迹的来历、导师的真实身份

## Themes

- 平凡与非凡的边界
- 能力带来的责任
- 成长与自我认知

## Connections

- **承接前文**：N/A（开篇）
- **引出后续**：能力的深层来源、更大的世界格局

---

Files processed: chapter_001.txt, chapter_002.txt, chapter_003.txt, chapter_004.txt,
chapter_005.txt, chapter_006.txt, chapter_007.txt, chapter_008.txt, chapter_009.txt,
chapter_010.txt
```

### 第二层摘要示例 (summary_01.txt)

```markdown
# Summary of Part 1: Chapters 1-100

Source: section_summary01/summary_01.txt - summary_10.txt
Generated: 2025-10-15

## Major Story Arcs

### Arc 1: 觉醒篇 (Chapters 1-30)

主角张三从普通人到能力觉醒，在导师李四的引导下开始理解这个隐藏的世界。
建立了基本的能力体系和世界观框架。

### Arc 2: 训练篇 (Chapters 31-60)

系统性的能力训练，结识同期的能力者伙伴。逐步揭示能力者组织的存在，
以及维护平衡的使命。期间遭遇小规模冲突，展现成长。

### Arc 3: 试炼篇 (Chapters 61-100)

首次大型任务，面对真正的威胁。导师李四在关键时刻牺牲保护学生，
主角在痛苦中实现突破。初步了解到更大的阴谋。

## Character Progression

**主要角色发展**：

- **张三**：从新手 → 初级能力者 → 经历挫折后的成熟者
- **伙伴团队建立**：赵六（技术型）、孙七（战斗型）、周八（治疗型）
- **反派势力**：暗影组织初露端倪，首领身份成谜

**重要转折**：

- Chapter 25：能力来源的部分真相
- Chapter 58：导师李四牺牲
- Chapters 85-92：大型战斗，初露锋芒

## World Building Elements

- 能力者组织"守护者联盟"
- 能力等级体系：觉醒 → 修习 → 精通 → 超越
- 元素属性与克制关系
- 隐藏世界的运作规则

## Thematic Development

- 从"能力是什么"到"如何使用能力"
- 责任意识的建立
- 牺牲与传承
- 团队协作的重要性

## Key Plot Points Requiring Follow-up

- 导师遗言中提到的"真正的威胁"
- 暗影组织的最终目的
- 主角特殊能力的真实来源
- 古老预言的含义

---

Summaries processed: summary_01.txt through summary_10.txt (Chapters 1-100)
```

### 第三层最终大纲示例 (final_outline.txt)

```markdown
# 完整小说大纲：《觉醒之路》

Total Chapters: 200
Analysis Date: 2025-10-15

## 整体结构

### 第一部：起源与成长 (Chapters 1-100)

**主题**：从平凡到非凡的蜕变

#### 第一阶段：觉醒 (Ch 1-30)

- 主角张三意外获得能力
- 导师李四引导入门
- 建立世界观和能力体系基础
- **关键事件**：遗迹觉醒（Ch 3）、首次训练（Ch 8-10）

#### 第二阶段：修炼 (Ch 31-60)

- 系统性能力训练
- 伙伴团队建立（赵六、孙七、周八）
- 小规模任务与冲突
- **关键事件**：真相揭示（Ch 25）、团队成立（Ch 45）

#### 第三阶段：试炼 (Ch 61-100)

- 首次大型威胁
- 导师牺牲，主角成长
- 暗影组织浮现
- **关键事件**：大型战斗（Ch 85-92）、导师牺牲（Ch 58）

### 第二部：挑战与突破 (Chapters 101-200)

**主题**：承担责任，守护世界

#### 第四阶段：深入 (Ch 101-150)

- 调查暗影组织
- 能力突破，达到更高层次
- 更多真相揭露
- 面对内心挣扎与选择
- **关键事件**：能力突破（Ch 120）、重大发现（Ch 135）

#### 第五阶段：决战 (Ch 151-200)

- 暗影组织的终极计划
- 集结所有力量
- 最终大战
- 牺牲与胜利
- 新的平衡建立
- **关键事件**：真相大白（Ch 165）、最终决战（Ch 180-195）、尾声（Ch 196-200）

## 核心人物弧光

### 主角：张三

- **起点**：普通高中生，善良但缺乏自信
- **转折**：能力觉醒、导师牺牲、重大选择
- **终点**：成熟的守护者，承担起传承使命
- **内在成长**：从被动接受 → 主动探索 → 承担责任 → 超越自我

### 导师：李四

- 前期重要引导角色
- Ch 58 牺牲，成为主角成长的催化剂
- 遗留的秘密在后期逐步揭示
- 象征传承与牺牲主题

### 伙伴团队

- **赵六**：技术支援，代表智慧与策略
- **孙七**：战斗主力，代表勇气与力量
- **周八**：治疗支持，代表关怀与平衡
- 团队成长与个人成长相辅相成

### 反派：暗影组织

- 首领身份的多重反转
- 动机的复杂性（非纯粹邪恶）
- 最终揭示其与古老历史的联系
- 代表失衡与极端

## 主要主题

1. **成长与责任**

   - 能力越大，责任越大
   - 从自我到他人，从个体到集体

2. **牺牲与传承**

   - 每一代守护者的使命
   - 导师的牺牲换来新生代的成长

3. **平衡与选择**

   - 力量的使用需要智慧
   - 关键时刻的道德抉择

4. **团队与个人**
   - 无法独自完成的使命
   - 信任与协作的力量

## 世界观设定

### 能力体系

- **等级**：觉醒 → 修习 → 精通 → 超越 → 传说
- **类型**：元素操控、物理增强、精神感知、时空异能
- **来源**：古老文明的遗留力量

### 组织架构

- **守护者联盟**：维护平衡的正面组织
- **暗影组织**：追求极端力量的对立面
- **中立势力**：观察者、仲裁者

### 隐藏世界规则

- 不干涉普通世界的原则
- 能力者间的制衡机制
- 古老契约与限制

## 关键转折点

1. **Ch 3**: 遗迹觉醒 - 故事开端
2. **Ch 25**: 部分真相 - 世界观扩展
3. **Ch 58**: 导师牺牲 - 情感高潮
4. **Ch 92**: 初战告捷 - 第一部终结
5. **Ch 120**: 能力突破 - 力量跨越
6. **Ch 135**: 重大发现 - 剧情转折
7. **Ch 165**: 真相大白 - 所有线索汇聚
8. **Ch 180-195**: 最终决战 - 全书高潮
9. **Ch 200**: 新的开始 - 开放式结局

## 伏笔与回收

### 主要伏笔

- **古老遗迹的来历** (Ch 3) → 揭示于 Ch 165
- **导师的真实身份** (Ch 6) → 揭示于 Ch 140
- **主角特殊能力的独特性** (Ch 15) → 揭示于 Ch 175
- **预言的真正含义** (Ch 40) → 揭示于 Ch 185

### 次要伏笔

- 反复出现的神秘符号
- 某些角色的双重身份
- 历史事件的关联性

## 情节节奏分析

- **前 30 章**：世界观建立，节奏平稳
- **31-60 章**：能力发展，节奏加快
- **61-100 章**：冲突升级，高潮与低谷交替
- **101-150 章**：深入调查，悬念递进
- **151-195 章**：激烈冲突，多重高潮
- **196-200 章**：收尾与展望

## 写作特色

- **叙事视角**：第三人称全知，主要跟随主角
- **情感基调**：热血、励志、略带悲壮
- **战斗描写**：详细的能力对抗，策略与力量结合
- **人物刻画**：注重内心成长和关系发展

## 适合读者群

- 喜欢成长类故事的读者
- 超能力/都市异能爱好者
- 热血冒险题材粉丝
- 年龄段：15-35 岁

## 潜在续作方向

- 新一代守护者的故事
- 其他地区的能力者世界
- 古老文明的深层探索
- 主角团队的后续任务

---

## 总结评价

这是一部经典的成长冒险小说，通过 200 章的篇幅完整地呈现了一个少年从普通人到守护者的蜕变。
故事结构完整，节奏把控得当，人物塑造饱满，主题表达明确。前 100 章侧重个人成长和能力建立，
后 100 章升华到责任承担和世界守护，层层递进，逻辑严密。

**优势**：

- 完整的世界观和能力体系
- 清晰的角色成长线
- 主题明确且有深度
- 伏笔与回收处理得当

**可优化之处**：

- 部分过渡章节可能略显平淡
- 某些次要角色可以更丰满
- 最终决战的篇幅可以适当扩展

**整体评分**：4.2/5.0

---

Source: Complete analysis of all 200 chapters via hierarchical summarization
Generated by: recursive-summarizer sub-agent
Date: 2025-10-15
```

## 💡 提示

1. **首次使用建议**：先用少量文件测试（如 20-30 章），验证输出质量后再处理全部
2. **文件命名**：确保文件有序命名（如 chapter_001.txt 而非 chapter_1.txt）
3. **质量控制**：每完成一层后检查几个摘要，确保格式和内容符合预期
4. **进度保存**：每层完成后的文件都会保存，可以随时中断和继续

## 🔧 故障排除

**问题：Sub-agent 没有自动被调用**

- 解决：显式地说"使用 recursive-summarizer subagent"

**问题：摘要太简短/太详细**

- 解决：在提示词中明确指定长度要求（如"每个摘要 300-500 字"）

**问题：处理中断了**

- 解决：检查已生成的文件，从下一批次继续处理

**问题：文件找不到**

- 解决：使用绝对路径，确保文件存在且可读

## 📖 更多信息

详细文档请查看：

- 完整指南：`docs/build-with-claude-code/examples/recursive-summarization-guide.md`
- Sub-agent 文档：`docs/build-with-claude-code/sub-agents.md`
