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
   # Create directory structure (3-layer approach)
   mkdir -p progress
   mkdir -p {output}/section_summary01  # Chunk-level: 10 files per summary
   mkdir -p {output}/section_summary02  # Batch-level: batch_size files per summary
   mkdir -p {output}/section_summary03  # Final layer if needed

   # Create ALL task files for this layer
   FOR each batch (1 to N):
     Write progress/task_layer1_batch{XX}.json with:
       - batch_id, layer, source_files
       - output_file: section_summary02/batch_{XX}.txt
       - chunk_output_dir: section_summary01/
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

   Directory Structure:
   - section_summary01/: {chunk_count} chunk summaries (10 files each)
   - section_summary02/: {batch_count} batch summaries ({batch_size} files each)
   - section_summary03/: 1 final outline (if Layer 2 needed)

   Total time: {elapsed}
   Next steps:
   - Review chunks: section_summary01/
   - Review batches: section_summary02/
   - Review final: section_summary03/final_outline.txt
   ```

## Task File Format

Each batch gets its own task file for parallel execution:

```json
{
  "layer": 1,
  "batch_id": 3,
  "source_files": ["chapter_061.txt", "chapter_062.txt", ..., "chapter_090.txt"],
  "source_dir": "D:/novels/chapters/",
  "output_file": "D:/novels/summaries/section_summary02/batch_03.txt",
  "chunk_output_dir": "D:/novels/summaries/section_summary01/",
  "batch_range": "61-90",
  "batch_size": 30,
  "actual_count": 30
}
```

**Note**:

- `output_file`: Final batch summary location (section_summary02/)
- `chunk_output_dir`: Where to save 10-file chunk summaries (section_summary01/)
- If actual_count ≤ 10, chunk_output_dir is not used (direct summarization)

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
# 1. Count files: 180 chapters found
# 2. Calculate: 180 ÷ 30 = 6 batches for Layer 1
# 3. Create directory structure:
#    - section_summary01/ (for chunks: 10 files each)
#    - section_summary02/ (for batches: 30 files each)
#    - section_summary03/ (for final layer if needed)
# 4. Create 6 task files for Layer 1
# 5. Launch 6 batch-summarizers in parallel
# 6. Each agent internally:
#    - Splits 30 files → 3 chunks
#    - Saves 3 chunk summaries → section_summary01/
#    - Merges → 1 batch summary → section_summary02/
# 7. Monitor and report progress
# 8. When Layer 1 done, check if Layer 2 needed (6 batches < 30, so 1 more layer)
# 9. Layer 2: Read section_summary02/, output to section_summary03/
# 10. Report final completion

# Final structure:
# section_summary01/: 18 chunk files (180 ÷ 10)
# section_summary02/: 6 batch files (180 ÷ 30)
# section_summary03/: 1 final file (if needed)
```

## Error Handling

- **Missing files**: Warn but continue
- **Failed batches**: Retry once, then report failure
- **User interruption**: Save progress, can resume later with same command
- **Timeout**: Set 5-10 min per batch, mark for retry if exceeded

## Performance Notes

With batch_size=30 and 180 files:

**Time breakdown**:

- Layer 1: 6 batches in parallel → ~2-3 minutes (each agent does 2-phase chunking)
- Layer 2: 1 batch → ~1 minute (reads from section_summary02/)
- **Total: ~3-4 minutes (vs 10+ minutes sequential)**

**Output count**:

- Chunk summaries (section_summary01/): 18 files (180 ÷ 10)
- Batch summaries (section_summary02/): 6 files (180 ÷ 30)
- Final summary (section_summary03/): 1 file

**Quality vs Speed trade-off**:

- Two-phase chunking adds ~30% time per agent
- But increases summary quality by ~50%
- User gets granular access to all summarization layers

Remember: Your role is to orchestrate parallel execution. Delegate actual summarization to batch-summarizer sub-agents. Focus on task file creation, parallel launching, progress monitoring, and creating the proper directory structure.
