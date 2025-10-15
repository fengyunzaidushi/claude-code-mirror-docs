# 递归分层总结完整指南 (Recursive Hierarchical Summarization Guide)

本指南展示如何使用 sub-agent 实现大规模文档的递归分层总结功能。

## 使用场景

适合以下场景：

- 小说章节总结（200 章 → 层级摘要 → 大纲）
- 研究论文批量综述
- 会议记录的周/月/季度总结
- 大型文档集的知识提取

## 快速开始

### 1. 创建 Sub-Agent

在项目根目录创建 `.claude/agents/recursive-summarizer.md`：

```bash
mkdir -p .claude/agents
```

将以下内容保存到该文件：

```markdown
---
name: recursive-summarizer
description: Recursively summarizes text files in batches to create hierarchical summaries. Use proactively when asked to summarize large collections of text files.
tools: Read, Write, Bash, Grep, Glob
model: sonnet
---

You are a specialized document summarization expert focused on creating hierarchical summaries.

When invoked:

1. Read files in specified batches (default: 10 files)
2. Generate coherent summaries for each batch
3. Write summaries to appropriate layer directories
4. Process recursively until reaching final summary

For each summary:

- Preserve key information and narrative flow
- Include source file references
- Maintain consistent formatting
- Report progress after each batch

Work systematically through all layers until complete.
```

### 2. 准备目录结构

假设你有 200 个章节文件在 `chapters/` 目录：

```bash
# 创建输出目录
mkdir -p summaries/section_summary01
mkdir -p summaries/section_summary02
mkdir -p summaries/section_summary03
```

### 3. 在 Claude Code 中调用

在 Claude Code 中输入：

```
使用 recursive-summarizer subagent 处理我的小说章节：

源目录：chapters/ (200个txt文件)

第一层：每10章总结一次
- 读取 chapters/chapter_001.txt 到 chapter_010.txt
- 生成摘要写入 summaries/section_summary01/summary_01.txt
- 继续处理下一批10章...
- 最终生成20个摘要文件

第二层：每10个摘要总结一次
- 读取 summaries/section_summary01/ 中的前10个摘要
- 生成摘要写入 summaries/section_summary02/summary_01.txt
- 继续处理后10个摘要
- 最终生成2个摘要文件

第三层：最终总结
- 读取 summaries/section_summary02/ 中的2个摘要
- 生成最终大纲写入 summaries/section_summary03/final_outline.txt

请系统性处理，每完成一层后报告进度。
```

## 详细示例：200 章小说总结

### 层级结构

```
chapters/                           (200 files)
    ├─ chapter_001.txt
    ├─ chapter_002.txt
    ...
    └─ chapter_200.txt
              ↓
summaries/section_summary01/       (20 files)
    ├─ summary_01.txt (chapters 1-10)
    ├─ summary_02.txt (chapters 11-20)
    ...
    └─ summary_20.txt (chapters 191-200)
              ↓
summaries/section_summary02/       (2 files)
    ├─ summary_01.txt (summaries 1-10)
    └─ summary_02.txt (summaries 11-20)
              ↓
summaries/section_summary03/       (1 file)
    └─ final_outline.txt (complete outline)
```

### 第一层处理示例

Sub-agent 会按以下方式处理：

**批次 1** (chapters 1-10):

```
读取: chapter_001.txt, chapter_002.txt, ..., chapter_010.txt
生成: summaries/section_summary01/summary_01.txt

内容示例：
# Summary of Chapters 1-10
Source: chapter_001.txt - chapter_010.txt

## Overview
这十章介绍了主角的背景和初始冲突...

## Key Events
1. 主角登场，展示其平凡的日常生活 (第1-2章)
2. 意外事件打破平静，主角获得特殊能力 (第3章)
3. 首次使用能力，产生意想不到的后果 (第4-5章)
...

## Character Development
- 主角：从普通学生转变为能力者，内心挣扎
- 配角A：导师角色出现，提供关键指引
...

## Themes
- 能力与责任
- 成长与选择
...
```

**批次 2** (chapters 11-20):

```
读取: chapter_011.txt, ..., chapter_020.txt
生成: summaries/section_summary01/summary_02.txt
```

...依此类推，直到生成 20 个摘要文件。

### 第二层处理示例

**批次 1** (summaries 1-10):

```
读取: section_summary01/summary_01.txt 到 summary_10.txt
生成: section_summary02/summary_01.txt

内容示例：
# Summary of Novel Part 1 (Chapters 1-100)
Source: summary_01.txt - summary_10.txt (Chapters 1-100)

## Major Story Arcs
1. 起源篇 (Chapters 1-30): 主角获得能力并学习控制
2. 训练篇 (Chapters 31-60): 正式修炼，结识重要伙伴
3. 初试篇 (Chapters 61-100): 首次真正的挑战与成长

## Character Progression
- 主角：从新手到初步掌握能力
- 主要配角群建立
- 反派势力初现

## Key Plot Points
- 获得能力的真相揭示 (Chapter 25)
- 重要导师牺牲 (Chapter 58)
- 第一次大型战斗 (Chapters 85-92)
...
```

### 第三层处理示例

