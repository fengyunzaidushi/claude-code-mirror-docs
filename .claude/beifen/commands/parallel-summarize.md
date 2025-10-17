---
description: Start parallel hierarchical summarization using batch-summarizer sub-agents
argument-hint: [source_dir] [batch_size] [output_base_dir]
allowed-tools: Read, Write, Bash, Grep, Glob, SubAgent
model: sonnet
---

# Parallel Hierarchical Summarization Controller

You are controlling a parallel hierarchical summarization workflow. Your job is to:

1. **Parse user configuration** from arguments:

   - `$1`: Source directory (e.g., `D:/novels/chapters/`)
   - `$2`: Batch size (e.g., `30` - how many files each sub-agent can process)
   - `$3`: Output base directory (e.g., `D:/novels/summaries/`)

2. **Analyze and plan**:

   - Count total files in source directory
   - Calculate layers and batches: `ceil(files / batch_size)` per layer
   - Plan directory structure for each layer
   - Display the execution plan to user

3. **Execute Layer by Layer with PARALLEL sub-agents**:

   **For Layer 1:**

   ```
   # Create progress directory
   mkdir -p progress
   mkdir -p {output}/section_summary01

   # Create ALL task files for this layer
   FOR each batch (1 to N):
     Write progress/task_layer1_batch{XX}.json with:
       - batch_id, layer, source_files, output_file
       - batch_size, actual_count, batch_range
   END FOR

   # Launch ALL batch-summarizer sub-agents in PARALLEL
   FOR each batch (1 to N):
     Invoke: "Use batch-summarizer sub-agent to process task_layer1_batch{XX}.json"
     Print: "🚀 Launched batch {X}/{N}"
     # DON'T WAIT - launch next one immediately!
   END FOR

   Print: "✅ Launched {N} sub-agents in parallel for Layer 1"
   Print: "⏳ Monitoring completion... (check every 15-20 seconds)"

   # Monitor completion asynchronously
   WHILE not all batches complete:
     Check for output files
     Report progress: "Layer 1: X/N completed (Y in progress)"
     Sleep 15 seconds
   END WHILE
   ```

   **For subsequent layers:** Repeat the same process using previous layer's outputs as inputs

4. **Progress tracking**:

   - Create individual task files: `progress/task_layer{L}_batch{N}.json`
   - Monitor by checking output file existence
   - Report completion status frequently

5. **Final report**:

   ```
   ====================================
   HIERARCHICAL SUMMARIZATION COMPLETE
   ====================================

   Source: {source_dir} ({total} files)
   Configuration: batch_size = {batch_size}

   Layer 1: {N} summaries → section_summary01/ (PARALLEL)
   Layer 2: {M} summaries → section_summary02/ (PARALLEL)
   ...

   Total time: {elapsed}
   Next steps: Review final outline at {final_path}
   ```

## Task File Format

Each batch gets its own task file for parallel execution:

```json
{
  "layer": 1,
  "batch_id": 3,
  "source_files": ["chapter_061.txt", "chapter_062.txt", ..., "chapter_090.txt"],
  "source_dir": "D:/novels/chapters/",
  "output_file": "D:/novels/summaries/section_summary01/summary_03.txt",
  "batch_range": "61-90",
  "batch_size": 30,
  "actual_count": 30
}
```

## Key Principles

1. **Parallel execution within layers**: All batches in same layer run simultaneously
2. **Sequential between layers**: Must wait for entire layer to complete before next
3. **Independent task files**: Each batch has its own task file
4. **Async monitoring**: Check output files periodically, don't block
5. **User visibility**: Report progress frequently so user knows what's happening

## Example Usage

```bash
# User invokes:
/parallel-summarize D:/novels/chapters/ 30 D:/novels/summaries/

# You will:
# 1. Count files: 185 chapters found
# 2. Calculate: Layer 1 = 7 batches, Layer 2 = 1 batch
# 3. Create 7 task files for Layer 1
# 4. Launch 7 batch-summarizers in parallel
# 5. Monitor and report progress
# 6. When Layer 1 done, proceed to Layer 2
# 7. Report final completion
```

## Error Handling

- **Missing files**: Warn but continue
- **Failed batches**: Retry once, then report failure
- **User interruption**: Save progress, can resume later with same command
- **Timeout**: Set 5-10 min per batch, mark for retry if exceeded

## Performance Notes

With batch_size=30 and 185 files:

- Layer 1: 7 batches in parallel → ~1-2 minutes (vs 7+ minutes sequential)
- Layer 2: 1 batch → ~1 minute
- **Total: ~2-3 minutes (vs 8+ minutes sequential)**

Remember: Your role is to orchestrate parallel execution. Delegate actual summarization to batch-summarizer sub-agents. Focus on task file creation, parallel launching, and progress monitoring.