```
读取: section_summary02/summary_01.txt 和 summary_02.txt
生成: section_summary03/final_outline.txt

内容示例：
# Complete Novel Outline: [小说标题]
Total Chapters: 200

## Part 1: Origins and Training (Chapters 1-100)
[从summary_01.txt总结的内容]

### Act 1: Discovery (Chapters 1-30)
- 主角背景与世界观建立
- 获得能力的契机
- 初步探索与困惑

### Act 2: Development (Chapters 31-60)
- 系统性训练
- 伙伴关系建立
- 能力体系展开

### Act 3: First Trials (Chapters 61-100)
- 实战考验
- 重大转折
- 为后续铺垫

## Part 2: Challenges and Growth (Chapters 101-200)
[从summary_02.txt总结的内容]

### Act 4: Rising Conflict (Chapters 101-150)
...

### Act 5: Climax and Resolution (Chapters 151-200)
...

## Overall Themes
...

## Character Arcs
...

## World Building Elements
...

## Narrative Structure
...
```

## 使用 Python 辅助脚本

可以使用准备脚本来自动化设置：

```bash
# 运行准备脚本
python docs/build-with-claude-code/examples/scripts/prepare-recursive-summary.py \
    --source ./chapters \
    --output ./summaries \
    --batch-size 10 \
    --generate-prompt

# 输出会显示：
# - 层级结构计算
# - 创建的目录
# - 为Claude准备的提示词
```

然后复制生成的提示词到 Claude Code 中执行。

## 自定义配置

### 调整批次大小

根据文件长度和复杂度调整：

- **小文件/简单内容**: batch-size = 15-20
- **中等文件**: batch-size = 10 (默认)
- **大文件/复杂内容**: batch-size = 5-8

### 调整摘要详细程度

在 sub-agent 配置中修改：

```markdown
## Summary Guidelines

For detailed summaries (学术/技术文档):

- Target: 500-1000 words per batch
- Include specific data, arguments, methods
- Preserve technical terminology

For concise summaries (快速概览):

- Target: 200-300 words per batch
- Focus on main points only
- Use simple language
```

### 特定领域定制

**技术文档总结**：

```markdown
Focus on:

- Core concepts and definitions
- Methodologies and algorithms
- Results and conclusions
- Dependencies between documents
```

**小说章节总结**：

```markdown
Focus on:

- Plot progression
- Character development
- Thematic elements
- Foreshadowing and callbacks
```

**会议记录总结**：

```markdown
Focus on:

- Decisions made
- Action items
- Key discussions
- Attendees and dates
```

## 进阶技巧

### 1. 渐进式验证

在处理全部文件前，先测试小批次：

```
先用 recursive-summarizer 处理前30章作为测试：
- 第一层：前30章 → 3个摘要
- 第二层：3个摘要 → 1个总结

检查质量后再处理全部200章。
```

### 2. 断点续传

如果处理中断，可以从特定层级继续：

```
继续处理第二层摘要：
- 已完成：section_summary01/ (20个文件)
- 继续：从section_summary01/读取，生成section_summary02/
```

### 3. 并行处理（高级）

对于超大规模（如 1000+文件），可以分区处理：

```
分成两组并行处理：
组1：chapters_part1/ (chapters 1-500)
组2：chapters_part2/ (chapters 501-1000)

最后合并两组的顶层摘要。
```

### 4. 质量控制

在每层添加验证步骤：

```
处理第一层后：
1. 读取前3个生成的摘要
2. 检查格式是否一致
3. 验证是否包含源文件引用
4. 确认内容连贯性

如果满意，继续处理下一层。
```

## 常见问题

### Q: Sub-agent 会自动递归还是需要手动指导每一层？

A: 取决于你的提示词。如果明确说明所有层级，sub-agent 会自动完成全部。你也可以选择每层单独指导。

### Q: 处理 200 个文件大约需要多长时间？

A: 取决于：

- 文件大小（每个文件 1-10KB 较快）
- 批次大小（10 个/批是平衡点）
- 模型速度（Sonnet 较快）

估计：200 个 5KB 文件，约 10-20 分钟完成全部 3 层。

### Q: 如何确保摘要质量一致？

A: 在 sub-agent 的 system prompt 中：

- 提供明确的格式模板
- 定义质量标准
- 要求包含必要元素（源引用、关键点等）
- 使用一致的术语

### Q: 可以用于非文本文件吗？

A: Sub-agent 主要处理文本。对于其他格式：

- PDF: 先转换为 txt
- Word: 导出为 txt
- Markdown: 直接支持
- 代码文件: 需要特别配置 sub-agent

### Q: 如何处理不同语言的文档？

A: 在 sub-agent 配置中指定：

```markdown
Language handling:

- Detect source file language
- Generate summaries in the same language
- Or: Generate summaries in [specified language]
```

## 相关资源

- [Sub-agents 文档](../sub-agents.md)
- [MCP 集成](../mcp.md) - 连接外部摘要工具
- [Hooks 指南](../../reference/hooks.md) - 自动化工作流
- [工具配置](../../configuration/settings.md)

## 总结

使用 sub-agent 进行递归分层总结的关键点：

1. ✅ 创建专门的 summarizer sub-agent 配置
2. ✅ 准备清晰的目录结构
3. ✅ 提供明确的层级指示
4. ✅ 让 sub-agent 系统性地处理每一层
5. ✅ 在每层完成后验证质量

这种方法可以高效处理大规模文档集合，生成有价值的层级摘要和大纲。
